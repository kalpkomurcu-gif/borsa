"""
BIST 100 Gunluk Tarama — v5 (Sinyal Takip)
Tum BIST 100 hisseleri taranir. Kriterlere uyan hisselerin listeye
GIRIS tarihi/fiyati, GUNCEL fiyati ve listeden CIKIS tarihi/fiyati izlenir.

Kriterler:
  1) MACD (12-26-9) > Sinyal cizgisi (al kesisimi bolgesi)
  2) RSI (14) > 50
  3) Kapanis > MA5 ve MA9 ve MA21 (SMA)

Kurallar:
  - Giris fiyati  = kriterlerin ILK saglandigi gunun kapanisi
  - Cikis fiyati  = kriterlerin ILK bozuldugu gunun kapanisi
  - Rapor: aktif sinyaller + son 7 gunde listeden cikanlar
  - Cikip tekrar giren hisse YENI pozisyon sayilir

Gecmis veriden her gun yeniden hesaplanir; ayri durum dosyasi gerekmez.

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

CIKANLAR_GUN = 7      # listeden cikanlar kac gun raporda kalsin
MIN_VERI = 60         # bundan az veri varsa hisse atlanir (yeni halka arzlar)

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


def sinyal_serisi(close: pd.Series) -> pd.Series:
    """Her gun icin kriterlerin saglanip saglanmadigini (True/False) doner."""
    close = close.dropna()
    ma5 = close.rolling(5).mean()
    ma9 = close.rolling(9).mean()
    ma21 = close.rolling(21).mean()
    if MACD_MODE == "histogram":
        macd_val = macd_histogram(close)
    else:
        macd_val = macd_line(close)
    rsi_val = rsi(close)

    sinyal = (
        (macd_val > 0)
        & (rsi_val > 50)
        & (close > ma5)
        & (close > ma9)
        & (close > ma21)
    )
    # Ilk 30 bar: gostergeler henuz oturmamis, sinyal sayma
    sinyal.iloc[:30] = False
    return sinyal.fillna(False)


def pozisyonlar(close: pd.Series) -> list[dict]:
    """
    Sinyal serisindeki kesintisiz True bloklarini pozisyonlara cevirir.
    Her blok: giris (ilk True gun) ve varsa cikis (blok sonrasi ilk gun).
    """
    close = close.dropna()
    if len(close) < MIN_VERI:
        return []
    sinyal = sinyal_serisi(close)

    poz = []
    aktif = None
    for i, (tarih, s) in enumerate(sinyal.items()):
        if s and aktif is None:
            aktif = {
                "giris_tarih": tarih,
                "giris_fiyat": float(close.iloc[i]),
                "gun": 1,
            }
        elif s and aktif is not None:
            aktif["gun"] += 1
        elif (not s) and aktif is not None:
            aktif["cikis_tarih"] = tarih
            aktif["cikis_fiyat"] = float(close.iloc[i])
            poz.append(aktif)
            aktif = None
    if aktif is not None:  # hala listede
        aktif["guncel_fiyat"] = float(close.iloc[-1])
        poz.append(aktif)
    return poz


def getiri(giris: float, simdiki: float) -> float:
    return round((simdiki / giris - 1) * 100, 1)


def fmt_tarih(t) -> str:
    return pd.Timestamp(t).strftime("%d.%m.%Y")


def main():
    import json
    from datetime import datetime, timedelta

    print(f"BIST 100 verileri indiriliyor... ({len(TICKERS)} hisse)")
    data = yf.download(
        TICKERS, period="6mo", interval="1d",
        auto_adjust=True, progress=False, group_by="ticker",
    )

    aktifler = []   # su an listede olanlar
    cikanlar = []   # son CIKANLAR_GUN gun icinde cikanlar
    failed = []
    esik = pd.Timestamp(datetime.now() - timedelta(days=CIKANLAR_GUN))

    for t in TICKERS:
        sym = t.replace(".IS", "")
        try:
            close = data[t]["Close"]
            for p in pozisyonlar(close):
                if "guncel_fiyat" in p:  # aktif pozisyon
                    aktifler.append({
                        "hisse": sym,
                        "giris_tarih": p["giris_tarih"],
                        "giris_fiyat": round(p["giris_fiyat"], 2),
                        "guncel_fiyat": round(p["guncel_fiyat"], 2),
                        "getiri": getiri(p["giris_fiyat"], p["guncel_fiyat"]),
                        "gun": p["gun"],
                    })
                elif pd.Timestamp(p["cikis_tarih"]) >= esik:  # yeni cikan
                    cikanlar.append({
                        "hisse": sym,
                        "giris_tarih": p["giris_tarih"],
                        "giris_fiyat": round(p["giris_fiyat"], 2),
                        "cikis_tarih": p["cikis_tarih"],
                        "cikis_fiyat": round(p["cikis_fiyat"], 2),
                        "getiri": getiri(p["giris_fiyat"], p["cikis_fiyat"]),
                        "gun": p["gun"],
                    })
        except Exception:
            failed.append(sym)

    aktifler.sort(key=lambda x: x["getiri"], reverse=True)
    cikanlar.sort(key=lambda x: pd.Timestamp(x["cikis_tarih"]), reverse=True)

    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    baslik = "MACD > Sinyal (al kesisimi), RSI > 50, Fiyat > MA5/MA9/MA21"

    lines_md = [
        f"# BIST 100 Tarama — {tarih}",
        "",
        f"Kriterler: {baslik}",
        f"Taranan: {len(BIST100)} hisse | Listede: {len(aktifler)} "
        f"| Son {CIKANLAR_GUN} gunde cikan: {len(cikanlar)}",
        "",
        f"## 🟢 Aktif Sinyaller ({len(aktifler)})",
        "",
    ]

    if aktifler:
        lines_md.append("| Hisse | Giris Tarihi | Giris Fiyati | Guncel Fiyat | Getiri % | Gun |")
        lines_md.append("|---|---|---|---|---|---|")
        for a in aktifler:
            lines_md.append(
                f"| {a['hisse']} | {fmt_tarih(a['giris_tarih'])} | {a['giris_fiyat']} "
                f"| {a['guncel_fiyat']} | {a['getiri']:+.1f}% | {a['gun']} |"
            )
    else:
        lines_md.append("Su an kriterleri saglayan hisse yok.")

    lines_md += [
        "",
        f"## 🔴 Listeden Cikanlar — Son {CIKANLAR_GUN} Gun ({len(cikanlar)})",
        "",
    ]

    if cikanlar:
        lines_md.append("| Hisse | Giris | Giris F. | Cikis | Cikis F. | Getiri % | Gun |")
        lines_md.append("|---|---|---|---|---|---|---|")
        for c in cikanlar:
            lines_md.append(
                f"| {c['hisse']} | {fmt_tarih(c['giris_tarih'])} | {c['giris_fiyat']} "
                f"| {fmt_tarih(c['cikis_tarih'])} | {c['cikis_fiyat']} "
                f"| {c['getiri']:+.1f}% | {c['gun']} |"
            )
    else:
        lines_md.append(f"Son {CIKANLAR_GUN} gunde listeden cikan hisse yok.")

    lines_md += [
        "",
        "Not: Giris/cikis fiyatlari sinyal gununun kapanisidir; "
        "gercek islem fiyati ertesi gun acilisina gore degisebilir.",
    ]

    if failed:
        lines_md += ["", f"Veri alinamayan: {', '.join(failed)}"]

    # Konsol ozeti
    print(f"\n=== AKTIF SINYALLER ({len(aktifler)}) | SON {CIKANLAR_GUN} GUN CIKAN ({len(cikanlar)}) ===\n")
    for a in aktifler:
        print(f"  {a['hisse']:6s} giris {fmt_tarih(a['giris_tarih'])} @{a['giris_fiyat']} "
              f"-> {a['guncel_fiyat']} ({a['getiri']:+.1f}%)")
    for c in cikanlar:
        print(f"  {c['hisse']:6s} CIKTI {fmt_tarih(c['cikis_tarih'])} @{c['cikis_fiyat']} "
              f"(giris @{c['giris_fiyat']}, {c['getiri']:+.1f}%)")
    if failed:
        print(f"\nVeri alinamayan: {', '.join(failed)}")

    # Dosya ciktilari (GitHub Actions bunlari commit eder)
    import os
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/latest.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines_md) + "\n")

    def _json_poz(p):
        q = dict(p)
        for k in ("giris_tarih", "cikis_tarih"):
            if k in q:
                q[k] = pd.Timestamp(q[k]).strftime("%Y-%m-%d")
        return q

    with open("sonuclar/latest.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "tarih": tarih,
                "kriterler": baslik,
                "taranan_hisse_sayisi": len(BIST100),
                "aktif_sinyaller": [_json_poz(a) for a in aktifler],
                "listeden_cikanlar": [_json_poz(c) for c in cikanlar],
                "veri_alinamayan": failed,
            },
            f, ensure_ascii=False, indent=2, default=float,
        )
    print("\nSonuclar sonuclar/latest.md ve latest.json dosyalarina yazildi.")


if __name__ == "__main__":
    main()
