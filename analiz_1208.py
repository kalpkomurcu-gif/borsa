"""
Tek seferlik karsilastirma: 12.08.2026 kapanisina gore ESKI ve YENI kriterler.

ESKI : MACD > Sinyal, RSI > 50, Kapanis > MA5/MA9/MA21, ADX > 25, Hacim (giriste)
YENI : MACD > Sinyal, RSI > 50, MA5 > MA21, ADX > 25, Hacim (giriste),
       son 20 gunluk baz genisligi < %18 (giriste)

YENI taraf tarama.py'nin yayindaki kodunu (T.pozisyonlar) dogrudan cagirir;
ESKI taraf degisiklik oncesi mantigin birebir kopyasidir. Veri 12.08.2026'ya
kadar kirpilir, boylece rapor o gunun kapanisiyla uretilmis gibi olur.

Cikti: sonuclar/analiz_1208.md   (gunluk latest.md'ye DOKUNMAZ)
"""

import pandas as pd
import yfinance as yf

import gostergeler as G
import tarama as T

SON_GUN = pd.Timestamp("2026-08-12")
CIKANLAR_GUN = T.CIKANLAR_GUN


# ---------------------------------------------------------------
# ESKI mantik — degisiklik oncesi tarama.py'nin birebir kopyasi
# ---------------------------------------------------------------
def temel_eski(close: pd.Series) -> pd.Series:
    close = close.dropna()
    ma5 = close.rolling(5).mean()
    ma9 = close.rolling(9).mean()
    ma21 = close.rolling(21).mean()
    macd_val = (T.macd_histogram(close) if T.MACD_MODE == "histogram"
                else T.macd_line(close))
    sinyal = ((macd_val > 0) & (T.rsi(close) > 50)
              & (close > ma5) & (close > ma9) & (close > ma21))
    sinyal.iloc[:30] = False
    return sinyal.fillna(False)


def pozisyonlar_eski(high, low, close, volume) -> list[dict]:
    close = close.dropna()
    if len(close) < T.MIN_VERI:
        return []
    temel = temel_eski(close)
    adx_ok = (T.adx(high.reindex(close.index), low.reindex(close.index), close)
              > T.ADX_ESIK).fillna(False)
    hacim_ok = T.hacim_kosulu(volume.reindex(close.index))

    giris_kosulu = temel & adx_ok & hacim_ok
    kalma_kosulu = temel & adx_ok          # hacim sadece giriste

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


# ---------------------------------------------------------------
def topla(data, poz_fn):
    """Tum hisseler icin aktif ve cikan pozisyonlari toplar."""
    aktifler, cikanlar, basarisiz = [], [], []
    esik = SON_GUN - pd.Timedelta(days=CIKANLAR_GUN)

    for t in T.TICKERS:
        sym = t.replace(".IS", "")
        try:
            d = data[t]
            kirp = d.index <= SON_GUN
            d = d[kirp]
            close = d["Close"].dropna()
            if close.empty:
                basarisiz.append(sym)
                continue
            for p in poz_fn(d["High"], d["Low"], close, d["Volume"]):
                if "guncel_fiyat" in p:
                    aktifler.append({
                        "hisse": sym,
                        "giris_tarih": p["giris_tarih"],
                        "giris_fiyat": round(p["giris_fiyat"], 2),
                        "guncel_fiyat": round(p["guncel_fiyat"], 2),
                        "getiri": T.getiri(p["giris_fiyat"], p["guncel_fiyat"]),
                        "gun": p["gun"],
                    })
                elif pd.Timestamp(p["cikis_tarih"]) >= esik:
                    cikanlar.append({
                        "hisse": sym,
                        "giris_tarih": p["giris_tarih"],
                        "giris_fiyat": round(p["giris_fiyat"], 2),
                        "cikis_tarih": p["cikis_tarih"],
                        "cikis_fiyat": round(p["cikis_fiyat"], 2),
                        "getiri": T.getiri(p["giris_fiyat"], p["cikis_fiyat"]),
                        "gun": p["gun"],
                    })
        except Exception as e:
            basarisiz.append(f"{sym}({type(e).__name__})")

    aktifler.sort(key=lambda x: x["getiri"], reverse=True)
    cikanlar.sort(key=lambda x: pd.Timestamp(x["cikis_tarih"]), reverse=True)
    return aktifler, cikanlar, basarisiz


def tablolar(baslik, aktifler, cikanlar):
    L = [f"## {baslik}", "",
         f"Listede: {len(aktifler)} | Son {CIKANLAR_GUN} gunde cikan: {len(cikanlar)}",
         "", f"### Aktif Sinyaller ({len(aktifler)})", ""]
    if aktifler:
        L += ["| Hisse | Giris Tarihi | Giris Fiyati | Guncel Fiyat | Getiri % | Gun |",
              "|---|---|---|---|---|---|"]
        for a in aktifler:
            L.append(f"| {a['hisse']} | {T.fmt_tarih(a['giris_tarih'])} "
                     f"| {a['giris_fiyat']} | {a['guncel_fiyat']} "
                     f"| {a['getiri']:+.1f}% | {a['gun']} |")
    else:
        L.append("Kriterleri saglayan hisse yok.")

    L += ["", f"### Listeden Cikanlar — Son {CIKANLAR_GUN} Gun ({len(cikanlar)})", ""]
    if cikanlar:
        L += ["| Hisse | Giris | Giris F. | Cikis | Cikis F. | Getiri % | Gun |",
              "|---|---|---|---|---|---|---|"]
        for c in cikanlar:
            L.append(f"| {c['hisse']} | {T.fmt_tarih(c['giris_tarih'])} "
                     f"| {c['giris_fiyat']} | {T.fmt_tarih(c['cikis_tarih'])} "
                     f"| {c['cikis_fiyat']} | {c['getiri']:+.1f}% | {c['gun']} |")
    else:
        L.append("Cikan yok.")
    return L


def main():
    print(f"{len(T.TICKERS)} hisse indiriliyor...")
    data = yf.download(T.TICKERS, period="6mo", interval="1d",
                       auto_adjust=True, progress=False, group_by="ticker")

    eski_a, eski_c, bas1 = topla(data, pozisyonlar_eski)
    yeni_a, yeni_c, bas2 = topla(data, T.pozisyonlar)

    e_set = {a["hisse"] for a in eski_a}
    y_set = {a["hisse"] for a in yeni_a}

    L = [f"# 12.08.2026 Kapanisi — Kriter Karsilastirmasi", "",
         f"Veri {SON_GUN:%d.%m.%Y} kapanisina kirpildi. Ayni veri, iki kriter seti.",
         ""]
    L += tablolar("ESKI kriterler (Fiyat > MA5/MA9/MA21)", eski_a, eski_c)
    L += [""]
    L += tablolar(f"YENI kriterler (MA5 > MA21 + baz genisligi < %{T.BAZ_ESIK:g})",
                  yeni_a, yeni_c)
    L += ["", "## Fark", "",
          f"- Eski listede {len(e_set)}, yeni listede {len(y_set)} hisse.",
          f"- Sadece ESKI'de: {', '.join(sorted(e_set - y_set)) or '—'}",
          f"- Sadece YENI'de: {', '.join(sorted(y_set - e_set)) or '—'}",
          f"- Ortak: {', '.join(sorted(e_set & y_set)) or '—'}"]
    if bas1 or bas2:
        L += ["", f"Veri alinamayan: {', '.join(sorted(set(bas1) | set(bas2)))}"]

    metin = "\n".join(L) + "\n"
    import os
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/analiz_1208.md", "w", encoding="utf-8") as f:
        f.write(metin)
    print(metin)


if __name__ == "__main__":
    main()
