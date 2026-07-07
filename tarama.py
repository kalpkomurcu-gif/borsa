# -*- coding: utf-8 -*-
"""
BIST 100 Gunluk Tarama
Kriterler:
  1) MACD (12-26-9) > Sinyal cizgisi (al kesisimi bolgesi)
  2) RSI (14) > 50
  3) Kapanis > MA5 ve MA9 ve MA21 (SMA)

Kullanim: python bist100_screener.py
Gereksinim: pip install yfinance pandas
"""

import pandas as pd
import yfinance as yf

# ---------------------------------------------------------------
# BIST 100 listesi (.IS = Borsa Istanbul, Yahoo Finance formati)
# NOT: Endeks bilesenleri donemsel degisir; listeyi guncel tut.
# ---------------------------------------------------------------
BIST100 = [
    "AEFES", "AGHOL", "AKBNK", "AKSA", "AKSEN", "ALARK", "ALFAS", "ANSGR",
    "ARCLK", "ASELS", "ASTOR", "BERA", "BIMAS", "BRSAN", "BRYAT", "BTCIM",
    "CCOLA", "CIMSA", "CLEBI", "CWENE", "DOAS", "DOHOL", "ECILC", "EGEEN",
    "EKGYO", "ENJSA", "ENKAI", "EREGL", "EUPWR", "FROTO", "GARAN", "GESAN",
    "GUBRF", "HALKB", "HEKTS", "ISCTR", "ISMEN", "KCAER", "KCHOL", "KONTR",
    "KONYA", "KOZAA", "KOZAL", "KRDMD", "MAVI", "MGROS", "MIATK", "MPARK",
    "ODAS", "OTKAR", "OYAKC", "PETKM", "PGSUS", "REEDR", "SAHOL", "SASA",
    "SISE", "SKBNK", "SMRTG", "SOKM", "TABGD", "TAVHL", "TCELL", "THYAO",
    "TKFEN", "TOASO", "TSKB", "TTKOM", "TTRAK", "TUKAS", "TUPRS", "TURSG",
    "ULKER", "VAKBN", "VESBE", "VESTL", "YKBNK", "YEOTK", "ZOREN", "DSTKF",
]
TICKERS = [t + ".IS" for t in BIST100]


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Wilder RSI"""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


# MACD kosulu modu:
#   "line"      -> MACD cizgisi > 0 (EMA12 > EMA26)  [cok kisitlayici, nadir sinyal]
#   "histogram" -> MACD > Sinyal cizgisi (al kesisimi bolgesi) [daha sik sinyal]
MACD_MODE = "histogram"


def macd_line(close: pd.Series, fast: int = 12, slow: int = 26) -> pd.Series:
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    return ema_fast - ema_slow


def macd_histogram(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
    macd = macd_line(close, fast, slow)
    sig = macd.ewm(span=signal, adjust=False).mean()
    return macd - sig


def screen(close: pd.Series) -> dict | None:
    """Tek hisse icin kriter kontrolu. Kriterler saglaniyorsa dict doner."""
    close = close.dropna()
    if len(close) < 60:  # yeterli veri yoksa atla
        return None

    ma5 = close.rolling(5).mean().iloc[-1]
    ma9 = close.rolling(9).mean().iloc[-1]
    ma21 = close.rolling(21).mean().iloc[-1]
    if MACD_MODE == "histogram":
        macd_val = macd_histogram(close).iloc[-1]
    else:
        macd_val = macd_line(close).iloc[-1]
    rsi_val = rsi(close).iloc[-1]
    price = close.iloc[-1]

    if (
        macd_val > 0
        and rsi_val > 50
        and price > ma5
        and price > ma9
        and price > ma21
    ):
        return {
            "Fiyat": round(price, 2),
            "MACD": round(macd_val, 3),
            "RSI": round(rsi_val, 1),
            "MA5": round(ma5, 2),
            "MA9": round(ma9, 2),
            "MA21": round(ma21, 2),
        }
    return None


def main():
    import json
    from datetime import datetime

    print("BIST 100 verileri indiriliyor...")
    data = yf.download(
        TICKERS, period="6mo", interval="1d",
        auto_adjust=True, progress=False, group_by="ticker",
    )

    results = {}
    failed = []
    for t in TICKERS:
        try:
            close = data[t]["Close"]
            hit = screen(close)
            if hit:
                results[t.replace(".IS", "")] = hit
        except Exception:
            failed.append(t.replace(".IS", ""))

    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    baslik = "MACD > Sinyal (al kesisimi), RSI > 50, Fiyat > MA5/MA9/MA21"

    # Konsol ciktisi
    print(f"\n=== KRITERLERI SAGLAYAN HISSELER ===\n({baslik})\n")
    lines_md = [f"# BIST 100 Tarama — {tarih}", "", f"Kriterler: {baslik}", ""]
    if results:
        df = pd.DataFrame(results).T.sort_values("RSI", ascending=False)
        print(df.to_string())
        lines_md.append("| Hisse | Fiyat | RSI | MACD Hist | MA5 | MA9 | MA21 |")
        lines_md.append("|---|---|---|---|---|---|---|")
        for sym, row in df.iterrows():
            lines_md.append(
                f"| {sym} | {row['Fiyat']} | {row['RSI']} | {row['MACD']} "
                f"| {row['MA5']} | {row['MA9']} | {row['MA21']} |"
            )
    else:
        print("Bugun kriterleri saglayan hisse yok.")
        lines_md.append("Bugun kriterleri saglayan hisse yok.")

    if failed:
        print(f"\nVeri alinamayan: {', '.join(failed)}")
        lines_md += ["", f"Veri alinamayan: {', '.join(failed)}"]

    # Dosya ciktilari (GitHub Actions bunlari commit eder)
    import os
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/latest.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines_md) + "\n")
    with open("sonuclar/latest.json", "w", encoding="utf-8") as f:
        json.dump({"tarih": tarih, "kriterler": baslik,
                   "sonuclar": results, "veri_alinamayan": failed},
                  f, ensure_ascii=False, indent=2, default=float)
    print("\nSonuclar sonuclar/latest.md ve latest.json dosyalarina yazildi.")


if __name__ == "__main__":
    main()
