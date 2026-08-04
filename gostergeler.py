"""
Gosterge kutuphanesi.

Tasarim kurallari:
  1) Her fonksiyon Series alir, Series doner. Yeterli veri yoksa NaN kalir;
     NaN karsilastirmasi False verdigi icin sinyal uretmez (guvenli taraf).
  2) GERIYE BAKAN esikler daima shift(1) ile hesaplanir. Aksi halde
     bugunku bar kendi esigini yukseltip kosulu kendiliginden zayiflatir
     (hacim ve Donchian'da klasik hata).
  3) "Seviye" ile "degisim" ayrimi onemlidir: ADX>25 trendin ORTASI,
     ADX yukseliyor + DI kesisimi trendin DOGUSU. Ikisi ayri fonksiyon.
"""

from __future__ import annotations

import pandas as pd


# ---------------------------------------------------------------
# Temel yardimcilar
# ---------------------------------------------------------------
def wilder(s: pd.Series, periyot: int) -> pd.Series:
    """Wilder yumusatmasi (RSI/ADX/ATR ortak)."""
    return s.ewm(alpha=1 / periyot, min_periods=periyot, adjust=False).mean()


def _sayisal(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


# ---------------------------------------------------------------
# Momentum
# ---------------------------------------------------------------
def rsi(close: pd.Series, periyot: int = 14) -> pd.Series:
    delta = close.diff()
    kazanc = wilder(delta.clip(lower=0), periyot)
    kayip = wilder(-delta.clip(upper=0), periyot)
    return 100 - (100 / (1 + kazanc / kayip))


def macd(close: pd.Series, hizli: int = 12, yavas: int = 26,
         sinyal: int = 9) -> tuple[pd.Series, pd.Series, pd.Series]:
    """(macd_cizgisi, sinyal_cizgisi, histogram) doner."""
    cizgi = (close.ewm(span=hizli, adjust=False).mean()
             - close.ewm(span=yavas, adjust=False).mean())
    sig = cizgi.ewm(span=sinyal, adjust=False).mean()
    return cizgi, sig, cizgi - sig


# ---------------------------------------------------------------
# Volatilite
# ---------------------------------------------------------------
def gercek_aralik(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    high, low, close = _sayisal(high), _sayisal(low), _sayisal(close)
    onceki = close.shift()
    return pd.concat(
        [high - low, (high - onceki).abs(), (low - onceki).abs()], axis=1
    ).max(axis=1).where(onceki.notna())


def atr(high: pd.Series, low: pd.Series, close: pd.Series,
        periyot: int = 14) -> pd.Series:
    return wilder(gercek_aralik(high, low, close), periyot)


def dmi(high: pd.Series, low: pd.Series, close: pd.Series,
        periyot: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    """(plus_di, minus_di, adx) doner."""
    high, low, close = _sayisal(high), _sayisal(low), _sayisal(close)
    yukari, asagi = high.diff(), -low.diff()
    # Ilk barda onceki bar yok -> DM tanimsiz. where(...) NaN'i False sayip
    # 0 yazacagi icin acikca maskeleniyor.
    arti_dm = yukari.where((yukari > asagi) & (yukari > 0), 0.0).where(yukari.notna())
    eksi_dm = asagi.where((asagi > yukari) & (asagi > 0), 0.0).where(asagi.notna())

    ort_ta = wilder(gercek_aralik(high, low, close), periyot)
    arti_di = 100 * wilder(arti_dm, periyot) / ort_ta
    eksi_di = 100 * wilder(eksi_dm, periyot) / ort_ta
    dx = 100 * (arti_di - eksi_di).abs() / (arti_di + eksi_di)
    return arti_di, eksi_di, wilder(dx, periyot)


def adx(high: pd.Series, low: pd.Series, close: pd.Series,
        periyot: int = 14) -> pd.Series:
    return dmi(high, low, close, periyot)[2]


def bollinger(close: pd.Series, periyot: int = 20,
              k: float = 2.0) -> tuple[pd.Series, pd.Series, pd.Series]:
    orta = close.rolling(periyot).mean()
    sapma = close.rolling(periyot).std(ddof=0)
    return orta - k * sapma, orta, orta + k * sapma


def bant_genisligi(close: pd.Series, periyot: int = 20, k: float = 2.0) -> pd.Series:
    """Bollinger bant genisligi = (ust - alt) / orta. Sikismanin olcusu."""
    alt, orta, ust = bollinger(close, periyot, k)
    return (ust - alt) / orta


def keltner(high: pd.Series, low: pd.Series, close: pd.Series,
            periyot: int = 20, k: float = 1.5) -> tuple[pd.Series, pd.Series]:
    orta = close.ewm(span=periyot, adjust=False).mean()
    a = atr(high, low, close, periyot)
    return orta - k * a, orta + k * a


# ---------------------------------------------------------------
# Sikisma (TTM Squeeze) — buyuk hareketler daralmadan dogar
# ---------------------------------------------------------------
def sikisma(high: pd.Series, low: pd.Series, close: pd.Series,
            periyot: int = 20, bb_k: float = 2.0, kc_k: float = 1.5) -> pd.Series:
    """Bollinger bantlari Keltner kanalinin ICINDE ise True (sikisma var)."""
    bb_alt, _, bb_ust = bollinger(close, periyot, bb_k)
    kc_alt, kc_ust = keltner(high, low, close, periyot, kc_k)
    return ((bb_alt > kc_alt) & (bb_ust < kc_ust)).where(bb_ust.notna())


def yuzdelik_sira(s: pd.Series, pencere: int = 126) -> pd.Series:
    """
    Her gun icin: deger, son 'pencere' gun icinde hangi yuzdelik dilimde?
    0 = donemin en dusugu, 1 = en yuksegi. BBW'nin dip yapmasini yakalamak icin.
    """
    return s.rolling(pencere).rank(pct=True)


def sikisma_dipte(close: pd.Series, pencere: int = 126,
                  esik: float = 0.10) -> pd.Series:
    """Bant genisligi son 'pencere' gunun en dusuk %esik'lik diliminde mi?"""
    return (yuzdelik_sira(bant_genisligi(close), pencere) <= esik)


def yakin_gecmiste(kosul: pd.Series, gun: int = 10) -> pd.Series:
    """
    Kosul son 'gun' icinde (BUGUN HARIC) en az bir kez saglandi mi?

    Kurulum kriterleri icin sart. Ornek: sikisma ile kirilim ayni gun
    ARANAMAZ — kirilim gunu bantlar tanimi geregi genisler, yani
    "bugun sikisma var" ile "bugun kirilim var" birbirini diser.
    Dogrusu: sikisma yakin GECMISTE vardi, kirilim BUGUN oldu.
    """
    return (kosul.fillna(False).astype(float)
            .shift(1).rolling(gun, min_periods=1).max()
            .fillna(0).astype(bool))


# ---------------------------------------------------------------
# Baz / kirilim
# ---------------------------------------------------------------
def donchian_ust(high: pd.Series, periyot: int = 20) -> pd.Series:
    """
    Onceki 'periyot' gunun en yuksegi — BUGUN HARIC (shift(1)).
    Bugunku bari dahil etmek kirilimi tanimsiz hale getirirdi.
    """
    return _sayisal(high).shift(1).rolling(periyot).max()


def kirilim(close: pd.Series, high: pd.Series, periyot: int = 20) -> pd.Series:
    """Kapanis, onceki 'periyot' gunun en yuksegini asti mi? = hareketin 1. gunu."""
    return close > donchian_ust(high, periyot)


def baz_genisligi(high: pd.Series, low: pd.Series, periyot: int = 20) -> pd.Series:
    """
    Kirilan bazin darligi. (en yuksek - en dusuk) / en dusuk, bugun haric.
    Dar baz (<%10) kaliteli kirilim; genis dalgali baz zayif.
    """
    h = _sayisal(high).shift(1).rolling(periyot).max()
    l = _sayisal(low).shift(1).rolling(periyot).min()
    return (h - l) / l


def zirve_yakinligi(close: pd.Series, periyot: int = 252) -> pd.Series:
    """Fiyat / son 'periyot' gunun zirvesi. 1.0'a yakin = 52 hafta zirvesinde."""
    return close / close.rolling(periyot, min_periods=periyot // 2).max()


# ---------------------------------------------------------------
# Hacim — tek en guclu oncu sinyal
# ---------------------------------------------------------------
def rvol(volume: pd.Series, periyot: int = 20) -> pd.Series:
    """
    Bagil hacim = bugunku hacim / onceki 'periyot' gunun MEDYANI.
    Medyan bilincli tercih: tek bir dev gun ortalamayi sisirip
    sonraki gercek patlamalari gorunmez yapiyor.
    """
    v = _sayisal(volume)
    return v / v.shift(1).rolling(periyot).median()


def hacim_genislemesi(volume: pd.Series, kisa: int = 5,
                      uzun: int = 60) -> pd.Series:
    """Kisa donem ort. hacim / uzun donem ort. hacim. >1.5 = toplama."""
    v = _sayisal(volume)
    return v.rolling(kisa).mean() / v.rolling(uzun).mean()


# ---------------------------------------------------------------
# Gun ici baski
# ---------------------------------------------------------------
def kapanis_konumu(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """(C-L)/(H-L). 1'e yakin = gun boyu alici baskisi, tepede kapanis."""
    h, l, c = _sayisal(high), _sayisal(low), _sayisal(close)
    aralik = h - l
    return ((c - l) / aralik).where(aralik > 0)


def govde_orani(high: pd.Series, low: pd.Series, close: pd.Series,
                periyot: int = 20) -> pd.Series:
    """Gunluk aralik / ATR. >1.5 = normalin cok ustunde hareket."""
    return (_sayisal(high) - _sayisal(low)) / atr(high, low, close, periyot)


# ---------------------------------------------------------------
# Goreli guc — SEVIYE degil DEGISIM
# ---------------------------------------------------------------
def gg_orani(close: pd.Series, endeks: pd.Series) -> pd.Series:
    """Hisse / endeks orani. Yukselen oran = endeksten guclu."""
    return close / endeks.reindex(close.index).ffill()


def gg_kirilimi(close: pd.Series, endeks: pd.Series,
                periyot: int = 20) -> pd.Series:
    """
    GG orani, onceki 'periyot' gunun zirvesini yeni kirdi mi?
    "Son 21 gun getirisi > endeks" (bir aydir kosuyor = gec) yerine
    bunun oncu olmasinin sebebi: GG kirilimi fiyat kirilimindan once gelir.
    """
    oran = gg_orani(close, endeks)
    return oran > oran.shift(1).rolling(periyot).max()


def donem_getirisi(close: pd.Series, periyot: int) -> pd.Series:
    return close / close.shift(periyot) - 1


# ---------------------------------------------------------------
# Trendin DOGUSU (ADX>25'in erken alternatifi)
# ---------------------------------------------------------------
def trend_dogusu(high: pd.Series, low: pd.Series, close: pd.Series,
                 periyot: int = 14, adx_tavan: float = 25.0,
                 yukselis_gun: int = 3) -> pd.Series:
    """
    ADX henuz DUSUK ama YUKSELIYOR ve DI+ > DI-.
    ADX>25 trendin ortasidir (Wilder cift yumusatma ~2x periyot gecikme);
    bu kosul trend olgunlasmadan once tetiklenir.
    """
    arti_di, eksi_di, a = dmi(high, low, close, periyot)
    yukseliyor = a > a.shift(yukselis_gun)
    return (a < adx_tavan) & yukseliyor & (arti_di > eksi_di)


def taze_kesisim(close: pd.Series, kisa: int = 5, uzun: int = 21,
                 gun: int = 3) -> pd.Series:
    """
    MA kesisimi son 'gun' icinde mi oldu?
    "MA5 > MA21" 30 gundur dogru olabilir; bu kosul sadece kesisim
    penceresinde True doner.
    """
    k, u = close.rolling(kisa).mean(), close.rolling(uzun).mean()
    ustunde = k > u
    yeni = ustunde & ~ustunde.shift(1).fillna(False)
    return yeni.rolling(gun, min_periods=1).max().astype(bool) & ustunde
