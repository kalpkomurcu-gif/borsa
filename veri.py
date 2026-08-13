"""
Veri katmani — indirme + diskte onbellek.

Yahoo 100 hisselik tek istekte sik sik throttle ediyor; ayrica her
denemede yeniden indirmek iterasyonu imkansiz kiliyor. Bu yuzden:
  - kucuk gruplar halinde indirilir (PARCA_BOYU),
  - basarisiz grup ustel bekleme ile tekrar denenir,
  - sonuc parquet olarak ONBELLEK_DIZIN altina yazilir,
  - ayni (evren, periyot) icin ikinci cagri diskten okur.

Onbellegi tazelemek icin: veri_getir(..., tazele=True)
veya ONBELLEK_DIZIN altindaki dosyayi sil.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

ONBELLEK_DIZIN = os.environ.get("BORSA_ONBELLEK", ".onbellek")

BORSA_SAAT_DILIMI = ZoneInfo("Europe/Istanbul")

PARCA_BOYU = 15        # tek istekte kac sembol
DENEME = 4             # parca basina deneme sayisi
BEKLE = 2.0            # ilk bekleme (saniye); her denemede iki katina cikar
PARCALAR_ARASI = 1.0   # ardisik parcalar arasi nezaket beklemesi

# Onbellek bu saatten eskiyse yok sayilip yeniden indirilir.
# Dosya adinda tarih olmadigi icin bu kontrol olmadan ikinci calistirma
# sessizce DUNKU fiyatlari guncelmis gibi kullaniyordu.
AZAMI_YAS_SAAT = 8.0

# auto_adjust=False bilincli tercih. Duzeltilmis (adjusted) fiyat
# gostergeler icin dogrudur — bolunme/bedelsiz suregi bozmaz — ama
# EKRANDA gosterilecek fiyat aracı kurumdaki fiyat olmalidir; ikisi
# temettu/bedelsiz sonrasi birbirinden ayrilir. Bu yuzden ham OHLC ve
# Adj Close birlikte saklanir: gostergeler duzeltilmisi, tablo hamı
# kullanir (bkz. hisse_cerceve(duzeltilmis=...)).
OTO_DUZELT = False

# Yahoo bazi gunlerde gunluk barin OHLC ve HACMINI dogru veriyor ama
# KAPANIS alanini bos birakiyor (Adj Close de bos gelir). Bar var, kapanis
# yok. Gozlenen kalip: kapanis seans sirasinda canli fiyattan doluyor,
# seans kapandiktan bir sure sonra null'a dusuyor, ertesi gun icinde geri
# doluyor. Akşam 18:40'taki zamanlanmis tarama bu delige denk gelmiyor,
# ertesi sabah elle calistirilan tarama denk geliyor.
#
# Kapanis aslinda kaybolmuyor: chart meta'sindaki regularMarketPrice
# alaninda o seansin gerceklesmis kapanisi duruyor. Buradan tamamlanir.
YAHOO_CHART = ("https://query1.finance.yahoo.com/v8/finance/chart/{}"
               "?range=5d&interval=1d")
META_ZAMAN_ASIMI = 15   # saniye
META_ARASI = 0.3        # ardisik meta istekleri arasi nezaket beklemesi


def _onbellek_yolu(ad: str, periyot: str, aralik: str) -> str:
    return os.path.join(ONBELLEK_DIZIN, f"{ad}_{periyot}_{aralik}.parquet")


def _bayat(yol: str, azami_yas_saat: float) -> bool:
    """Onbellek dosyasi cok mu eski?"""
    if azami_yas_saat is None:
        return False
    yas = (time.time() - os.path.getmtime(yol)) / 3600
    return yas > azami_yas_saat


def _indir_parca(semboller: list[str], periyot: str, aralik: str) -> pd.DataFrame:
    """Tek bir sembol grubunu indirir; basarisizsa ustel bekleyip tekrar dener."""
    son_hata = None
    for deneme in range(DENEME):
        try:
            df = yf.download(
                semboller, period=periyot, interval=aralik,
                auto_adjust=OTO_DUZELT, progress=False, group_by="ticker",
                threads=False,
            )
            if df is not None and not df.empty:
                return df
            son_hata = "bos cerceve"
        except Exception as exc:
            son_hata = f"{type(exc).__name__}: {exc}"
        if deneme < DENEME - 1:
            time.sleep(BEKLE * (2 ** deneme))
    raise RuntimeError(f"{len(semboller)} sembol indirilemedi ({son_hata})")


def son_seans_kapanisi(sembol: str) -> tuple[pd.Timestamp, float] | None:
    """
    Yahoo chart meta'sindan son GERCEKLESMIS seansin (gun, kapanis) ikilisi.

    yfinance katmanindan bagimsizdir; gunluk barin kapanisi bos gelse bile
    meta doludur. Ulasilamazsa None doner — cagiran taraf yamama yapmaz.
    """
    try:
        istek = urllib.request.Request(
            YAHOO_CHART.format(sembol), headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(istek, timeout=META_ZAMAN_ASIMI) as y:
            meta = json.load(y)["chart"]["result"][0]["meta"]
    except Exception:
        return None

    zaman, fiyat = meta.get("regularMarketTime"), meta.get("regularMarketPrice")
    if zaman is None or fiyat is None:
        return None
    try:
        fiyat = float(fiyat)
    except (TypeError, ValueError):
        return None
    if not (fiyat > 0):
        return None

    tz = meta.get("exchangeTimezoneName") or "Europe/Istanbul"
    gun = pd.Timestamp(zaman, unit="s", tz=tz).normalize().tz_localize(None)
    return gun, fiyat


def eksik_kapanislari_tamamla(df: pd.DataFrame,
                              semboller: list[str]) -> tuple[list[str], list[str]]:
    """
    Son barin kapanisi bos olan sembolleri meta'daki kapanistan tamamlar.

    (tamamlanan, tamamlanamayan) doner. Sadece SON bara dokunur; gecmis
    barlarin eksigi meta'dan kapatilamaz (meta yalnizca son seansi bilir).

    Uc guvenlik siniri var, ucu de yanlis fiyat enjekte etmemek icin:
      1. Bar tarihi bugunse hicbir sey yapilmaz. Seans suruyorsa meta
         fiyati KAPANIS degil canli fiyattir; yarim bari tamamlanmis gibi
         gostermek en tehlikeli hata olurdu (bkz. gunluk.son_bar_tamamlandi_mi).
      2. Barin Open/High/Low'u da bossa o hisse o gun islem gormemis
         demektir; bar uydurulmaz, sadece kapanisi eksik olan tamamlanir.
      3. Meta gunu barin gunuyle ayni degilse, ya da meta fiyati barin
         dip-tepe araligina sigmiyorsa yamanmaz. Bu, farkli bir seansin
         fiyatini o gunun kapanisi diye yazmayi engeller.
    """
    if df.empty or not isinstance(df.columns, pd.MultiIndex):
        return [], []

    son = df.index[-1]
    bugun = pd.Timestamp.now(tz=BORSA_SAAT_DILIMI).normalize().tz_localize(None)
    if pd.Timestamp(son).normalize() >= bugun:      # (1) suren seans
        return [], []

    tamamlanan, kalan = [], []
    for sembol in semboller:
        if sembol not in df.columns.get_level_values(0):
            continue
        sutunlar = df[sembol]
        if "Close" not in sutunlar.columns:
            continue
        kapanis = pd.to_numeric(sutunlar["Close"], errors="coerce").iloc[-1]
        if kapanis == kapanis:                      # zaten dolu
            continue

        aralik = {}
        for alan in ("Open", "High", "Low"):
            if alan not in sutunlar.columns:
                break
            aralik[alan] = pd.to_numeric(
                sutunlar[alan], errors="coerce").iloc[-1]
        if len(aralik) < 3 or any(v != v for v in aralik.values()):
            kalan.append(sembol)                    # (2) bar gercekten yok
            continue

        sonuc = son_seans_kapanisi(sembol)
        time.sleep(META_ARASI)
        if sonuc is None:
            kalan.append(sembol)
            continue
        gun, fiyat = sonuc
        if (gun != pd.Timestamp(son).normalize()
                or not aralik["Low"] <= fiyat <= aralik["High"]):
            kalan.append(sembol)                    # (3) fiyat bu bara ait degil
            continue

        df.iloc[-1, df.columns.get_loc((sembol, "Close"))] = fiyat
        if (sembol, "Adj Close") in df.columns:
            # En yeni barda duzeltme carpani 1'dir: o barin ardindan henuz
            # temettu/bolunme olmadi, dolayisiyla Adj Close = Close.
            df.iloc[-1, df.columns.get_loc((sembol, "Adj Close"))] = fiyat
        tamamlanan.append(sembol)

    return tamamlanan, kalan


def veri_getir(semboller: list[str], ad: str, periyot: str = "2y",
               aralik: str = "1d", tazele: bool = False,
               azami_yas_saat: float | None = AZAMI_YAS_SAAT,
               eksik_tamamla: bool = False) -> pd.DataFrame:
    """
    Cok sembollu OHLCV cercevesi doner (sutunlar: (sembol, alan)).

    ad             : onbellek dosya adi (orn. "bist100", "sp500")
    tazele         : True ise onbellek yok sayilip yeniden indirilir
    azami_yas_saat : onbellek bundan eskiyse yeniden indirilir.
                     None = yas kontrolu yok (backtest icin uygun;
                     gunluk tarama icin DEGIL).
    eksik_tamamla  : son barin bos kapanislari meta'dan tamamlansin mi.
                     GUNLUK TARAMA icin True. Backtest'te False kalmali:
                     sembol basina bir HTTP istegi demek ve gecmis
                     barlara zaten faydasi yok.
    """
    yol = _onbellek_yolu(ad, periyot, aralik)
    if not tazele and os.path.exists(yol):
        if _bayat(yol, azami_yas_saat):
            yas = (time.time() - os.path.getmtime(yol)) / 3600
            print(f"[veri] onbellek bayat ({yas:.1f} saat > "
                  f"{azami_yas_saat} saat), yeniden indiriliyor")
        else:
            df = pd.read_parquet(yol)
            son = pd.Timestamp(df.index[-1]).date() if len(df.index) else "?"
            print(f"[veri] onbellekten: {yol} ({df.shape[0]} gun, "
                  f"{len(set(c[0] for c in df.columns))} sembol, "
                  f"son veri gunu: {son})")
            if eksik_tamamla:
                _tamamla_ve_bildir(df, semboller)
            return df

    os.makedirs(ONBELLEK_DIZIN, exist_ok=True)
    parcalar, basarisiz = [], []
    toplam = (len(semboller) + PARCA_BOYU - 1) // PARCA_BOYU

    for i in range(0, len(semboller), PARCA_BOYU):
        grup = semboller[i:i + PARCA_BOYU]
        no = i // PARCA_BOYU + 1
        try:
            parcalar.append(_indir_parca(grup, periyot, aralik))
            print(f"[veri] parca {no}/{toplam} tamam ({len(grup)} sembol)")
        except RuntimeError as exc:
            basarisiz.extend(grup)
            print(f"[veri] parca {no}/{toplam} BASARISIZ — {exc}")
        time.sleep(PARCALAR_ARASI)

    if not parcalar:
        raise SystemExit("HATA: hicbir parca indirilemedi.")

    df = pd.concat(parcalar, axis=1).sort_index()
    if eksik_tamamla:
        _tamamla_ve_bildir(df, semboller)
    df.to_parquet(yol)
    print(f"[veri] yazildi: {yol} ({df.shape[0]} gun)")
    if basarisiz:
        print(f"[veri] alinamayan {len(basarisiz)}: {', '.join(basarisiz)}")
    return df


def _tamamla_ve_bildir(df: pd.DataFrame, semboller: list[str]) -> None:
    """eksik_kapanislari_tamamla() + ne yapildigini logla."""
    tamamlanan, kalan = eksik_kapanislari_tamamla(df, semboller)
    if tamamlanan:
        son = pd.Timestamp(df.index[-1])
        print(f"[veri] {son:%Y-%m-%d} barinda kapanisi bos olan "
              f"{len(tamamlanan)} sembol meta'daki gerceklesmis kapanistan "
              f"tamamlandi")
    if kalan:
        print(f"[veri] kapanisi tamamlanamayan {len(kalan)}: "
              f"{', '.join(kalan[:15])}{' ...' if len(kalan) > 15 else ''}")


def tek_sembol(sembol: str, periyot: str = "2y", aralik: str = "1d",
               tazele: bool = False,
               azami_yas_saat: float | None = AZAMI_YAS_SAAT) -> pd.Series:
    """Tek sembolun kapanis serisi (endeks icin). Ayni onbellek mantigi."""
    yol = _onbellek_yolu(f"tek_{sembol.replace('^', '')}", periyot, aralik)
    if not tazele and os.path.exists(yol) and not _bayat(yol, azami_yas_saat):
        return pd.read_parquet(yol)["Close"].dropna()

    os.makedirs(ONBELLEK_DIZIN, exist_ok=True)
    df = _indir_parca([sembol], periyot, aralik)
    if isinstance(df.columns, pd.MultiIndex):
        df = df[sembol] if sembol in df.columns.get_level_values(0) else df.droplevel(0, axis=1)
    # Endeks icin duzeltilmis kapanis: goreli guc ve rejim hesaplarinda
    # sureklilik gerekiyor.
    kapanis = df["Adj Close"] if "Adj Close" in df.columns else df["Close"]
    pd.DataFrame({"Close": kapanis}).to_parquet(yol)
    return kapanis.dropna()


def hisse_cerceve(data: pd.DataFrame, sembol: str,
                  duzeltilmis: bool = True) -> pd.DataFrame | None:
    """
    Cok sembollu cerceveden tek hissenin OHLCV'sini cikarir.
    Sembol yoksa veya kapanis tamamen bossa None doner.

    duzeltilmis=True  (varsayilan, GOSTERGELER icin):
        OHLC, Adj Close / Close oraniyla olceklenir. Bolunme ve bedelsiz
        seriyi kirmaz — bunlar duzeltilmezse MA/ATR/kirilim hesaplari
        tamamen bozulur.

    duzeltilmis=False (TABLODA GOSTERILECEK fiyat icin):
        Ham fiyat. Kullanicinin aracı kurum ekraninda gordugu sayi budur.
        Duzeltilmis fiyat temettu/bedelsiz sonrasi bundan ayrilir; ekranda
        onu gostermek "fiyatlar yanlis" demenin en yaygin sebebidir.
    """
    if sembol not in data.columns.get_level_values(0):
        return None
    d = data[sembol].copy()
    for alan in ("Open", "High", "Low", "Close", "Volume"):
        if alan not in d.columns:
            return None
        d[alan] = pd.to_numeric(d[alan], errors="coerce")

    if duzeltilmis and "Adj Close" in d.columns:
        ham_kapanis = d["Close"]
        duzeltilmis_kapanis = pd.to_numeric(d["Adj Close"], errors="coerce")
        oran = (duzeltilmis_kapanis / ham_kapanis).where(ham_kapanis > 0)
        for alan in ("Open", "High", "Low", "Close"):
            d[alan] = d[alan] * oran

    d = d.dropna(subset=["Close"])
    return d if not d.empty else None
