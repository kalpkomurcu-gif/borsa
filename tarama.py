"""
BIST 100 Gunluk Tarama — v5 (Sinyal Takip)
Tum BIST 100 hisseleri taranir. Kriterlere uyan hisselerin listeye
GIRIS tarihi/fiyati, GUNCEL fiyati ve listeden CIKIS tarihi/fiyati izlenir.

Kriterler:
  1) MACD (12-26-9) > Sinyal cizgisi (al kesisimi bolgesi)
  2) RSI (14) > 50
  3) MA5 > MA21 (SMA) — surekli kosul, hem girise hem kalmaya etki eder
  4) ADX (14) > 25  (trend gucu — varsayilan: her gun aranir)
  5) Hacim > onceki 20 gunun ortalama hacmi  (varsayilan: sadece GIRIS gunu)
  6) Son 20 gunluk baz genisligi < %30  (varsayilan: sadece GIRIS gunu)

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

import gostergeler as G

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

# ---------------------------------------------------------------
# Hacim kosulu (v6)
# ---------------------------------------------------------------
# Karsilastirma penceresi sinyal gununu ICERMEZ (shift(1)); aksi halde
# yuksek hacimli gun kendi esigini yukseltip kosulu zayiflatir.
HACIM_PERIYOT = 20
HACIM_CARPAN = 1.0        # 1.0 = esigin ustunde | 1.5 = %50 fazla hacim iste
HACIM_MODU = "ortalama"   # "ortalama" -> 20 gun ort. | "maksimum" -> 20 gunun en yuksegi

# True  -> hacim SADECE giris gunu aranir, pozisyon MACD/RSI/MA ile devam eder
# False -> hacim her gun aranir; hacim dususte pozisyon listeden cikar
HACIM_SADECE_GIRIS = True

# ---------------------------------------------------------------
# ADX kosulu (v6) — trend gucu
# ---------------------------------------------------------------
ADX_PERIYOT = 14
ADX_ESIK = 25.0

# False -> ADX her gun aranir; trend zayiflayinca pozisyon listeden cikar
#          (RSI/MACD gibi surekli bir kosul; onerilen)
# True  -> ADX sadece giris gunu aranir
ADX_SADECE_GIRIS = False

# ---------------------------------------------------------------
# Baz genisligi kosulu (v7) — dar bazdan cikan kirilim daha temiz
# ---------------------------------------------------------------
# G.baz_genisligi(): (son BAZ_PERIYOT gunun en yuksegi - en dusugu) / en dusuk,
# BUGUN HARIC (shift(1)). Bugunku bar dahil edilseydi kirilim gunu kendi bazini
# genisletip kosulu kendiliginden bozardi — hacimdeki shift(1) ile ayni mantik.
BAZ_PERIYOT = 20
# %18 BIST100'de fazla darmis: 12.08.2026 verisinde tum listeyi 7 hisseden
# 1'e dusuruyor ve o gunun en iyisini (TKFEN +%25.3, baz %54.6) eliyordu.
# %30 ayni gunde 3 hisse birakiyor. Olcum icin bkz. sonuclar/analiz_1208.md
BAZ_ESIK = 30.0           # yuzde

# True  -> baz darligi SADECE giris gunu aranir (onerilen). strateji.py'de de
#          "kurulum" kriteridir: dar baz girisin KOSULU, pozisyonun degil.
#          Kirilimdan sonra bazin genislemesi beklenen davranistir; bu yuzden
#          pozisyon kapatmak kazanan hareketi daha 2. gunde keserdi.
# False -> her gun aranir; baz genisleyince pozisyon listeden cikar.
BAZ_SADECE_GIRIS = True


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


def adx(high: pd.Series, low: pd.Series, close: pd.Series,
        period: int = ADX_PERIYOT) -> pd.Series:
    """
    Wilder ADX. RSI ile ayni yumusatma kullanilir:
    ewm(alpha=1/period, adjust=False).
    Yeterli veri oturmadan NaN doner; NaN karsilastirmasi False verir.
    """
    high = pd.to_numeric(high, errors="coerce")
    low = pd.to_numeric(low, errors="coerce")
    close = pd.to_numeric(close, errors="coerce")

    up = high.diff()
    down = -low.diff()
    # Ilk barda onceki bar yok -> DM/TR tanimsiz (NaN). where(...) kosulu
    # NaN'da False verip 0 yazacagi icin acikca maskeleniyor.
    plus_dm = up.where((up > down) & (up > 0), 0.0).where(up.notna())
    minus_dm = down.where((down > up) & (down > 0), 0.0).where(down.notna())

    onceki_kapanis = close.shift()
    tr = pd.concat(
        [high - low, (high - onceki_kapanis).abs(), (low - onceki_kapanis).abs()],
        axis=1,
    ).max(axis=1).where(onceki_kapanis.notna())

    def wilder(s: pd.Series) -> pd.Series:
        return s.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    atr = wilder(tr)
    plus_di = 100 * wilder(plus_dm) / atr
    minus_di = 100 * wilder(minus_dm) / atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return wilder(dx)


def hacim_kosulu(volume: pd.Series) -> pd.Series:
    """Sinyal gunundeki hacim, onceki HACIM_PERIYOT gunun esigini asiyor mu?"""
    v = pd.to_numeric(volume, errors="coerce")
    onceki = v.shift(1).rolling(HACIM_PERIYOT)
    ref = onceki.max() if HACIM_MODU == "maksimum" else onceki.mean()
    return (v > ref * HACIM_CARPAN).fillna(False)


def sinyal_serisi(close: pd.Series) -> pd.Series:
    """Her gun icin kriterlerin saglanip saglanmadigini (True/False) doner."""
    close = close.dropna()
    ma5 = close.rolling(5).mean()
    ma21 = close.rolling(21).mean()
    if MACD_MODE == "histogram":
        macd_val = macd_histogram(close)
    else:
        macd_val = macd_line(close)
    rsi_val = rsi(close)

    sinyal = (
        (macd_val > 0)
        & (rsi_val > 50)
        & (ma5 > ma21)
    )
    # Ilk 30 bar: gostergeler henuz oturmamis, sinyal sayma
    sinyal.iloc[:30] = False
    return sinyal.fillna(False)


def pozisyonlar(high: pd.Series, low: pd.Series, close: pd.Series,
                volume: pd.Series) -> list[dict]:
    """
    Sinyal serisindeki kesintisiz True bloklarini pozisyonlara cevirir.
    Her blok: giris (ilk True gun) ve varsa cikis (blok sonrasi ilk gun).

    GIRIS  : MACD/RSI/MA + ADX + hacim + baz genisligi kosullarinin tamami.
    DEVAM  : MACD/RSI/MA + "SADECE_GIRIS" bayragi False olan filtreler.
    """
    close = close.dropna()
    if len(close) < MIN_VERI:
        return []
    yuksek = high.reindex(close.index)
    dusuk = low.reindex(close.index)
    temel = sinyal_serisi(close)
    adx_ok = (adx(yuksek, dusuk, close) > ADX_ESIK).fillna(False)
    hacim_ok = hacim_kosulu(volume.reindex(close.index))
    baz_ok = (G.baz_genisligi(yuksek, dusuk, BAZ_PERIYOT) * 100
              < BAZ_ESIK).fillna(False)

    giris_kosulu = temel & adx_ok & hacim_ok & baz_ok
    kalma_kosulu = temel.copy()
    if not ADX_SADECE_GIRIS:
        kalma_kosulu &= adx_ok
    if not HACIM_SADECE_GIRIS:
        kalma_kosulu &= hacim_ok
    if not BAZ_SADECE_GIRIS:
        kalma_kosulu &= baz_ok

    poz = []
    aktif = None
    for i, tarih in enumerate(close.index):
        girebilir = bool(giris_kosulu.iloc[i])
        kalabilir = bool(kalma_kosulu.iloc[i])
        if aktif is None and girebilir:
            aktif = {
                "giris_tarih": tarih,
                "giris_fiyat": float(close.iloc[i]),
                "gun": 1,
            }
        elif aktif is not None and kalabilir:
            aktif["gun"] += 1
        elif aktif is not None and not kalabilir:
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
            for p in pozisyonlar(data[t]["High"], data[t]["Low"], close,
                                 data[t]["Volume"]):
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
    _hacim_ref = (
        f"son {HACIM_PERIYOT} gunun "
        f"{'en yuksek' if HACIM_MODU == 'maksimum' else 'ortalama'} hacmi"
    )
    _hacim_carpan = "" if HACIM_CARPAN == 1.0 else f" x{HACIM_CARPAN:g}"
    _hacim_kapsam = "giriste" if HACIM_SADECE_GIRIS else "her gun"
    _adx_kapsam = "giriste" if ADX_SADECE_GIRIS else "her gun"
    _baz_kapsam = "giriste" if BAZ_SADECE_GIRIS else "her gun"
    baslik = (
        "MACD > Sinyal (al kesisimi), RSI > 50, MA5 > MA21, "
        f"ADX({ADX_PERIYOT}) > {ADX_ESIK:g} ({_adx_kapsam}), "
        f"Hacim > {_hacim_ref}{_hacim_carpan} ({_hacim_kapsam}), "
        f"Son {BAZ_PERIYOT} gunluk baz genisligi < %{BAZ_ESIK:g} ({_baz_kapsam})"
    )

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
