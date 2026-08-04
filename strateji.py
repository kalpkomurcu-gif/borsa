"""
Strateji tanimi — KURULUM / TETIK / KALMA ayrimi.

Eski kodun yapisal sorunu: 5 kriter tek bir `&` yiginindaydi ve hepsi
onay (confirmation) gostergesiydi. AND'lenince giris gunu her zaman EN GEC
kriterin gunu olur — pratikte ADX(14)>25 ve "21 gun getirisi > endeks"
belirliyordu, ikisi de hareketin ~2-4 hafta gerisinde tetikleniyor.

Burada kriterler uc role ayrilir:

  KURULUM (setup)  : "Bu hisse hareket etmeye HAZIR mi?"  — durum.
                     Sikisma, dar baz, hacim toplama, zirveye yakinlik.
                     Gunlerce True kalabilir; tek basina alim emri degildir.

  TETIK (trigger)  : "Hareket BUGUN basladi mi?" — olay.
                     Baz kirilimi, hacim patlamasi, tepede kapanis.
                     Tanimi geregi tek gunluk; hareketin 1. gunudur.

  KALMA (stay)     : "Pozisyonda kalmaya devam?" — sadece cikisi ilgilendirir.
                     Girise ETKI ETMEZ; bu ayrim olmadan yavas bir kalma
                     kosulu girisi de geciktiriyordu.

  SUREKLI (both)   : Hem girisi hem kalmayi kapayan kosul. Eski sistemin
                     MACD/RSI/MA/ADX kriterleri boyleydi — baseline'i
                     durust kurmak icin bu tip sart.

Giris = tum KURULUM + TETIK + SUREKLI ayni gun True.
Cikis = KALMA/SUREKLI bozulmasi VEYA ATR bazli stop VEYA sure asimi.

Kriterler isimli nesneler oldugu icin olcum.py tek tek cikarip
katkisini olcebilir (ablasyon).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import pandas as pd

import gostergeler as G

# Kriter fonksiyonu imzasi: (ohlcv, endeks_kapanis|None) -> bool Series
KriterFn = Callable[[pd.DataFrame, pd.Series | None], pd.Series]


@dataclass(frozen=True)
class Kriter:
    ad: str
    tip: str                 # "kurulum" | "tetik" | "kalma" | "surekli"
    fn: KriterFn
    aciklama: str = ""
    endeks_ister: bool = False

    TIPLER = ("kurulum", "tetik", "kalma", "surekli")

    def __post_init__(self):
        if self.tip not in Kriter.TIPLER:
            raise ValueError(
                f"{self.ad}: gecersiz tip {self.tip!r} "
                f"(gecerli: {', '.join(Kriter.TIPLER)})")


@dataclass(frozen=True)
class Cikis:
    """
    Cikis kurallari.

    atr_carpan     : baslangic stop = giris - carpan * ATR(giris gunu).
                     Sabit yuzde stop yerine ATR: BIST'te tipik gunluk ATR
                     %3-5, sabit -%4 stop gurultu seviyesinde kaliyordu.
    iz_suren       : True ise stop, giristen sonraki en yuksek kapanisa gore
                     yukselir (asla dusmez). Kazandiran islemi kosturmak icin.
    kriter_bozulunca: KALMA kriterleri bozulunca cik.
    max_gun        : bu kadar gun sonra kosulsuz cik (None = sinirsiz).
    """
    atr_carpan: float | None = 2.0
    atr_periyot: int = 20
    iz_suren: bool = True
    kriter_bozulunca: bool = True
    max_gun: int | None = None


@dataclass
class Strateji:
    ad: str
    kriterler: list[Kriter] = field(default_factory=list)
    cikis: Cikis = field(default_factory=Cikis)

    def alt_kume(self, tip: str) -> list[Kriter]:
        return [k for k in self.kriterler if k.tip == tip]

    def haric(self, ad: str) -> "Strateji":
        """Tek kriteri cikarilmis kopya — ablasyon icin."""
        return Strateji(
            ad=f"{self.ad} (-{ad})",
            kriterler=[k for k in self.kriterler if k.ad != ad],
            cikis=self.cikis,
        )

    def endeks_ister(self) -> bool:
        return any(k.endeks_ister for k in self.kriterler)


# ---------------------------------------------------------------
# Seri hesaplama
# ---------------------------------------------------------------
def _birlestir(kriterler: list[Kriter], d: pd.DataFrame,
               endeks: pd.Series | None) -> pd.Series:
    """Kriterleri AND'ler. Hic kriter yoksa hepsi True."""
    sonuc = pd.Series(True, index=d.index)
    for k in kriterler:
        if k.endeks_ister and endeks is None:
            raise ValueError(f"{k.ad} endeks verisi istiyor ama verilmedi")
        seri = k.fn(d, endeks)
        # NaN -> False: gosterge oturmadan sinyal uretme (guvenli taraf)
        sonuc &= seri.reindex(d.index).fillna(False).astype(bool)
    return sonuc


def giris_serisi(s: Strateji, d: pd.DataFrame,
                 endeks: pd.Series | None = None) -> pd.Series:
    return _birlestir(
        s.alt_kume("kurulum") + s.alt_kume("tetik") + s.alt_kume("surekli"),
        d, endeks)


def kalma_serisi(s: Strateji, d: pd.DataFrame,
                 endeks: pd.Series | None = None) -> pd.Series:
    return _birlestir(s.alt_kume("kalma") + s.alt_kume("surekli"), d, endeks)


# ---------------------------------------------------------------
# Pozisyon uretimi
# ---------------------------------------------------------------
MIN_VERI = 60   # bundan az bari olan hisse atlanir (yeni halka arzlar)


def pozisyonlar(s: Strateji, d: pd.DataFrame,
                endeks: pd.Series | None = None) -> list[dict]:
    """
    Stratejiyi tek hissede calistirir, islem listesi doner.

    Fiyatlar kapanistir. Stop "bu seviyeyi ILK goren kapanista cik"
    demektir; gap ile acilan sert dususte gerceklesen zarar bundan
    daha kotu olur. Bu, kapanis verisiyle backtestin kacinilmaz
    iyimserligidir — sonuclari okurken akilda tutulmali.
    """
    d = d.dropna(subset=["Close"])
    if len(d) < MIN_VERI:
        return []

    close = d["Close"]
    girebilir = giris_serisi(s, d, endeks)
    kalabilir = kalma_serisi(s, d, endeks)
    a = (G.atr(d["High"], d["Low"], close, s.cikis.atr_periyot)
         if s.cikis.atr_carpan else None)

    islemler: list[dict] = []
    aktif: dict | None = None

    for i, tarih in enumerate(d.index):
        fiyat = float(close.iloc[i])

        if aktif is None:
            if bool(girebilir.iloc[i]):
                atr_giris = float(a.iloc[i]) if a is not None else float("nan")
                aktif = {
                    "giris_tarih": tarih,
                    "giris_fiyat": fiyat,
                    "atr_giris": atr_giris,
                    "stop": (fiyat - s.cikis.atr_carpan * atr_giris
                             if a is not None and atr_giris == atr_giris else None),
                    "en_yuksek": fiyat,
                    "gun": 1,
                }
            continue

        # Iz suren stop: yeni zirvede yukari cekilir, asla asagi inmez.
        if fiyat > aktif["en_yuksek"]:
            aktif["en_yuksek"] = fiyat
            if s.cikis.iz_suren and aktif["stop"] is not None:
                yeni = fiyat - s.cikis.atr_carpan * aktif["atr_giris"]
                aktif["stop"] = max(aktif["stop"], yeni)

        sebep = None
        if aktif["stop"] is not None and fiyat <= aktif["stop"]:
            sebep = "STOP"
        elif s.cikis.max_gun is not None and aktif["gun"] >= s.cikis.max_gun:
            sebep = "SURE"
        elif s.cikis.kriter_bozulunca and not bool(kalabilir.iloc[i]):
            sebep = "KRITER"

        if sebep is None:
            aktif["gun"] += 1
            continue

        aktif.update(cikis_tarih=tarih, cikis_fiyat=fiyat, sebep=sebep)
        islemler.append(aktif)
        aktif = None

    if aktif is not None:
        aktif.update(guncel_fiyat=float(close.iloc[-1]), sebep="ACIK")
        islemler.append(aktif)
    return islemler


# ===============================================================
# Hazir kriterler
# ===============================================================
# --- Eski sistemin kriterleri (referans/baseline icin) ---------
# Hepsi "surekli": orijinal kodda bu kosullar hem girisi hem kalmayi
# kapiyordu. Sadece "kalma" isaretlemek baseline'i kusursuz gosterip
# karsilastirmayi anlamsiz kilardi.
K_MACD = Kriter(
    "macd", "surekli",
    lambda d, e: G.macd(d["Close"])[2] > 0,
    "MACD histogrami > 0 (MACD > sinyal cizgisi)")

K_RSI50 = Kriter(
    "rsi50", "surekli",
    lambda d, e: G.rsi(d["Close"]) > 50,
    "RSI(14) > 50")

K_MA_USTU = Kriter(
    "ma_ustu", "surekli",
    lambda d, e: ((d["Close"] > d["Close"].rolling(5).mean())
                  & (d["Close"] > d["Close"].rolling(9).mean())
                  & (d["Close"] > d["Close"].rolling(21).mean())),
    "Fiyat > MA5 ve MA9 ve MA21")

K_ADX25 = Kriter(
    "adx25", "surekli",
    lambda d, e: G.adx(d["High"], d["Low"], d["Close"]) > 25,
    "ADX(14) > 25 — GEC: Wilder cift yumusatma ~2x14 bar gecikme")

K_HACIM_ORT = Kriter(
    "hacim_ort", "tetik",
    lambda d, e: d["Volume"] > d["Volume"].shift(1).rolling(20).mean(),
    "Hacim > onceki 20 gun ortalamasi — zayif filtre, gunlerin ~%40'i gecer")

K_GG_SEVIYE = Kriter(
    "gg_seviye", "tetik",
    lambda d, e: (G.donem_getirisi(d["Close"], 21)
                  > G.donem_getirisi(e.reindex(d.index).ffill(), 21)),
    "Son 21 gun getirisi > endeks — GEC: bir aydir zaten kosuyor",
    endeks_ister=True)

# --- Erken giris kriterleri ------------------------------------
# KURULUM: hisse hareket etmeye hazir mi?
K_SIKISMA = Kriter(
    "sikisma", "kurulum",
    lambda d, e: G.yakin_gecmiste(
        G.sikisma_dipte(d["Close"], pencere=126, esik=0.25), gun=10),
    "Son 10 gun icinde sikisma vardi (bant genisligi 6 ayin en dusuk %25'i)")

K_DAR_BAZ = Kriter(
    "dar_baz", "kurulum",
    lambda d, e: G.baz_genisligi(d["High"], d["Low"], 20) < 0.18,
    "Son 20 gunluk baz genisligi < %18 — dar baz kaliteli kirilim verir")

K_HACIM_TOPLAMA = Kriter(
    "hacim_toplama", "kurulum",
    lambda d, e: G.hacim_genislemesi(d["Volume"], 5, 60) > 1.2,
    "5 gun ort. hacim / 60 gun ort. hacim > 1.2 — sessiz toplama")

K_ZIRVEYE_YAKIN = Kriter(
    "zirveye_yakin", "kurulum",
    lambda d, e: G.zirve_yakinligi(d["Close"], 252) > 0.80,
    "Fiyat 52 hafta zirvesinin %80'i uzerinde")

# TETIK: hareket bugun basladi mi?
K_KIRILIM = Kriter(
    "kirilim", "tetik",
    lambda d, e: G.kirilim(d["Close"], d["High"], 20),
    "Kapanis > onceki 20 gunun en yuksegi — tanimi geregi hareketin 1. gunu")

K_RVOL2 = Kriter(
    "rvol2", "tetik",
    lambda d, e: G.rvol(d["Volume"], 20) > 2.0,
    "Hacim, onceki 20 gun medyaninin 2 katindan fazla")

K_TEPEDE_KAPANIS = Kriter(
    "tepede_kapanis", "tetik",
    lambda d, e: G.kapanis_konumu(d["High"], d["Low"], d["Close"]) > 0.7,
    "Kapanis gunun araliginin ust %30'unda — gun boyu alici baskisi")

K_GG_KIRILIM = Kriter(
    "gg_kirilim", "tetik",
    lambda d, e: G.gg_kirilimi(d["Close"], e, 20),
    "Goreli guc orani 20 gunun zirvesini kirdi — fiyat kirilimindan once gelir",
    endeks_ister=True)

K_TREND_DOGUSU = Kriter(
    "trend_dogusu", "tetik",
    lambda d, e: G.trend_dogusu(d["High"], d["Low"], d["Close"]),
    "ADX dusuk ama yukseliyor + DI+ > DI- — ADX>25'in erken alternatifi")

# KALMA: gevsek trend kosullari (girisi geciktirmez)
K_KALMA_MA21 = Kriter(
    "kalma_ma21", "kalma",
    lambda d, e: d["Close"] > d["Close"].rolling(21).mean(),
    "Fiyat MA21 uzerinde")

K_KALMA_MA10 = Kriter(
    "kalma_ma10", "kalma",
    lambda d, e: d["Close"] > d["Close"].rolling(10).mean(),
    "Fiyat MA10 uzerinde")


# ===============================================================
# Hazir stratejiler
# ===============================================================
def mevcut_sistem() -> Strateji:
    """
    son_sinyaller.py'nin kriterleri — KARSILASTIRMA TABANI.
    Amaci iyi calismak degil, yeni sistemin neye gore olculdugunu
    sabitlemek. Cikis da eskisi gibi: sabit -%4, iz suren yok.
    """
    return Strateji(
        ad="mevcut",
        kriterler=[K_MACD, K_RSI50, K_ADX25, K_HACIM_ORT, K_GG_SEVIYE,
                   Kriter("ma5_ma21", "surekli",
                          lambda d, e: (d["Close"].rolling(5).mean()
                                        > d["Close"].rolling(21).mean()),
                          "MA5 > MA21")],
        cikis=Cikis(atr_carpan=None, iz_suren=False, kriter_bozulunca=True),
    )


def erken_giris() -> Strateji:
    """
    Kurulum + tetik mimarisi. Amac: hareketin 1. gununde girmek.

    Bunun bedeli acikca kabul edilmistir: erken giris ISABET ORANINI
    DUSURUR (kirilimlarin cogu basarisiz olur). Karsiliginda R:R duzelir —
    bazin hemen ustunden girilir, stop bazin altina konur, kazanan islem
    iz suren stop ile kosturulur. Sistem "cok kazanan" degil
    "kazananlari buyuk" olmak uzerine kurulu.
    """
    return Strateji(
        ad="erken",
        kriterler=[
            K_SIKISMA, K_DAR_BAZ, K_ZIRVEYE_YAKIN,      # kurulum
            K_KIRILIM, K_RVOL2, K_TEPEDE_KAPANIS,       # tetik
            K_KALMA_MA21,                                # kalma
        ],
        cikis=Cikis(atr_carpan=2.0, iz_suren=True, kriter_bozulunca=True),
    )
