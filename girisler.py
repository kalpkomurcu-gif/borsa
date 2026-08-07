"""
Son N gunde sinyale GIREN hisseler — tarama.py kriterleriyle.

son_sinyaller.py'den farki: o dosyanin kendine ait DENEME kriterleri var
(MA5>MA21, zarar kes, goreli guc, yukari gun sarti). Bu dosya ise
tarama.py'nin pozisyonlar() fonksiyonunu oldugu gibi cagirir, yani
sonuclar/latest.md ile BIREBIR ayni kriter setini kullanir —
yeni eklenen "son 21 gun getirisi < %10" tavani dahil.

Ayrica tavan KAPALIYKEN de ayni tarama kosturulur; boylece filtrenin
hangi girisleri eledigi acikca gorunur. Filtrenin ne yaptigini
gormeden esik ayarlamak (%10 mu %15 mi) korlemesine olur.

Kullanim: python girisler.py [gun_sayisi]   (varsayilan 20)
"""

import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

import tarama as T

GUN = int(sys.argv[1]) if len(sys.argv) > 1 else 20


def girisleri_topla(data, esik: pd.Timestamp) -> tuple[list[dict], list[str]]:
    """pozisyonlar()'i her hisse icin calistirip esik sonrasi girisleri doner."""
    kayitlar, basarisiz = [], []
    for t in T.TICKERS:
        sym = t.replace(".IS", "")
        try:
            d = data[t]
            if d["Close"].dropna().empty:
                basarisiz.append(sym)
                continue
            for p in T.pozisyonlar(d["High"], d["Low"], d["Close"], d["Volume"]):
                if pd.Timestamp(p["giris_tarih"]).normalize() < esik:
                    continue
                acik = "guncel_fiyat" in p
                satis = p["guncel_fiyat"] if acik else p["cikis_fiyat"]
                kayitlar.append({
                    "hisse": sym,
                    "giris_tarih": pd.Timestamp(p["giris_tarih"]),
                    "giris_fiyat": round(p["giris_fiyat"], 2),
                    "cikis_tarih": None if acik else pd.Timestamp(p["cikis_tarih"]),
                    "satis_fiyat": round(satis, 2),
                    "getiri": round((satis / p["giris_fiyat"] - 1) * 100, 1),
                    "gun": p["gun"],
                    "acik": acik,
                })
        except Exception as e:
            basarisiz.append(f"{sym}({type(e).__name__})")
    kayitlar.sort(key=lambda x: (x["giris_tarih"], x["hisse"]))
    return kayitlar, basarisiz


def anahtar(k: dict) -> tuple:
    """Ayni pozisyonu iki tarama arasinda eslestirmek icin."""
    return (k["hisse"], k["giris_tarih"])


def tablo(kayitlar: list[dict]) -> list[str]:
    if not kayitlar:
        return ["Bu donemde sinyale giren hisse yok."]
    L = ["| Hisse | Giris | Giris F. | Guncel/Cikis F. | Getiri % | Gun | Durum |",
         "|---|---|---|---|---|---|---|"]
    for k in kayitlar:
        durum = "LISTEDE" if k["acik"] else f"cikti {k['cikis_tarih']:%d.%m}"
        L.append(f"| **{k['hisse']}** | {k['giris_tarih']:%d.%m.%Y} "
                 f"| {k['giris_fiyat']} | {k['satis_fiyat']} "
                 f"| {k['getiri']:+.1f}% | {k['gun']} | {durum} |")
    return L


def ozet(kayitlar: list[dict]) -> str:
    if not kayitlar:
        return "—"
    toplam = sum(k["getiri"] for k in kayitlar)
    karli = sum(1 for k in kayitlar if k["getiri"] > 0)
    return (f"{len(kayitlar)} giris | karli {karli} | "
            f"ortalama {toplam / len(kayitlar):+.2f}%")


def main() -> None:
    print(f"BIST 100 indiriliyor... ({len(T.TICKERS)} hisse)")
    data = yf.download(T.TICKERS, period="6mo", interval="1d",
                       auto_adjust=True, progress=False, group_by="ticker")
    if data.empty:
        raise SystemExit("HATA: veri alinamadi.")

    son_bar = pd.Timestamp(data.index[-1])
    esik = pd.Timestamp(datetime.now() - timedelta(days=GUN)).normalize()

    tavan = T.GETIRI_TAVAN
    if tavan is None:
        raise SystemExit("HATA: GETIRI_TAVAN kapali; karsilastirilacak filtre yok.")

    # 1) Yeni kriterle (tavan acik)
    T.GETIRI_TAVAN = tavan
    yeni, basarisiz = girisleri_topla(data, esik)

    # 2) Tavan kapaliyken — farki gormek icin
    T.GETIRI_TAVAN = None
    eski, _ = girisleri_topla(data, esik)
    T.GETIRI_TAVAN = tavan

    yeni_anahtarlar = {anahtar(k) for k in yeni}
    elenen = [k for k in eski if anahtar(k) not in yeni_anahtarlar]

    L = [
        f"# Son {GUN} Gunde Sinyale Girenler — yeni kriterle",
        "",
        f"Son veri gunu: **{son_bar:%d.%m.%Y}** | "
        f"Giris tarihi {esik:%d.%m.%Y} ve sonrasi | "
        f"Rapor: {datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"Kriterler: MACD > Sinyal, RSI > 50, Fiyat > MA5/MA9/MA21, "
        f"ADX({T.ADX_PERIYOT}) > {T.ADX_ESIK:g} (her gun), "
        f"Hacim > onceki {T.HACIM_PERIYOT} gun ortalamasi (giriste), "
        f"**Son {T.GETIRI_PERIYOT} gun getirisi < %{tavan:g} (giriste)**",
        "",
        f"## 🟢 Sinyale girenler ({len(yeni)})",
        "",
        *tablo(yeni),
        "",
        f"Ozet: {ozet(yeni)}",
        "",
        f"## ⛔ Getiri tavaninin eledigi girisler ({len(elenen)})",
        "",
        "Eski kriterlerle sinyal verirdi; **son "
        f"{T.GETIRI_PERIYOT} gunde %{tavan:g}'dan fazla kosmus** oldugu icin "
        "artik girilmiyor. Getiri sutunu, girilseydi ne olacagini gosterir.",
        "",
        *tablo(elenen),
        "",
        f"Ozet: {ozet(elenen)}",
        "",
        "---",
        f"Tavan kapali: {len(eski)} giris ({ozet(eski)})",
        f"Tavan acik  : {len(yeni)} giris ({ozet(yeni)})",
        "",
        "Not: Fiyatlar kapanistir; gercek islem fiyati ertesi gun acilisina "
        "gore degisir. Yuzdeler komisyon/slipaj icermez ve her isleme esit "
        "tutar konuldugu varsayimiyla ortalanmistir.",
    ]
    if basarisiz:
        L += ["", f"Veri alinamayan: {', '.join(basarisiz)}"]

    metin = "\n".join(L) + "\n"
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/girisler.md", "w", encoding="utf-8") as f:
        f.write(metin)
    print(metin)


if __name__ == "__main__":
    main()
