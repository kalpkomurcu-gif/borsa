"""
Tek seferlik karsilastirma: 12.08.2026 kapanisina gore kriter setleri.

Dort varyant ayni veriyle taranir ki hangi degisiklik neyi eledigi gorulsun:
  A) ESKI          : Kapanis > MA5/MA9/MA21            (baz filtresi yok)
  B) SADECE MA     : MA5 > MA21                        (baz filtresi yok)
  C) SADECE BAZ    : Kapanis > MA5/MA9/MA21 + baz < %18
  D) YENI          : MA5 > MA21 + baz < %18            (yayindaki hali)

Ayrica ESKI'de olup YENI'de olmayan her hisse icin GIRIS GUNUNDEKI baz
genisligi yazilir — esigin nereye konmasi gerektigi buradan okunur.

Veri 12.08.2026'ya kirpilir. Cikti: sonuclar/analiz_1208.md
Gunluk latest.md'ye DOKUNMAZ.
"""

import pandas as pd
import yfinance as yf

import gostergeler as G
import tarama as T

SON_GUN = pd.Timestamp("2026-08-12")
CIKANLAR_GUN = T.CIKANLAR_GUN


def temel_seri(close: pd.Series, yeni_ma: bool) -> pd.Series:
    """yeni_ma=True -> MA5 > MA21 | False -> Kapanis > MA5/MA9/MA21."""
    close = close.dropna()
    macd_val = (T.macd_histogram(close) if T.MACD_MODE == "histogram"
                else T.macd_line(close))
    ortak = (macd_val > 0) & (T.rsi(close) > 50)
    if yeni_ma:
        sinyal = ortak & (close.rolling(5).mean() > close.rolling(21).mean())
    else:
        sinyal = (ortak
                  & (close > close.rolling(5).mean())
                  & (close > close.rolling(9).mean())
                  & (close > close.rolling(21).mean()))
    sinyal.iloc[:30] = False
    return sinyal.fillna(False)


def pozisyonlar(high, low, close, volume, yeni_ma: bool,
                baz_filtresi: bool) -> list[dict]:
    """tarama.pozisyonlar() ile ayni akis; MA ve baz secenekleri parametrik."""
    close = close.dropna()
    if len(close) < T.MIN_VERI:
        return []
    yuksek, dusuk = high.reindex(close.index), low.reindex(close.index)
    temel = temel_seri(close, yeni_ma)
    adx_ok = (T.adx(yuksek, dusuk, close) > T.ADX_ESIK).fillna(False)
    hacim_ok = T.hacim_kosulu(volume.reindex(close.index))

    giris_kosulu = temel & adx_ok & hacim_ok
    if baz_filtresi:
        giris_kosulu &= (G.baz_genisligi(yuksek, dusuk, T.BAZ_PERIYOT) * 100
                         < T.BAZ_ESIK).fillna(False)
    kalma_kosulu = temel & adx_ok          # hacim ve baz sadece giriste

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


def topla(data, yeni_ma, baz_filtresi):
    aktifler, cikanlar = [], []
    esik = SON_GUN - pd.Timedelta(days=CIKANLAR_GUN)
    for t in T.TICKERS:
        sym = t.replace(".IS", "")
        try:
            d = data[t]
            d = d[d.index <= SON_GUN]
            close = d["Close"].dropna()
            if close.empty:
                continue
            for p in pozisyonlar(d["High"], d["Low"], close, d["Volume"],
                                 yeni_ma, baz_filtresi):
                ortak = {"hisse": sym,
                         "giris_tarih": p["giris_tarih"],
                         "giris_fiyat": round(p["giris_fiyat"], 2),
                         "gun": p["gun"]}
                if "guncel_fiyat" in p:
                    aktifler.append({**ortak,
                                     "guncel_fiyat": round(p["guncel_fiyat"], 2),
                                     "getiri": T.getiri(p["giris_fiyat"],
                                                        p["guncel_fiyat"])})
                elif pd.Timestamp(p["cikis_tarih"]) >= esik:
                    cikanlar.append({**ortak,
                                     "cikis_tarih": p["cikis_tarih"],
                                     "cikis_fiyat": round(p["cikis_fiyat"], 2),
                                     "getiri": T.getiri(p["giris_fiyat"],
                                                        p["cikis_fiyat"])})
        except Exception:
            pass
    aktifler.sort(key=lambda x: x["getiri"], reverse=True)
    cikanlar.sort(key=lambda x: pd.Timestamp(x["cikis_tarih"]), reverse=True)
    return aktifler, cikanlar


def aktif_tablo(aktifler):
    if not aktifler:
        return ["Kriterleri saglayan hisse yok."]
    L = ["| Hisse | Giris Tarihi | Giris Fiyati | Guncel Fiyat | Getiri % | Gun |",
         "|---|---|---|---|---|---|"]
    for a in aktifler:
        L.append(f"| {a['hisse']} | {T.fmt_tarih(a['giris_tarih'])} "
                 f"| {a['giris_fiyat']} | {a['guncel_fiyat']} "
                 f"| {a['getiri']:+.1f}% | {a['gun']} |")
    return L


def cikan_tablo(cikanlar):
    if not cikanlar:
        return ["Cikan yok."]
    L = ["| Hisse | Giris | Giris F. | Cikis | Cikis F. | Getiri % | Gun |",
         "|---|---|---|---|---|---|---|"]
    for c in cikanlar:
        L.append(f"| {c['hisse']} | {T.fmt_tarih(c['giris_tarih'])} "
                 f"| {c['giris_fiyat']} | {T.fmt_tarih(c['cikis_tarih'])} "
                 f"| {c['cikis_fiyat']} | {c['getiri']:+.1f}% | {c['gun']} |")
    return L


def main():
    print(f"{len(T.TICKERS)} hisse indiriliyor...")
    data = yf.download(T.TICKERS, period="6mo", interval="1d",
                       auto_adjust=True, progress=False, group_by="ticker")

    varyantlar = [
        ("A) ESKI — Fiyat > MA5/MA9/MA21, baz filtresi yok", False, False),
        ("B) SADECE MA degisikligi — MA5 > MA21, baz filtresi yok", True, False),
        ("C) SADECE baz filtresi — eski MA + baz < %18", False, True),
        (f"D) YENI (yayinda) — MA5 > MA21 + baz < %{T.BAZ_ESIK:g}", True, True),
    ]

    sonuc = {}
    L = ["# 12.08.2026 Kapanisi — Kriter Karsilastirmasi", "",
         f"Veri {SON_GUN:%d.%m.%Y} kapanisina kirpildi; dort kriter seti ayni veriyle.",
         ""]

    for ad, yeni_ma, baz in varyantlar:
        a, c = topla(data, yeni_ma, baz)
        sonuc[ad[0]] = (a, c)
        L += [f"## {ad}", "",
              f"Listede: {len(a)} | Son {CIKANLAR_GUN} gunde cikan: {len(c)}", "",
              f"### Aktif Sinyaller ({len(a)})", ""] + aktif_tablo(a)
        L += ["", f"### Listeden Cikanlar ({len(c)})", ""] + cikan_tablo(c) + [""]

    # --- Elenenlerin giris gunundeki baz genisligi --------------------
    eski_a = sonuc["A"][0]
    yeni_isim = {x["hisse"] for x in sonuc["D"][0]}
    L += ["## Elenen hisselerin GIRIS GUNUNDEKI baz genisligi", "",
          f"Esik su an %{T.BAZ_ESIK:g}. Asagidaki hisseler eski kriterlerle "
          "listedeydi; giris gunundeki baz genisligi esigin ustunde oldugu "
          "icin yeni kriterlerde giris alamiyor.", "",
          "| Hisse | Giris | Getiri % | Baz genisligi | Durum |",
          "|---|---|---|---|---|"]
    for a in eski_a:
        t = a["hisse"] + ".IS"
        d = data[t]
        d = d[d.index <= SON_GUN]
        gen = G.baz_genisligi(d["High"], d["Low"], T.BAZ_PERIYOT) * 100
        try:
            deger = float(gen.loc[a["giris_tarih"]])
            gen_txt = f"%{deger:.1f}"
        except Exception:
            deger, gen_txt = float("nan"), "—"
        durum = "GECTI" if a["hisse"] in yeni_isim else "ELENDI"
        L.append(f"| {a['hisse']} | {T.fmt_tarih(a['giris_tarih'])} "
                 f"| {a['getiri']:+.1f}% | {gen_txt} | {durum} |")

    L += ["", "## Ozet", ""]
    for ad, _, _ in varyantlar:
        a, c = sonuc[ad[0]]
        isim = ", ".join(x["hisse"] for x in a) or "—"
        L.append(f"- **{ad}** -> {len(a)} hisse: {isim}")

    metin = "\n".join(L) + "\n"
    import os
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/analiz_1208.md", "w", encoding="utf-8") as f:
        f.write(metin)
    print(metin)


if __name__ == "__main__":
    main()
