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

import os
import time

import pandas as pd
import yfinance as yf

ONBELLEK_DIZIN = os.environ.get("BORSA_ONBELLEK", ".onbellek")

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


def veri_getir(semboller: list[str], ad: str, periyot: str = "2y",
               aralik: str = "1d", tazele: bool = False,
               azami_yas_saat: float | None = AZAMI_YAS_SAAT) -> pd.DataFrame:
    """
    Cok sembollu OHLCV cercevesi doner (sutunlar: (sembol, alan)).

    ad             : onbellek dosya adi (orn. "bist100", "sp500")
    tazele         : True ise onbellek yok sayilip yeniden indirilir
    azami_yas_saat : onbellek bundan eskiyse yeniden indirilir.
                     None = yas kontrolu yok (backtest icin uygun;
                     gunluk tarama icin DEGIL).
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
    df.to_parquet(yol)
    print(f"[veri] yazildi: {yol} ({df.shape[0]} gun)")
    if basarisiz:
        print(f"[veri] alinamayan {len(basarisiz)}: {', '.join(basarisiz)}")
    return df


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
