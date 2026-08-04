"""
Gunluk tarama — HANGI HISSE, BUGUN.

rapor.py stratejiyi olcer (gecmiste ne kazandirdi). Bu dosya ise
bugun ne alinacagini soyler. Iki liste uretir:

  1) TETIKLENDI — tum giris kriterleri BUGUN saglandi. Alim adaylari.

  2) IZLEME LISTESI — kurulum tamam, tetik henuz gelmedi. Asil deger
     burada: "yukselisi ilk gununden yakalamak" istiyorsan kirilim
     gununu beklerken hangi hisseye bakacagini onceden bilmen gerekir.
     Kirilim gunu sabah bu listeye bakip gun ici takip edebilirsin.

Her hisse icin katalizor degerleri ayri ayri yazilir (RVOL kac, baz ne
kadar dar, zirveden ne kadar uzak), boylece sinyalin NEDEN olustugu
gorunur — tek bir True/False degil.

Kullanim:
    python gunluk.py                    # erken_dar stratejisi
    python gunluk.py --strateji erken
    python gunluk.py --liste sp500      # ABD evreni (henuz tanimli degilse hata)
"""

from __future__ import annotations

import argparse
import os

import pandas as pd

import gostergeler as G
import strateji as S
import veri as V
from tarama import BIST100

ENDEKS_ADAYLARI = ["XU100.IS", "^XU100"]

STRATEJILER = {
    "erken": S.erken_giris,
    "erken_dar": S.erken_dar,
    "erken_yalin": S.erken_yalin,
    "mevcut": S.mevcut_sistem,
}


def endeks_getir(periyot: str, tazele: bool) -> pd.Series:
    hatalar = []
    for sembol in ENDEKS_ADAYLARI:
        try:
            s = V.tek_sembol(sembol, periyot=periyot, tazele=tazele)
            if len(s) > 60:
                return s
            hatalar.append(f"{sembol}: {len(s)} satir (yetersiz)")
        except Exception as exc:
            hatalar.append(f"{sembol}: {type(exc).__name__}")
    raise SystemExit("HATA: endeks verisi alinamadi.\n  " + "\n  ".join(hatalar))


def katalizor_degerleri(d: pd.DataFrame, ham: pd.DataFrame,
                        endeks: pd.Series) -> dict:
    """
    Son gunun katalizor olcumleri — sinyalin NEDEN olustugunu gosterir.

    d   : duzeltilmis fiyatlar — TUM gosterge hesaplari bunun uzerinde
          (bolunme/bedelsiz seriyi kirmasin diye).
    ham : ham fiyatlar — TABLODA gosterilecek fiyat, kirilim seviyesi ve
          stop bunlardan. Kullanicinin aracı kurum ekraninda gordugu sayi.

    Oransal olculer (RVOL, baz genisligi, ATR%) duzeltmeden etkilenmez;
    mutlak TL seviyeleri etkilenir. Bu yuzden yalnizca seviyeler ham
    fiyattan alinir.
    """
    close, high, low, vol = d["Close"], d["High"], d["Low"], d["Volume"]
    son = -1

    def deger(seri) -> float:
        try:
            v = float(seri.iloc[son])
            return v if v == v else float("nan")
        except Exception:
            return float("nan")

    atr_yuzde = deger(G.atr(high, low, close, 20)) / deger(close) * 100

    # Seviyeler ham fiyattan
    ham_fiyat = deger(ham["Close"])
    ham_d20 = deger(G.donchian_ust(ham["High"], 20))
    ham_atr = ham_fiyat * atr_yuzde / 100 if ham_fiyat == ham_fiyat else float("nan")

    return {
        "fiyat": ham_fiyat,
        "rvol": deger(G.rvol(vol, 20)),
        "baz_genislik": deger(G.baz_genisligi(high, low, 20)) * 100,
        "zirve_yakinlik": deger(G.zirve_yakinligi(close, 252)) * 100,
        "kapanis_konum": deger(G.kapanis_konumu(high, low, close)) * 100,
        "d20_zirve": ham_d20,
        "kirilima_uzaklik": ((ham_d20 / ham_fiyat - 1) * 100
                             if ham_fiyat and ham_d20 == ham_d20 else float("nan")),
        "atr_yuzde": atr_yuzde,
        "stop": ham_fiyat - 2.0 * ham_atr if ham_fiyat == ham_fiyat else float("nan"),
        # Izleme listesi icin: giris kirilim SEVIYESINDEN olacagi icin
        # stop da o seviyeye gore hesaplanir, bugunku fiyata gore degil.
        "kirilim_stop": (ham_d20 - 2.0 * ham_atr
                         if ham_d20 == ham_d20 and ham_atr == ham_atr
                         else float("nan")),
        "gg_kirilim": bool(G.gg_kirilimi(close, endeks, 20).iloc[son]),
        "hacim_toplama": deger(G.hacim_genislemesi(vol, 5, 60)),
    }


def tara(strat: S.Strateji, data: pd.DataFrame, semboller: list[str],
         endeks: pd.Series) -> tuple[list[dict], list[dict]]:
    """(tetiklenenler, izleme_listesi) doner."""
    kurulumlar = strat.alt_kume("kurulum") + strat.alt_kume("surekli")
    tetikler = strat.alt_kume("tetik")

    tetiklendi, izleme = [], []
    for sembol in semboller:
        d = V.hisse_cerceve(data, sembol)                      # gostergeler
        ham = V.hisse_cerceve(data, sembol, duzeltilmis=False)  # ekran fiyati
        if d is None or ham is None or len(d) < S.MIN_VERI:
            continue
        try:
            kurulum_ok, kurulum_detay = True, []
            for k in kurulumlar:
                v = bool(k.fn(d, endeks).reindex(d.index)
                         .fillna(False).astype(bool).iloc[-1])
                kurulum_detay.append((k.ad, v))
                kurulum_ok &= v

            tetik_detay = []
            for k in tetikler:
                v = bool(k.fn(d, endeks).reindex(d.index)
                         .fillna(False).astype(bool).iloc[-1])
                tetik_detay.append((k.ad, v))
            tetik_sayisi = sum(v for _, v in tetik_detay)

            if not kurulum_ok:
                continue

            kayit = {
                "hisse": sembol.replace(".IS", ""),
                "tetik_sayisi": tetik_sayisi,
                "tetik_toplam": len(tetik_detay),
                "eksik": [ad for ad, v in tetik_detay if not v],
                **katalizor_degerleri(d, ham, endeks),
            }
            if tetik_sayisi == len(tetik_detay):
                tetiklendi.append(kayit)
            else:
                izleme.append(kayit)
        except Exception:
            continue

    tetiklendi.sort(key=lambda x: -(x["rvol"] if x["rvol"] == x["rvol"] else 0))
    # Izleme listesi: once en cok tetigi dolmus, sonra kirilima en yakin
    izleme.sort(key=lambda x: (-x["tetik_sayisi"],
                               x["kirilima_uzaklik"]
                               if x["kirilima_uzaklik"] == x["kirilima_uzaklik"]
                               else 999))
    return tetiklendi, izleme


def _sayi(x, ek: str = "", basamak: int = 2) -> str:
    return "—" if x != x else f"{x:.{basamak}f}{ek}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strateji", default="erken_dar", choices=list(STRATEJILER))
    ap.add_argument("--periyot", default="2y")
    ap.add_argument("--tazele", action="store_true")
    ap.add_argument("--izleme-limit", type=int, default=25,
                    help="izleme listesinde en fazla kac hisse gosterilsin")
    ap.add_argument("--azami-yas", type=float, default=4.0,
                    dest="azami_yas",
                    help="onbellek bu saatten eskiyse yeniden indirilir "
                         "(varsayilan 4)")
    ap.add_argument("--azami-uzaklik", type=float, default=10.0,
                    dest="azami_uzaklik",
                    help="izleme listesinde kirilim seviyesine bu yuzdeden "
                         "uzak hisseler gosterilmez (varsayilan 10). Tek "
                         "gunde %%10 yukselip kirilim yapmasi zaten "
                         "beklenmez; 3-5 daha gercekcidir")
    a = ap.parse_args()

    strat = STRATEJILER[a.strateji]()
    semboller = [t + ".IS" for t in BIST100]
    # Gunluk tarama icin onbellek yasi kisa tutulur: bayat veriyle
    # uretilen liste sessizce dunun listesi olur.
    data = V.veri_getir(semboller, "bist100", periyot=a.periyot,
                        tazele=a.tazele, azami_yas_saat=a.azami_yas)
    endeks = endeks_getir(a.periyot, a.tazele)

    son_tarih = pd.Timestamp(data.index[-1])
    gecikme = (pd.Timestamp.now().normalize() - son_tarih.normalize()).days
    tetiklendi, izleme = tara(strat, data, semboller, endeks)

    # Ulasilamayacak kadar uzaktakileri ele: tek gunde o mesafeyi kapatip
    # kirilim yapmasi beklenmedigi icin listede yer kaplamalari anlamsiz.
    uzak = [t for t in izleme
            if t["kirilima_uzaklik"] == t["kirilima_uzaklik"]
            and t["kirilima_uzaklik"] > a.azami_uzaklik]
    izleme = [t for t in izleme if t not in uzak]

    L = [
        f"# Gunluk Tarama — {son_tarih:%d.%m.%Y}",
        "",
        f"Strateji: **{strat.ad}** | Evren: BIST 100 | "
        f"Rapor: {pd.Timestamp.now():%Y-%m-%d %H:%M}",
        "",
        f"**Verinin son gunu: {son_tarih:%d.%m.%Y}**"
        + (f"  ⚠️ bugunden {gecikme} gun eski — piyasa kapaliysa normal, "
           "degilse veri gecikmesi var" if gecikme > 1 else ""),
        "",
        "Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum "
        "ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/"
        "bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.",
        "",
        f"## 🟢 BUGUN TETIKLENDI ({len(tetiklendi)})",
        "",
        "Tum giris kriterleri bugun saglandi.",
        "",
    ]

    if tetiklendi:
        L += ["| Hisse | Fiyat | RVOL | Baz gen. | 52h zirve | Kapanis konum "
              "| ATR% | Onerilen stop |",
              "|---|---|---|---|---|---|---|---|"]
        for t in tetiklendi:
            L.append(
                f"| **{t['hisse']}** | {_sayi(t['fiyat'])} "
                f"| {_sayi(t['rvol'], 'x')} | {_sayi(t['baz_genislik'], '%', 1)} "
                f"| {_sayi(t['zirve_yakinlik'], '%', 0)} "
                f"| {_sayi(t['kapanis_konum'], '%', 0)} "
                f"| {_sayi(t['atr_yuzde'], '%', 1)} | {_sayi(t['stop'])} |")
    else:
        L.append("Bugun tetiklenen hisse yok.")

    L += [
        "",
        f"## 🟡 IZLEME LISTESI ({len(izleme)})",
        "",
        "Kurulum tamam, tetik henuz gelmedi. **Asil liste bu:** kirilim "
        "gununde almak istiyorsan yarin hangi hisseye bakacagini buradan "
        "secersin. `Kirilim` sutunu, 20 gunluk zirveye ne kadar kaldigini "
        "gosterir — %0'a yakin olan bir sonraki guclu gunde tetiklenir.",
        "",
    ]

    if izleme:
        L += ["| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik "
              "| Stop (bu seviyeden) | Eksik kriter | Baz gen. |",
              "|---|---|---|---|---|---|---|"]
        for t in izleme[:a.izleme_limit]:
            L.append(
                f"| **{t['hisse']}** | {_sayi(t['fiyat'])} "
                f"| **{_sayi(t['d20_zirve'])}** "
                f"| {_sayi(t['kirilima_uzaklik'], '%', 1)} "
                f"| {_sayi(t['kirilim_stop'])} "
                f"| {', '.join(t['eksik']) or '—'} "
                f"| {_sayi(t['baz_genislik'], '%', 1)} |")
        if len(izleme) > a.izleme_limit:
            L.append("")
            L.append(f"_{len(izleme) - a.izleme_limit} hisse daha var; "
                     f"--izleme-limit ile artirabilirsin._")
    else:
        L.append("Kurulumu tamamlanmis hisse yok.")

    if uzak:
        L += ["", f"_Kirilim seviyesine %{a.azami_uzaklik:g}'den uzak "
                  f"{len(uzak)} hisse listeden cikarildi (tek gunde o "
                  f"mesafeyi kapatmasi beklenmez): "
                  + ", ".join(t["hisse"] for t in uzak[:15])
                  + (" ..." if len(uzak) > 15 else "") + "_"]

    L += [
        "",
        "### Nasil kullanilir",
        "",
        "1. Bu liste **kapanistan sonra** uretilir.",
        "2. Ertesi gun, hissenin fiyati **ALIM SEVIYESI**'ni gecerse aday olur.",
        "3. **Ama seviyeyi gecmesi tek basina yetmez.** Sinyalin tamamlanmasi "
        "icin o gun ayrica hacmin patlamasi (20 gun medyaninin 2 kati) ve "
        "kapanisin gun icindeki en yuksek %30'luk dilimde olmasi gerekir. "
        "Bu ikisi ancak KAPANISTA belli olur.",
        "4. Yani seviyeyi gun icinde gecerken alirsan, sinyalin onaylanip "
        "onaylanmayacagini bilmeden almis olursun. Olcumler kapanis "
        "fiyatina gore yapildi; en yakin uygulama kapanisa dogru veya "
        "ertesi acilista almaktir.",
        "5. Stop sutunu, alim seviyesinden girildigi varsayimiyla "
        "hesaplanmistir (seviye - 2 x ATR).",
    ]

    L += [
        "",
        "## Kriterler",
        "",
    ]
    for tip in ("kurulum", "tetik", "surekli", "kalma"):
        for k in strat.alt_kume(tip):
            L.append(f"- `{tip}` **{k.ad}** — {k.aciklama}")

    L += [
        "",
        "## Sutunlar",
        "",
        "- **RVOL** — bugunku hacim / onceki 20 gunun medyani. 2x uzeri = patlama.",
        "- **Baz gen.** — son 20 gunun dip-tepe genisligi. Dar baz (<%18) "
        "daha temiz kirilim verir.",
        "- **52h zirve** — fiyatin 52 haftalik zirveye orani.",
        "- **Kapanis konum** — kapanisin gun ici araliktaki yeri. %70 uzeri "
        "= gun boyu alici baskisi.",
        "- **Kirilim seviyesi** — onceki 20 gunun en yuksegi. Kapanis bunu "
        "gecerse tetik olusur.",
        "- **Uzaklik** — kirilim seviyesine kalan mesafe. **Negatif ise "
        "fiyat seviyeyi ZATEN gecmis**, sinyal baska bir kriterle "
        "bekliyor (genelde hacim). Eksik kriter sutunu hangisi oldugunu "
        "soyler.",
        "- **Onerilen stop** — giris - 2 x ATR(20). Sabit yuzde degil, "
        "hissenin kendi oynakligina gore.",
        "",
        "---",
        "Fiyatlar kapanistir; gercek islem fiyati ertesi gun acilisina gore "
        "degisir. Bu bir yatirim tavsiyesi degildir.",
    ]

    metin = "\n".join(L) + "\n"
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/gunluk.md", "w", encoding="utf-8") as f:
        f.write(metin)
    print(metin)
    print("\n[gunluk] sonuclar/gunluk.md yazildi.")


if __name__ == "__main__":
    main()
