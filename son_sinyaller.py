"""
Son N gunde sinyale GIREN tum hisseler ve kar/zararlari.

tarama.py'nin gosterge fonksiyonlarini kullanir; gunluk raporla ayni
5 kriter gecerlidir:
  MACD > Sinyal, RSI > 50, Fiyat > MA5/MA9/MA21, ADX(14) > 25,
  Hacim > onceki 20 gunun ortalamasi (girise sart)

ARTI, sadece bu raporda gecerli DENEME kriteri:
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


def pozisyonlar_deneme(high, low, close, volume) -> list[dict]:
    """
    tarama.pozisyonlar() ile ayni; tek fark girise eklenen
    "kapanis > onceki kapanis" kosulu. Kalma kosulu degismez.
    """
    close = close.dropna()
    if len(close) < T.MIN_VERI:
        return []
    temel = T.sinyal_serisi(close)
    adx_ok = (T.adx(high.reindex(close.index), low.reindex(close.index), close)
              > T.ADX_ESIK).fillna(False)
    hacim_ok = T.hacim_kosulu(volume.reindex(close.index))

    giris_kosulu = temel & adx_ok & hacim_ok
    if YUKARI_GUN_SART:
        giris_kosulu &= (close > close.shift(1)).fillna(False)

    kalma_kosulu = temel.copy()
    if not T.ADX_SADECE_GIRIS:
        kalma_kosulu &= adx_ok
    if not T.HACIM_SADECE_GIRIS:
        kalma_kosulu &= hacim_ok

    poz, aktif = [], None
    for i, tarih in enumerate(close.index):
        if aktif is None and bool(giris_kosulu.iloc[i]):
            aktif = {"giris_tarih": tarih, "giris_fiyat": float(close.iloc[i]),
                     "gun": 1}
        elif aktif is not None and bool(kalma_kosulu.iloc[i]):
            aktif["gun"] += 1
        elif aktif is not None:
            aktif["cikis_tarih"] = tarih
            aktif["cikis_fiyat"] = float(close.iloc[i])
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

    esik = pd.Timestamp(datetime.now() - timedelta(days=GUN)).normalize()
    kayitlar, basarisiz = [], []

    for t in tickers:
        sym = t.replace(".IS", "")
        try:
            d = data[t]
            if d["Close"].dropna().empty:
                basarisiz.append(sym)
                continue
            for p in pozisyonlar_deneme(d["High"], d["Low"], d["Close"], d["Volume"]):
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
        f"Kriterler: MACD > Sinyal, RSI > 50, Fiyat > MA5/MA9/MA21, "
        f"ADX({T.ADX_PERIYOT}) > {T.ADX_ESIK:g}, "
        f"Hacim > onceki {T.HACIM_PERIYOT} gun ortalamasi (girise sart)"
        + (", **Kapanis > onceki gun kapanisi (girise sart)**"
           if YUKARI_GUN_SART else ""),
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
                f"| {'LISTEDE' if k['acik'] else 'SATILDI'} |"
            )

        kapali = [k for k in kayitlar if not k["acik"]]
        aciklar = [k for k in kayitlar if k["acik"]]
        L += ["", "## Ozet", "",
              "| | Adet | Toplam % | Ortalama % |", "|---|---|---|---|"]
        for ad, grup in (("Satilanlar", kapali), ("Hala listede", aciklar),
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
