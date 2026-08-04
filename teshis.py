"""
Veri teshisi — "son gunun verisi neden yok?" sorusunu kesin cevaplar.

Problem: gunluk.py 03.08.2026 taramasinda 100 hissenin 99'unun son veri
gununu 31.07 buldu. tarama.py ise ayni gunlerde sorunsuz calisiyor.
Iki dosya Yahoo'dan FARKLI sekilde indiriyor; hangi farkin sorumlu
oldugu tahminle degil olcumle bulunmali.

Farklar:
                tarama.py        veri.py
  period        6mo              2y
  auto_adjust   True             False
  parcalama     yok (100 birden) var (15'erli)
  threads       varsayilan       False

Bu script her kombinasyonu ayri ayri deneyip her birinin DONEN SON
TARIHINI basar. Ayrica borsanin o gun acik olup olmadigini anlamak icin
tek tek birkac sembolu ham API'den sorgular.

Kullanim: python teshis.py [SEMBOL ...]     (varsayilan birkac BIST hissesi)
"""

from __future__ import annotations

import sys

import pandas as pd
import yfinance as yf

ORNEK = ["AKSA.IS", "AKBNK.IS", "THYAO.IS", "EREGL.IS", "GARAN.IS"]


def son_tarihler(df: pd.DataFrame, semboller: list[str]) -> dict[str, str]:
    """Her sembol icin Close'u dolu olan son barin tarihi."""
    out = {}
    for s in semboller:
        try:
            if isinstance(df.columns, pd.MultiIndex):
                if s not in df.columns.get_level_values(0):
                    out[s] = "SEMBOL YOK"
                    continue
                kapanis = df[s]["Close"]
            else:
                kapanis = df["Close"]
            kapanis = pd.to_numeric(kapanis, errors="coerce").dropna()
            out[s] = (f"{pd.Timestamp(kapanis.index[-1]):%Y-%m-%d} "
                      f"({kapanis.iloc[-1]:.2f})") if len(kapanis) else "BOS"
        except Exception as exc:
            out[s] = f"HATA {type(exc).__name__}"
    return out


def dene(ad: str, semboller: list[str], **kw) -> None:
    print(f"\n--- {ad} ---")
    print(f"    {kw}")
    try:
        df = yf.download(semboller, interval="1d", progress=False,
                         group_by="ticker", **kw)
        if df is None or df.empty:
            print("    BOS CERCEVE")
            return
        print(f"    cerceve son 3 tarih: "
              f"{[str(pd.Timestamp(t).date()) for t in df.index[-3:]]}")
        for s, v in son_tarihler(df, semboller).items():
            print(f"      {s:12s} {v}")
    except Exception as exc:
        print(f"    HATA: {type(exc).__name__}: {exc}")


def ham_api(sembol: str) -> None:
    """
    yfinance'i atlayip Yahoo chart API'sini dogrudan sorgular.
    Borsanin o gun acik olup olmadigini en dogrudan bu gosterir.
    """
    import json
    import urllib.request

    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sembol}"
           f"?range=1mo&interval=1d")
    try:
        istek = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(istek, timeout=30) as y:
            veri = json.load(y)
        sonuc = veri["chart"]["result"][0]
        zaman = sonuc["timestamp"]
        kapanis = sonuc["indicators"]["quote"][0]["close"]
        print(f"\n--- ham API: {sembol} ---")
        print(f"    borsa saat dilimi: {sonuc['meta'].get('exchangeTimezoneName')}")
        print(f"    son 6 bar:")
        for t, k in list(zip(zaman, kapanis))[-6:]:
            g = pd.Timestamp(t, unit="s", tz="Europe/Istanbul")
            print(f"      {g:%Y-%m-%d %a}  kapanis={k}")
    except Exception as exc:
        print(f"\n--- ham API: {sembol} --- HATA {type(exc).__name__}: {exc}")


def main() -> None:
    semboller = sys.argv[1:] or ORNEK
    print("=" * 62)
    print(f"VERI TESHISI — {pd.Timestamp.now():%Y-%m-%d %H:%M}")
    print(f"yfinance {yf.__version__} | pandas {pd.__version__}")
    print(f"Semboller: {', '.join(semboller)}")
    print("=" * 62)

    # tarama.py'nin yaptigi (calisiyor)
    dene("tarama.py tarzi", semboller, period="6mo", auto_adjust=True)
    # veri.py'nin yaptigi (sorunlu)
    dene("veri.py tarzi", semboller, period="2y", auto_adjust=False,
         threads=False)
    # Farklari tek tek izole et
    dene("sadece period farki (2y + auto_adjust)", semboller,
         period="2y", auto_adjust=True)
    dene("sadece auto_adjust farki (6mo + adj kapali)", semboller,
         period="6mo", auto_adjust=False)
    dene("sadece threads farki (6mo + adj + threads kapali)", semboller,
         period="6mo", auto_adjust=True, threads=False)
    # Tarih araligini acikca vermek fark yaratiyor mu?
    bugun = pd.Timestamp.now().normalize()
    dene("period yerine start/end", semboller,
         start=(bugun - pd.Timedelta(days=200)).strftime("%Y-%m-%d"),
         end=(bugun + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
         auto_adjust=True)

    for s in semboller[:2]:
        ham_api(s)

    print("\n" + "=" * 62)
    print("OKUMA:")
    print("  - Tum yontemler ayni son tarihi veriyorsa: Yahoo'da o gunun")
    print("    verisi YOK. Borsa kapaliysa normal; aciksa Yahoo geride.")
    print("  - Yontemler FARKLI tarih veriyorsa: sorun indirme")
    print("    parametrelerinde, hangi satirin farkli oldugu yukarida.")
    print("  - Ham API son barin gerçek tarihini gosterir; yfinance")
    print("    katmanindan bagimsizdir.")
    print("=" * 62)


if __name__ == "__main__":
    main()
