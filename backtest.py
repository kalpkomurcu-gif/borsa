"""
Filtre karsilastirmali backtest.

tarama.py'deki gercek gosterge fonksiyonlarini kullanir; pozisyon dongusu
burada acikca kurulur ki ESKI (MACD/RSI/MA) ve YENI (+ADX +Hacim) kriterler
ayni veri uzerinde yan yana hesaplanabilsin.

Iki getiri tanimi raporlanir:
  A) Giris fiyatindan cikisa   -> "3 gunden uzun sureni say" (ileriye donuk
                                  bilgi icerir, uygulanabilir degil)
  B) 4. gunun kapanisindan cikisa -> "3 gun sinyalde kalani al" (uygulanabilir)

Kullanim: python backtest.py
"""

import pandas as pd
import yfinance as yf

import tarama as T

PERIYOT = "1y"          # indirilecek gecmis
MIN_GUN = 3             # "3 gunden fazla" -> gun > 3
GIRIS_GUNU = 4          # B senaryosunda giris yapilan gun


def pozisyon_kur(close: pd.Series, giris: pd.Series, kalma: pd.Series) -> list[dict]:
    """Giris/kalma kosullarindan pozisyon listesi uretir."""
    poz, aktif = [], None
    for i, tarih in enumerate(close.index):
        if aktif is None and bool(giris.iloc[i]):
            aktif = {"giris_tarih": tarih, "giris_i": i,
                     "giris_fiyat": float(close.iloc[i]), "gun": 1}
        elif aktif is not None and bool(kalma.iloc[i]):
            aktif["gun"] += 1
        elif aktif is not None:
            aktif["cikis_tarih"] = tarih
            aktif["cikis_fiyat"] = float(close.iloc[i])
            poz.append(aktif)
            aktif = None
    if aktif is not None:
        aktif["acik"] = True
        aktif["cikis_fiyat"] = float(close.iloc[-1])
        aktif["cikis_tarih"] = close.index[-1]
        poz.append(aktif)
    return poz


def senaryo(sym, close, high, low, volume, adx_ac: bool, hacim_ac: bool) -> list[dict]:
    close = close.dropna()
    if len(close) < T.MIN_VERI:
        return []
    temel = T.sinyal_serisi(close)
    giris = temel.copy()
    kalma = temel.copy()

    if adx_ac:
        adx_ok = (T.adx(high.reindex(close.index), low.reindex(close.index), close)
                  > T.ADX_ESIK).fillna(False)
        giris &= adx_ok
        if not T.ADX_SADECE_GIRIS:
            kalma &= adx_ok
    if hacim_ac:
        hacim_ok = T.hacim_kosulu(volume.reindex(close.index))
        giris &= hacim_ok
        if not T.HACIM_SADECE_GIRIS:
            kalma &= hacim_ok

    out = []
    for p in pozisyon_kur(close, giris, kalma):
        p["hisse"] = sym
        i4 = p["giris_i"] + GIRIS_GUNU - 1
        p["gun4_fiyat"] = float(close.iloc[i4]) if i4 < len(close) else None
        out.append(p)
    return out


def ozet(poz: list[dict], etiket: str) -> dict:
    uzun = [p for p in poz if p["gun"] > MIN_GUN]
    kapali = [p for p in uzun if not p.get("acik")]
    acik = [p for p in uzun if p.get("acik")]

    def ret_a(p):
        return (p["cikis_fiyat"] / p["giris_fiyat"] - 1) * 100

    def ret_b(p):
        return None if not p["gun4_fiyat"] else (p["cikis_fiyat"] / p["gun4_fiyat"] - 1) * 100

    a = [ret_a(p) for p in kapali]
    b = [x for x in (ret_b(p) for p in kapali) if x is not None]
    aa = [ret_a(p) for p in acik]
    ab = [x for x in (ret_b(p) for p in acik) if x is not None]
    return {
        "etiket": etiket, "toplam_poz": len(poz), "uzun_poz": len(uzun),
        "kapali": len(kapali), "acik": len(acik),
        "A_toplam": sum(a), "A_ort": (sum(a)/len(a) if a else 0),
        "A_kazanan": sum(1 for x in a if x > 0),
        "B_toplam": sum(b), "B_ort": (sum(b)/len(b) if b else 0),
        "B_kazanan": sum(1 for x in b if x > 0), "B_sayi": len(b),
        "A_acik": sum(aa), "B_acik": sum(ab),
        "ort_gun": (sum(p["gun"] for p in uzun)/len(uzun) if uzun else 0),
        "kapali_poz": kapali,
    }


def main():
    tickers = [t + ".IS" for t in T.BIST100]
    print(f"{len(tickers)} hisse indiriliyor ({PERIYOT})...")
    data = yf.download(tickers, period=PERIYOT, interval="1d",
                       auto_adjust=True, progress=False, group_by="ticker")

    senaryolar = {
        "ESKI (MACD/RSI/MA)": dict(adx_ac=False, hacim_ac=False),
        "+ ADX>25": dict(adx_ac=True, hacim_ac=False),
        "+ Hacim>20g ort": dict(adx_ac=False, hacim_ac=True),
        "YENI (ADX + Hacim)": dict(adx_ac=True, hacim_ac=True),
    }
    sonuc, basarisiz = {k: [] for k in senaryolar}, []

    for t in tickers:
        sym = t.replace(".IS", "")
        try:
            d = data[t]
            if d["Close"].dropna().empty:
                basarisiz.append(sym)
                continue
            for ad, kw in senaryolar.items():
                sonuc[ad] += senaryo(sym, d["Close"], d["High"], d["Low"],
                                     d["Volume"], **kw)
        except Exception as e:
            basarisiz.append(f"{sym}({type(e).__name__})")

    ozetler = [ozet(v, k) for k, v in sonuc.items()]

    L = [
        "# Filtre Karsilastirmali Backtest",
        "",
        f"Veri: {PERIYOT} | Taranan: {len(T.BIST100)} hisse "
        f"| Veri alinamayan: {len(basarisiz)}",
        f"Filtre: sadece {MIN_GUN} gunden UZUN suren pozisyonlar",
        "",
        "A = giris fiyatindan cikisa (ileriye donuk bilgi icerir, uygulanabilir DEGIL)",
        f"B = {GIRIS_GUNU}. gun kapanisindan cikisa (uygulanabilir)",
        "",
        "| Senaryo | Kapali poz. | Ort. gun | A toplam | A ort | A kazanan | "
        "B toplam | B ort | B kazanan |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for o in ozetler:
        L.append(
            f"| {o['etiket']} | {o['kapali']} | {o['ort_gun']:.1f} "
            f"| {o['A_toplam']:+.1f}% | {o['A_ort']:+.2f}% | {o['A_kazanan']}/{o['kapali']} "
            f"| {o['B_toplam']:+.1f}% | {o['B_ort']:+.2f}% | {o['B_kazanan']}/{o['B_sayi']} |"
        )

    L += ["", "## Acik pozisyonlar (rapor gunu itibariyle)", "",
          "| Senaryo | Acik poz. | A toplam | B toplam |", "|---|---|---|---|"]
    for o in ozetler:
        L.append(f"| {o['etiket']} | {o['acik']} | {o['A_acik']:+.1f}% | {o['B_acik']:+.1f}% |")

    yeni = next(o for o in ozetler if o["etiket"].startswith("YENI"))
    en_iyi = sorted(yeni["kapali_poz"],
                    key=lambda p: -(p["cikis_fiyat"]/p["giris_fiyat"]))[:10]
    en_kotu = sorted(yeni["kapali_poz"],
                     key=lambda p: (p["cikis_fiyat"]/p["giris_fiyat"]))[:10]
    for baslik, grup in (("En iyi 10", en_iyi), ("En kotu 10", en_kotu)):
        L += ["", f"## YENI kriterler — {baslik}", "",
              "| Hisse | Giris | Giris F. | Cikis | Cikis F. | A % | B % | Gun |",
              "|---|---|---|---|---|---|---|---|"]
        for p in grup:
            ra = (p["cikis_fiyat"]/p["giris_fiyat"]-1)*100
            rb = ("-" if not p["gun4_fiyat"]
                  else f"{(p['cikis_fiyat']/p['gun4_fiyat']-1)*100:+.1f}%")
            L.append(
                f"| {p['hisse']} | {p['giris_tarih']:%d.%m.%Y} | {p['giris_fiyat']:.2f} "
                f"| {p['cikis_tarih']:%d.%m.%Y} | {p['cikis_fiyat']:.2f} "
                f"| {ra:+.1f}% | {rb} | {p['gun']} |"
            )

    L += ["", "Not: Yuzdeler her isleme esit tutar konuldugu ve bilesiklenme "
              "olmadigi varsayimiyla toplanmistir; portfoy getirisi degildir. "
              "Komisyon/slipaj dahil degildir."]
    if basarisiz:
        L += ["", f"Veri alinamayan: {', '.join(basarisiz)}"]

    metin = "\n".join(L) + "\n"
    import os
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/backtest.md", "w", encoding="utf-8") as f:
        f.write(metin)
    print(metin)


if __name__ == "__main__":
    main()
