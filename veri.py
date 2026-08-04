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


def _onbellek_yolu(ad: str, periyot: str, aralik: str) -> str:
    return os.path.join(ONBELLEK_DIZIN, f"{ad}_{periyot}_{aralik}.parquet")


def _indir_parca(semboller: list[str], periyot: str, aralik: str) -> pd.DataFrame:
    """Tek bir sembol grubunu indirir; basarisizsa ustel bekleyip tekrar dener."""
    son_hata = None
    for deneme in range(DENEME):
        try:
            df = yf.download(
                semboller, period=periyot, interval=aralik,
                auto_adjust=True, progress=False, group_by="ticker",
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
               aralik: str = "1d", tazele: bool = False) -> pd.DataFrame:
    """
    Cok sembollu OHLCV cercevesi doner (sutunlar: (sembol, alan)).

    ad     : onbellek dosya adi (orn. "bist100", "sp500")
    tazele : True ise onbellek yok sayilip yeniden indirilir
    """
    yol = _onbellek_yolu(ad, periyot, aralik)
    if not tazele and os.path.exists(yol):
        df = pd.read_parquet(yol)
        print(f"[veri] onbellekten: {yol} ({df.shape[0]} gun, "
              f"{len(set(c[0] for c in df.columns))} sembol)")
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
               tazele: bool = False) -> pd.Series:
    """Tek sembolun kapanis serisi (endeks icin). Ayni onbellek mantigi."""
    yol = _onbellek_yolu(f"tek_{sembol.replace('^', '')}", periyot, aralik)
    if not tazele and os.path.exists(yol):
        return pd.read_parquet(yol)["Close"].dropna()

    os.makedirs(ONBELLEK_DIZIN, exist_ok=True)
    df = _indir_parca([sembol], periyot, aralik)
    if isinstance(df.columns, pd.MultiIndex):
        df = df[sembol] if sembol in df.columns.get_level_values(0) else df.droplevel(0, axis=1)
    df[["Close"]].to_parquet(yol)
    return df["Close"].dropna()


def hisse_cerceve(data: pd.DataFrame, sembol: str) -> pd.DataFrame | None:
    """
    Cok sembollu cerceveden tek hissenin OHLCV'sini cikarir.
    Sembol yoksa veya kapanis tamamen bossa None doner.
    """
    if sembol not in data.columns.get_level_values(0):
        return None
    d = data[sembol].copy()
    for alan in ("Open", "High", "Low", "Close", "Volume"):
        if alan not in d.columns:
            return None
        d[alan] = pd.to_numeric(d[alan], errors="coerce")
    d = d.dropna(subset=["Close"])
    return d if not d.empty else None
