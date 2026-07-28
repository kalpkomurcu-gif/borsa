"""
Filtre karsilastirmali backtest.

tarama.py'deki gercek gosterge fonksiyonlarini kullanir; pozisyon dongusu
burada acikca kurulur ki farkli kriter setleri ayni veri uzerinde yan yana
hesaplanabilsin.

Getiri = giris gunu kapanisi -> cikis gunu kapanisi. Tum pozisyonlar sayilir;
sure filtresi YOKTUR.

Kriterler:
  TEMEL : MACD > Sinyal, RSI > 50, Fiyat > MA5/MA9/MA21
  HACIM : o gunku hacim > onceki 20 gunun ortalamasi  (girise sart)
  ADX   : ADX(14) > 25

Kullanim: python backtest.py
"""

import pandas as pd
import yfinance as yf

import tarama as T

PERIYOT = "1y"


def pozisyon_kur(close: pd.Series, giris: pd.Series, kalma: pd.Series) -> list[dict]:
    """Giris/kalma kosullarindan pozisyon listesi uretir."""
    poz, aktif = [], None
    for i, tarih in enumerate(close.index):
        if aktif is None and bool(giris.iloc[i]):
            aktif = {"giris_tarih": tarih, "giris_fiyat": float(close.iloc[i]), "gun": 1}
        elif aktif is not None and bool(kalma.iloc[i]):
            aktif["gun"] += 1
        elif aktif is not None:
            aktif["cikis_tarih"] = tarih
            aktif["cikis_fiyat"] = float(close.iloc[i])
            poz.append(aktif)
            aktif = None
    if aktif is not None:
        aktif["acik"] = True
        aktif["cikis_tarih"] = close.index[-1]
        aktif["cikis_fiyat"] = float(close.iloc[-1])
        poz.append(aktif)
    return poz


def senaryo(sym, close, high, low, volume, hacim: bool, adx: str | None) -> list[dict]:
    """adx: None | 'surekli' (her gun aranir) | 'giris' (sadece giriste)."""
    close = close.dropna()
    if len(close) < T.MIN_VERI:
        return []
    temel = T.sinyal_serisi(close)
    giris, kalma = temel.copy(), temel.copy()

    if adx:
        adx_ok = (T.adx(high.reindex(close.index), low.reindex(close.index), close)
                  > T.ADX_ESIK).fillna(False)
        giris &= adx_ok
        if adx == "surekli":
            kalma &= adx_ok
    if hacim:
        giris &= T.hacim_kosulu(volume.reindex(close.index))

    for p in (out := pozisyon_kur(close, giris, kalma)):
        p["hisse"] = sym
        p["getiri"] = (p["cikis_fiyat"] / p["giris_fiyat"] - 1) * 100
    return out


def ozet(poz: list[dict], etiket: str) -> dict:
    kapali = [p for p in poz if not p.get("acik")]
    acik = [p for p in poz if p.get("acik")]
    r = sorted(p["getiri"] for p in kapali)
    n = len(r)
    medyan = 0.0 if not n else (r[n // 2] if n % 2 else (r[n // 2 - 1] + r[n // 2]) / 2)
    kaz = [x for x in r if x > 0]
    kyb = [x for x in r if x <= 0]
    return {
        "etiket": etiket, "kapali": n, "acik": len(acik),
        "toplam": sum(r), "ort": (sum(r) / n if n else 0), "medyan": medyan,
        "kazanan": len(kaz),
        "kazanan_ort": (sum(kaz) / len(kaz) if kaz else 0),
        "kaybeden_ort": (sum(kyb) / len(kyb) if kyb else 0),
        "ort_gun": (sum(p["gun"] for p in kapali) / n if n else 0),
        "en_iyi": (r[-1] if n else 0), "en_kotu": (r[0] if n else 0),
        "acik_toplam": sum(p["getiri"] for p in acik),
        "kapali_poz": kapali,
    }


SENARYOLAR = {
    "TEMEL (MACD/RSI/MA)":        dict(hacim=False, adx=None),
    "+ Hacim":                    dict(hacim=True,  adx=None),
    "+ ADX (surekli)":            dict(hacim=False, adx="surekli"),
    "+ ADX (sadece giris)":       dict(hacim=False, adx="giris"),
    "TUMU — ADX surekli":         dict(hacim=True,  adx="surekli"),
    "TUMU — ADX sadece giris":    dict(hacim=True,  adx="giris"),
}


def main():
    tickers = [t + ".IS" for t in T.BIST100]
    print(f"{len(tickers)} hisse indiriliyor ({PERIYOT})...")
    data = yf.download(tickers, period=PERIYOT, interval="1d",
                       auto_adjust=True, progress=False, group_by="ticker")

    sonuc, basarisiz = {k: [] for k in SENARYOLAR}, []
    for t in tickers:
        sym = t.replace(".IS", "")
        try:
            d = data[t]
            if d["Close"].dropna().empty:
                basarisiz.append(sym)
                continue
            for ad, kw in SENARYOLAR.items():
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
        "Getiri: giris gunu kapanisi -> cikis gunu kapanisi. "
        "Tum pozisyonlar dahil, sure filtresi yok.",
        f"Hacim: o gunku hacim > onceki {T.HACIM_PERIYOT} gunun ortalamasi (girise sart). "
        f"ADX esigi: {T.ADX_ESIK:g}",
        "",
        "| Kriter seti | Poz. | Ort. gun | Toplam % | Ort. % | Medyan % | "
        "Kazanma | Kazanan ort. | Kaybeden ort. | En iyi | En kotu |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for o in ozetler:
        oran = f"{100*o['kazanan']/o['kapali']:.0f}%" if o["kapali"] else "-"
        L.append(
            f"| {o['etiket']} | {o['kapali']} | {o['ort_gun']:.1f} "
            f"| {o['toplam']:+.1f}% | {o['ort']:+.2f}% | {o['medyan']:+.2f}% "
            f"| {oran} ({o['kazanan']}/{o['kapali']}) "
            f"| {o['kazanan_ort']:+.2f}% | {o['kaybeden_ort']:+.2f}% "
            f"| {o['en_iyi']:+.1f}% | {o['en_kotu']:+.1f}% |"
        )

    L += ["", "## Acik pozisyonlar (rapor gunu itibariyle)", "",
          "| Kriter seti | Acik poz. | Toplam % |", "|---|---|---|"]
    for o in ozetler:
        L.append(f"| {o['etiket']} | {o['acik']} | {o['acik_toplam']:+.1f}% |")

    # Tam kriter setinin (senin istedigin) islem dagilimi
    tam = next(o for o in ozetler if o["etiket"] == "TUMU — ADX surekli")
    L += ["", "## Tum kriterler — sure dagilimi", "",
          "| Tutus suresi | Poz. | Toplam % | Ort. % | Kazanma |", "|---|---|---|---|---|"]
    for et, alt, ust in [("1 gun", 1, 1), ("2-3 gun", 2, 3), ("4-7 gun", 4, 7),
                         ("8-15 gun", 8, 15), ("16+ gun", 16, 10**6)]:
        g = [p["getiri"] for p in tam["kapali_poz"] if alt <= p["gun"] <= ust]
        if not g:
            continue
        L.append(f"| {et} | {len(g)} | {sum(g):+.1f}% | {sum(g)/len(g):+.2f}% "
                 f"| {100*sum(1 for x in g if x>0)/len(g):.0f}% |")

    for baslik, ters in (("En iyi 15", True), ("En kotu 15", False)):
        grup = sorted(tam["kapali_poz"], key=lambda p: p["getiri"], reverse=ters)[:15]
        L += ["", f"## Tum kriterler — {baslik}", "",
              "| Hisse | Giris | Giris F. | Cikis | Cikis F. | Getiri % | Gun |",
              "|---|---|---|---|---|---|---|"]
        for p in grup:
            L.append(
                f"| {p['hisse']} | {p['giris_tarih']:%d.%m.%Y} | {p['giris_fiyat']:.2f} "
                f"| {p['cikis_tarih']:%d.%m.%Y} | {p['cikis_fiyat']:.2f} "
                f"| {p['getiri']:+.1f}% | {p['gun']} |"
            )

    L += ["", "Not: Yuzdeler her isleme esit tutar konuldugu ve bilesiklenme "
              "olmadigi varsayimiyla toplanmistir; portfoy getirisi degildir. "
              "Fiyatlar kapanistir, komisyon/slipaj dahil degildir."]
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
