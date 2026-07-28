"""
Son N gunde sinyale GIREN tum hisseler ve kar/zararlari.

tarama.py'nin gosterge fonksiyonlarini kullanir; gunluk raporla ayni
5 kriter gecerlidir:
  MACD > Sinyal, RSI > 50, ADX(14) > 25,
  Hacim > onceki 20 gunun ortalamasi (girise sart)

ARTI, sadece bu raporda gecerli DENEME kriterleri:
  MA kosulu: "Fiyat > MA5/MA9/MA21" yerine "MA5 > MA21" (surekli).
  Zarar kes: giristen kumule -4% ve altina dusen kapanista cikis.
  Goreli guc: son 21 islem gunu getirisi BIST100'u gecmeli (girise sart).
  Kapanis > onceki gunun kapanisi  —  YALNIZCA GIRISTE aranir.
  Cikis degerlendirmesine girmez; pozisyon dusen gunde de listede kalir.
Bu yuzden pozisyon dongusu tarama.py'den kopyalanip tek satir eklendi;
kalma kosulu tarama.py ile birebir aynidir.

Cikan hisse cikis fiyatindan satilmis sayilir; hala listede olan
guncel fiyattan degerlenir. Sure filtresi YOKTUR.

Kullanim: python son_sinyaller.py [gun_sayisi]   (varsayilan 15)
"""

import sys
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

import tarama as T

GUN = int(sys.argv[1]) if len(sys.argv) > 1 else 15

# Deneme kriteri: kapanis onceki gunun kapanisinin uzerinde olsun (sadece giris)
YUKARI_GUN_SART = True

# Zarar kes: kapanista giris fiyatina gore bu yuzdenin altina dusuldugu gun
# pozisyon kapatilir — kriterler hala saglaniyor olsa bile. None = kapali.
# Not: gap ile acilan sert dususte gerceklesen zarar bu esikten daha kotu
# olabilir; esik "ilk bu seviyeyi goren kapanista cik" demektir.
ZARAR_KES = -4.0

# Deneme kriteri: "Fiyat > MA5/MA9/MA21" yerine "MA5 > MA21".
# MA9 tamamen devre disi. Diger kriterler gibi SUREKLI bir kosuldur:
# hem girise hem listede kalmaya etki eder.
MA5_MA21_MODU = True

# Deneme kriteri: hissenin son GORECELI_PERIYOT islem gunundeki getirisi
# BIST100 endeksinin ayni donemdeki getirisinden BUYUK olmali.
# Sadece GIRISTE aranir; pozisyon endeksin gerisine dusunce cikmaz.
GORECELI_GUC = True
GORECELI_PERIYOT = 21      # ~1 ay (islem gunu)
# Yahoo'da BIST100 hem "XU100.IS" hem "^XU100" olarak duruyor; ilki bos
# donerse ikincisi denenir. 100 hisselik indirmenin hemen ardindan gelen
# istek bazen 429 yiyor, o yuzden her sembol icin birkac deneme yapilir.
ENDEKS_ADAYLARI = ["XU100.IS", "^XU100"]
ENDEKS_DENEME = 3


def endeks_kapanis() -> tuple[pd.Series, str]:
    """BIST100 kapanis serisini getirir. Hicbiri gelmezse SystemExit."""
    import time
    hatalar = []
    for sembol in ENDEKS_ADAYLARI:
        for deneme in range(1, ENDEKS_DENEME + 1):
            try:
                e = yf.download(sembol, period="6mo", interval="1d",
                                auto_adjust=True, progress=False)
                kap = e["Close"] if "Close" in e else pd.Series(dtype=float)
                if hasattr(kap, "columns"):      # tek ticker'da da DataFrame gelebilir
                    kap = kap.iloc[:, 0]
                kap = kap.dropna()
                if len(kap) > GORECELI_PERIYOT:
                    return kap, sembol
                hatalar.append(f"{sembol} deneme {deneme}: {len(kap)} satir (yetersiz)")
            except Exception as exc:
                hatalar.append(f"{sembol} deneme {deneme}: {type(exc).__name__}")
            time.sleep(3 * deneme)
    raise SystemExit(
        "HATA: BIST100 endeks verisi alinamadi, goreli guc kriteri "
        "hesaplanamiyor. Kriteri sessizce atlayip yaniltici rapor "
        "uretmemek icin duruluyor.\n  " + "\n  ".join(hatalar)
    )


def donem_getirisi(close: pd.Series, periyot: int) -> pd.Series:
    """Her gun icin son 'periyot' islem gunundeki yuzde degisim."""
    return close / close.shift(periyot) - 1


def temel_seri(close: pd.Series) -> pd.Series:
    """
    tarama.sinyal_serisi() ile ayni — tek fark MA kosulu.
    MA5_MA21_MODU=False ise tarama.py'nin kosulu birebir kullanilir.
    """
    if not MA5_MA21_MODU:
        return T.sinyal_serisi(close)

    close = close.dropna()
    macd_val = (T.macd_histogram(close) if T.MACD_MODE == "histogram"
                else T.macd_line(close))
    sinyal = (
        (macd_val > 0)
        & (T.rsi(close) > 50)
        & (close.rolling(5).mean() > close.rolling(21).mean())
    )
    sinyal.iloc[:30] = False   # ilk 30 bar: gostergeler oturmamis
    return sinyal.fillna(False)


def pozisyonlar_deneme(high, low, close, volume,
                       endeks_getiri: pd.Series | None = None) -> list[dict]:
    """
    tarama.pozisyonlar() ile ayni; tek fark girise eklenen
    "kapanis > onceki kapanis" kosulu. Kalma kosulu degismez.
    """
    close = close.dropna()
    if len(close) < T.MIN_VERI:
        return []
    temel = temel_seri(close)
    adx_ok = (T.adx(high.reindex(close.index), low.reindex(close.index), close)
              > T.ADX_ESIK).fillna(False)
    hacim_ok = T.hacim_kosulu(volume.reindex(close.index))

    giris_kosulu = temel & adx_ok & hacim_ok
    if YUKARI_GUN_SART:
        giris_kosulu &= (close > close.shift(1)).fillna(False)
    if GORECELI_GUC:
        if endeks_getiri is None:
            raise ValueError("GORECELI_GUC acik ama endeks getirisi verilmedi")
        hisse_getiri = donem_getirisi(close, GORECELI_PERIYOT)
        giris_kosulu &= (
            hisse_getiri > endeks_getiri.reindex(close.index)
        ).fillna(False)

    kalma_kosulu = temel.copy()
    if not T.ADX_SADECE_GIRIS:
        kalma_kosulu &= adx_ok
    if not T.HACIM_SADECE_GIRIS:
        kalma_kosulu &= hacim_ok

    poz, aktif = [], None
    for i, tarih in enumerate(close.index):
        fiyat = float(close.iloc[i])
        if aktif is None:
            if bool(giris_kosulu.iloc[i]):
                aktif = {"giris_tarih": tarih, "giris_fiyat": fiyat, "gun": 1}
            continue

        # Zarar kes kriterlerden ONCE bakilir: kosullar hala saglansa bile cikar.
        zarar = (fiyat / aktif["giris_fiyat"] - 1) * 100
        if ZARAR_KES is not None and zarar <= ZARAR_KES:
            sebep = "ZARAR KES"
        elif bool(kalma_kosulu.iloc[i]):
            aktif["gun"] += 1
            continue
        else:
            sebep = "KRITER"

        aktif["cikis_tarih"] = tarih
        aktif["cikis_fiyat"] = fiyat
        aktif["sebep"] = sebep
        poz.append(aktif)
        aktif = None

    if aktif is not None:
        aktif["guncel_fiyat"] = float(close.iloc[-1])
        poz.append(aktif)
    return poz


def main():
    tickers = [t + ".IS" for t in T.BIST100]
    print(f"{len(tickers)} hisse indiriliyor...")
    data = yf.download(tickers, period="6mo", interval="1d",
                       auto_adjust=True, progress=False, group_by="ticker")

    endeks_getiri, endeks_sembol = None, None
    if GORECELI_GUC:
        print("BIST100 endeksi indiriliyor...")
        ekapanis, endeks_sembol = endeks_kapanis()
        endeks_getiri = donem_getirisi(ekapanis, GORECELI_PERIYOT)
        print(f"  {endeks_sembol}: {len(ekapanis)} gun veri alindi "
              f"({ekapanis.index[0]:%d.%m.%Y} - {ekapanis.index[-1]:%d.%m.%Y})")

    esik = pd.Timestamp(datetime.now() - timedelta(days=GUN)).normalize()
    kayitlar, basarisiz = [], []

    for t in tickers:
        sym = t.replace(".IS", "")
        try:
            d = data[t]
            if d["Close"].dropna().empty:
                basarisiz.append(sym)
                continue
            for p in pozisyonlar_deneme(d["High"], d["Low"], d["Close"], d["Volume"],
                                        endeks_getiri):
                if pd.Timestamp(p["giris_tarih"]).normalize() < esik:
                    continue
                acik = "guncel_fiyat" in p
                satis = p["guncel_fiyat"] if acik else p["cikis_fiyat"]
                kayitlar.append({
                    "hisse": sym,
                    "giris_tarih": p["giris_tarih"],
                    "giris_fiyat": round(p["giris_fiyat"], 2),
                    "cikis_tarih": None if acik else p["cikis_tarih"],
                    "satis_fiyat": round(satis, 2),
                    "getiri": round((satis / p["giris_fiyat"] - 1) * 100, 1),
                    "gun": p["gun"],
                    "acik": acik,
                    "sebep": p.get("sebep", ""),
                })
        except Exception as e:
            basarisiz.append(f"{sym}({type(e).__name__})")

    kayitlar.sort(key=lambda x: -x["getiri"])
    karli = [k for k in kayitlar if k["getiri"] > 0]
    zararli = [k for k in kayitlar if k["getiri"] < 0]
    notr = [k for k in kayitlar if k["getiri"] == 0]
    toplam = sum(k["getiri"] for k in kayitlar)

    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [
        f"# Son {GUN} Gunde Sinyale Girenler — {tarih}",
        "",
        f"Kriterler: MACD > Sinyal, RSI > 50, "
        + ("**MA5 > MA21**" if MA5_MA21_MODU else "Fiyat > MA5/MA9/MA21")
        + f", ADX({T.ADX_PERIYOT}) > {T.ADX_ESIK:g}, "
        f"Hacim > onceki {T.HACIM_PERIYOT} gun ortalamasi (girise sart)"
        + (", **Kapanis > onceki gun kapanisi (girise sart)**"
           if YUKARI_GUN_SART else "")
        + (f", **Son {GORECELI_PERIYOT} gun getirisi > BIST100 "
            f"[{endeks_sembol}] (girise sart)**" if GORECELI_GUC else "")
        + (f", **Zarar kes: kapanista {ZARAR_KES:g}%**"
           if ZARAR_KES is not None else ""),
        f"Giris tarihi {esik:%d.%m.%Y} ve sonrasi olan TUM pozisyonlar. "
        "Sure filtresi yok.",
        "",
        f"**Toplam {len(kayitlar)} sinyal** | Karli: {len(karli)} | "
        f"Zararli: {len(zararli)}" + (f" | Notr: {len(notr)}" if notr else ""),
        "",
        f"**Getiri toplami: {toplam:+.1f}%** | "
        f"Ortalama: {toplam/len(kayitlar):+.2f}%" if kayitlar else "Sinyal yok.",
        "",
    ]

    if kayitlar:
        L += [
            "| Hisse | Giris | Giris F. | Cikis | Satis F. | Kar/Zarar | Gun | Durum |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for k in kayitlar:
            ct = "—" if k["acik"] else f"{pd.Timestamp(k['cikis_tarih']):%d.%m.%Y}"
            L.append(
                f"| {k['hisse']} | {pd.Timestamp(k['giris_tarih']):%d.%m.%Y} "
                f"| {k['giris_fiyat']} | {ct} | {k['satis_fiyat']} "
                f"| {k['getiri']:+.1f}% | {k['gun']} "
                f"| {'LISTEDE' if k['acik'] else k['sebep'] or 'KRITER'} |"
            )

        kapali = [k for k in kayitlar if not k["acik"]]
        aciklar = [k for k in kayitlar if k["acik"]]
        L += ["", "## Ozet", "",
              "| | Adet | Toplam % | Ortalama % |", "|---|---|---|---|"]
        zk = [k for k in kapali if k["sebep"] == "ZARAR KES"]
        kr = [k for k in kapali if k["sebep"] != "ZARAR KES"]
        for ad, grup in (("Kriter bozulunca satilan", kr),
                         ("Zarar kes ile satilan", zk),
                         ("Hala listede", aciklar),
                         ("TUMU", kayitlar)):
            if grup:
                s = sum(x["getiri"] for x in grup)
                L.append(f"| {ad} | {len(grup)} | {s:+.1f}% | {s/len(grup):+.2f}% |")

    L += ["", "Not: Yuzdeler her isleme esit tutar konuldugu ve bilesiklenme "
              "olmadigi varsayimiyla toplanmistir. Fiyatlar kapanistir; "
              "komisyon/slipaj dahil degildir."]
    if basarisiz:
        L += ["", f"Veri alinamayan: {', '.join(basarisiz)}"]

    metin = "\n".join(L) + "\n"
    import os
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/son_sinyaller.md", "w", encoding="utf-8") as f:
        f.write(metin)
    print(metin)


if __name__ == "__main__":
    main()
