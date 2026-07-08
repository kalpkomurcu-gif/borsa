"""
BIST 100 Gunluk Tarama — v3
Tum BIST 100 hisseleri taranir, SADECE kriterleri saglayanlar raporlanir.

Kriterler:
  1) MACD (12-26-9) > Sinyal cizgisi (al kesisimi bolgesi)
  2) RSI (14) > 50
  3) Kapanis > MA5 ve MA9 ve MA21 (SMA)

Kullanim: python tarama.py
Gereksinim: pip install yfinance pandas
"""

import pandas as pd
import yfinance as yf

# ---------------------------------------------------------------
# BIST 100 listesi — Temmuz 2026 bilesimi (100 hisse)
# NOT: Endeks bilesenleri ceyreklik degisir (Oca-Mar, Nis-Haz,
# Tem-Eyl, Eki-Ara); listeyi donem basinda guncel tut.
# ---------------------------------------------------------------
BIST100 = [
    "AEFES", "AKBNK", "AKSA",  "AKSEN", "ALARK", "ALTNY", "ANSGR", "ARCLK",
    "ASELS", "ASTOR", "BALSU", "BERA",  "BIMAS", "BRSAN", "BRYAT", "BSOKE",
    "BTCIM", "CANTE", "CCOLA", "CIMSA", "CVKMD", "CWENE", "DAPGM", "DOAS",
    "DOHOL", "DSTKF", "ECILC", "EFOR",  "EKGYO", "ENERY", "ENJSA", "ENKAI",
    "EREGL", "ESEN",  "EUPWR", "EUREN", "FENER", "FROTO", "GARAN", "GENIL",
    "GESAN", "GLRMK", "GRSEL", "GRTHO", "GSRAY", "GUBRF", "HALKB", "HEKTS",
    "IEYHO", "ISCTR", "ISMEN", "IZENR", "KCHOL", "KLRHO", "KRDMD", "KTLEV",
    "KUYAS", "MAGEN", "MAVI",  "MGROS", "MIATK", "MPARK", "OBAMS", "ODAS",
    "ODINE", "OTKAR", "OYAKC", "PAHOL", "PASEU", "PATEK", "PETKM", "PGSUS",
    "PSGYO", "QUAGR", "RALYH", "REEDR", "SAHOL", "SARKY", "SASA",  "SISE",
    "SKBNK", "SOKM",  "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TRALT",
    "TRENJ", "TRMET", "TSKB",  "TTKOM", "TUKAS", "TUPRS", "TURSG", "ULKER",
    "VAKBN", "VESTL", "YKBNK", "ZOREN",
]
TICKERS = [t + ".IS" for t in BIST100]

# Portfoy hisseleri (raporda yildizla isaretlenir)
PORTFOY = {"THYAO", "TUPRS", "ASELS", "DSTKF"}

# MACD kosulu modu:
#   "line"      -> MACD cizgisi > 0 (EMA12 > EMA26)
#   "histogram" -> MACD > Sinyal cizgisi (al kesisimi bolgesi)
MACD_MODE = "histogram"


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Wilder RSI"""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


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
    if len(close) < 60:  # yeterli veri yoksa atla (yeni halka arzlar vb.)
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
            "RSI": round(rsi_val, 1),
            "MACD": round(macd_val, 3),
            "MA5": round(ma5, 2),
            "MA9": round(ma9, 2),
            "MA21": round(ma21, 2),
        }
    return None


def md_satir(sym: str, row) -> str:
    isim = f"⭐ {sym}" if sym in PORTFOY else sym
    rsi_str = f"**{row['RSI']}** ⚠️" if row["RSI"] > 70 else str(row["RSI"])
    return (
        f"| {isim} | {row['Fiyat']} | {rsi_str} | {row['MACD']} "
        f"| {row['MA5']} | {row['MA9']} | {row['MA21']} |"
    )


def main():
    import json
    from datetime import datetime

    print(f"BIST 100 verileri indiriliyor... ({len(TICKERS)} hisse)")
    data = yf.download(
        TICKERS, period="6mo", interval="1d",
        auto_adjust=True, progress=False, group_by="ticker",
    )

    results = {}
    failed = []
    for t in TICKERS:
        sym = t.replace(".IS", "")
        try:
            close = data[t]["Close"]
            hit = screen(close)
            if hit:
                results[sym] = hit
        except Exception:
            failed.append(sym)

    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    baslik = "MACD > Sinyal (al kesisimi), RSI > 50, Fiyat > MA5/MA9/MA21"

    lines_md = [
        f"# BIST 100 Tarama — {tarih}",
        "",
        f"Kriterler: {baslik}",
        f"Taranan: {len(BIST100)} hisse | Kriterleri saglayan: {len(results)} "
        f"| ⭐ portfoy | ⚠️ RSI > 70 asiri alim",
        "",
    ]

    print(f"\n=== KRITERLERI SAGLAYAN HISSELER ({len(results)}/{len(BIST100)}) ===\n({baslik})\n")
    if results:
        df = pd.DataFrame(results).T.sort_values("RSI", ascending=False)
        print(df.to_string())
        lines_md.append("| Hisse | Fiyat | RSI | MACD Hist | MA5 | MA9 | MA21 |")
        lines_md.append("|---|---|---|---|---|---|---|")
        for sym, row in df.iterrows():
            lines_md.append(md_satir(sym, row))
    else:
        print("Bugun kriterleri saglayan hisse yok.")
        lines_md.append("Bugun kriterleri saglayan hisse yok.")

    # Portfoy hisselerinden sinyal vermeyenleri ayrica belirt
    portfoy_dis = sorted(PORTFOY - set(results.keys()))
    if portfoy_dis:
        lines_md += ["", f"Portfoyden sinyal vermeyenler: {', '.join(portfoy_dis)}"]

    if failed:
        print(f"\nVeri alinamayan: {', '.join(failed)}")
        lines_md += ["", f"Veri alinamayan: {', '.join(failed)}"]

    # Dosya ciktilari (GitHub Actions bunlari commit eder)
    import os
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/latest.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines_md) + "\n")
    with open("sonuclar/latest.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "tarih": tarih,
                "kriterler": baslik,
                "taranan_hisse_sayisi": len(BIST100),
                "sonuclar": results,
                "portfoy_sinyal_vermeyen": portfoy_dis,
                "veri_alinamayan": failed,
            },
            f, ensure_ascii=False, indent=2, default=float,
        )
    print("\nSonuclar sonuclar/latest.md ve latest.json dosyalarina yazildi.")


if __name__ == "__main__":
    main()
