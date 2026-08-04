"""
Olcum raporu — mevcut sistem ile erken giris sistemini yan yana olcer.

Kullanim:
    python rapor.py                 # BIST 100, 2 yil
    python rapor.py --periyot 5y
    python rapor.py --tazele        # onbellegi yok say, yeniden indir

Cikti: sonuclar/olcum.md

Raporu okurken:
  - "Beklenti" tek basina yeterli degil; EVREN KIYASI satirina bakin.
    Ayni gunlerde ortalama hisse ne yaptiysa asil sayi aradaki farktir.
  - Ablasyon tablosunda bir kriteri cikarinca beklenti YUKSELIYORSA
    o kriter zarar veriyordur.
  - Islem sayisi 30'un altindaysa hicbir sonuc istatistiksel degildir;
    periyodu uzatin ya da kriterleri gevsetin.
"""

from __future__ import annotations

import argparse
import os

import pandas as pd

import olcum as O
import strateji as S
import veri as V
from tarama import BIST100

ENDEKS_ADAYLARI = ["XU100.IS", "^XU100"]


def endeks_getir(periyot: str, tazele: bool) -> pd.Series:
    hatalar = []
    for sembol in ENDEKS_ADAYLARI:
        try:
            s = V.tek_sembol(sembol, periyot=periyot, tazele=tazele)
            if len(s) > 60:
                print(f"[rapor] endeks: {sembol} ({len(s)} gun)")
                return s
            hatalar.append(f"{sembol}: {len(s)} satir (yetersiz)")
        except Exception as exc:
            hatalar.append(f"{sembol}: {type(exc).__name__}")
    raise SystemExit(
        "HATA: endeks verisi alinamadi. Goreli guc ve rejim ayrimi bu "
        "veri olmadan hesaplanamaz; yaniltici rapor uretmemek icin "
        "duruluyor.\n  " + "\n  ".join(hatalar))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--periyot", default="2y",
                    help="veri periyodu (2y, 5y, 10y...)")
    ap.add_argument("--baslangic", default=None,
                    help="bu tarihten sonraki girisler (YYYY-MM-DD)")
    ap.add_argument("--tazele", action="store_true",
                    help="onbellegi yok say, yeniden indir")
    ap.add_argument("--bolme", default=None,
                    help="donem bolme tarihi (YYYY-MM-DD). Ayni backtest "
                         "uzerinde varyant secmenin yarattigi uydurma "
                         "riskini gormek icin; bos birakilirsa verinin "
                         "orta noktasi kullanilir")
    a = ap.parse_args()

    semboller = [t + ".IS" for t in BIST100]
    data = V.veri_getir(semboller, "bist100", periyot=a.periyot,
                        tazele=a.tazele)
    endeks = endeks_getir(a.periyot, a.tazele)

    stratejiler = (S.mevcut_sistem(), S.erken_giris(), S.erken_yalin(),
                   S.erken_dar())
    L: list[str] = [
        f"# Olcum Raporu — {pd.Timestamp.now():%Y-%m-%d %H:%M}",
        "",
        f"Evren: BIST 100 ({len(semboller)} hisse) | Periyot: {a.periyot}"
        + (f" | Girisler {a.baslangic} sonrasi" if a.baslangic else ""),
        "",
        "> **Tek basina getiri sayisi yorumlanamaz.** Her strateji icin "
        "**evren kiyasi** satirina bakin: ayni tarihlerde ortalama hisse "
        "ne getirdiyse, stratejinin katkisi aradaki farktir. TL bazli "
        "getiriler enflasyonla siser; mutlak sayilar degil FARK anlamlidir.",
        "",
        "> ⚠️ **Hayatta kalma yanliligi.** Evren, BIST 100'un BUGUNKU "
        "bilesimidir; gecmise dogru uygulanmasi 'bugun endekste olmayi "
        "basarmis' hisseleri test etmek demektir. Cokup endeksten dusenler "
        "listede yok, bu da mutlak getirileri yukari sisirir. Evren kiyasi "
        "bu yanliligi KISMEN giderir (kiyas da ayni carpik evreni kullanir), "
        "bu yuzden **fark satirina mutlak getiriden cok daha fazla "
        "guvenilebilir**. Periyot uzadikca yanlilik buyur.",
        "",
    ]

    for strat in stratejiler:
        isl = O.calistir(strat, data, semboller, endeks, a.baslangic)
        L += O.ozet_yaz(f"{strat.ad} sistemi", O.metrikler(isl),
                        O.portfoy(isl))

        if isl.empty:
            continue

        kiyas = O.evren_kiyasi(isl, data, semboller)
        fark = kiyas["fark"].mean()
        L += [
            f"**Evren kiyasi:** strateji {kiyas['getiri'].mean()*100:+.2f}% vs "
            f"ayni tarihlerde ortalama hisse {kiyas['evren_getiri'].mean()*100:+.2f}% "
            f"→ **fark {fark*100:+.2f}%**"
            + ("  ✅ evreni geciyor" if fark > 0 else "  ❌ evrenin altinda"),
            "",
        ]

        gec = O.gecikme_olc(isl, data)
        L += [
            f"**Giris konumu:** dipten ortalama +{gec['dipten_yukselis'].mean():.1f}% "
            f"yukarida | 20 gunluk aralikta konum "
            f"{gec['aralik_konum'].mean():.0f}/100 "
            f"(>=100 = kirilim gunu girisi)",
            "",
            f"**Cikis sebepleri:** "
            + ", ".join(f"{k}: {v}" for k, v in
                        isl["sebep"].value_counts().items()),
            "",
        ]

        rej = O.rejim_ayir(isl, endeks)
        if not rej.empty:
            L += ["**Rejime gore:**", "",
                  "| Rejim | Islem | Isabet | Ort. getiri | Beklenti |",
                  "|---|---|---|---|---|"]
            for ad, r in rej.iterrows():
                L.append(f"| {ad} | {int(r['islem'])} | {r['isabet']*100:.1f}% "
                         f"| {r['ort_getiri']*100:+.2f}% "
                         f"| {r['beklenti']*100:+.2f}% |")
            L.append("")

    # Ablasyon yalin sistem uzerinde: budanmis surumun kalan kriterleri
    # hala tasiyip tasimadigini gorurruz.
    hedef = S.erken_yalin()
    L += [f"## Ablasyon — her kriterin katkisi ({hedef.ad})", "",
          "Bir kriteri cikarinca **beklenti yukseliyorsa** o kriter zarar "
          "veriyordur. Islem sayisi cok artip beklenti korunuyorsa kriter "
          "gereksiz yere firsat kaciriyordur.", ""]
    ab = O.ablasyon(hedef, data, semboller, endeks, a.baslangic)
    L += ["| Varyant | Islem | Isabet | Ort. getiri | Beklenti | PF |",
          "|---|---|---|---|---|---|"]
    for ad, r in ab.iterrows():
        if not r.get("islem"):
            L.append(f"| {ad} | 0 | — | — | — | — |")
            continue
        L.append(f"| {ad} | {int(r['islem'])} | {r['isabet']*100:.1f}% "
                 f"| {r['ort_getiri']*100:+.2f}% | {r['beklenti']*100:+.2f}% "
                 f"| {r['profit_factor']:.2f} |")

    # ---- Giris zamani: kapanista mi, ertesi acilista mi? ----
    L += ["", "## Giris zamani — kapanis mi, ertesi acilis mi?", "",
          "Olcumler sinyal gununun KAPANISINDAN girildigi varsayimiyla "
          "yapilir. Pratikte bu, kapanisa dakikalar kala ekranda olmayi "
          "gerektirir. Kolay alternatif ertesi gun acilistan girmektir; "
          "bedeli gecelik boslugun (gap) maliyetidir. Asagidaki tablo o "
          "maliyeti gosterir.", ""]
    L += ["| Strateji | Giris | Islem | Isabet | Beklenti | PF |",
          "|---|---|---|---|---|---|"]
    for temel in (S.erken_giris(), S.erken_dar()):
        for zaman in ("kapanis", "ertesi_acilis"):
            st = temel.giris_zamanli(zaman)
            m = O.metrikler(O.calistir(st, data, semboller, endeks,
                                       a.baslangic))
            if not m.get("islem"):
                continue
            L.append(f"| {temel.ad} | {zaman} | {m['islem']} "
                     f"| {m['isabet']*100:.1f}% | {m['beklenti']*100:+.2f}% "
                     f"| {m['profit_factor']:.2f} |")
    L.append("")

    # ---- Donem bolme: uydurma (curve-fitting) kontrolu ----
    bolme = a.bolme or str(
        pd.Timestamp(data.index[len(data.index) // 2]).date())
    L += ["", "## Donem bolme — uydurma kontrolu", "",
          f"Bolme tarihi: **{bolme}**", "",
          "Varyantlari ayni backtest uzerinde secmek, o donemin gurultusune "
          "uyum saglama riskini dogurur. Bir strateji yalnizca 1. donemde "
          "calisiyorsa **sonuca guvenmeyin**; 2. donem gercek beklentiye "
          "daha yakindir.", ""]
    for strat in stratejiler:
        db = O.donem_bol(strat, data, semboller, endeks, bolme)
        if db.empty:
            continue
        L += [f"**{strat.ad}**", "",
              "| Donem | Islem | Isabet | Ort. getiri | Beklenti | PF |",
              "|---|---|---|---|---|---|"]
        for ad, r in db.iterrows():
            L.append(f"| {ad} | {int(r['islem'])} | {r['isabet']*100:.1f}% "
                     f"| {r['ort_getiri']*100:+.2f}% "
                     f"| {r['beklenti']*100:+.2f}% "
                     f"| {r['profit_factor']:.2f} |")
        L.append("")

    L += ["", "## Kriterler", ""]
    for strat in stratejiler:
        L += [f"**{strat.ad}:**", ""]
        for tip in ("kurulum", "tetik", "surekli", "kalma"):
            for k in strat.alt_kume(tip):
                L.append(f"- `{tip}` **{k.ad}** — {k.aciklama}")
        c = strat.cikis
        L += ["", f"  Cikis: "
              + (f"ATR x{c.atr_carpan}" if c.atr_carpan else "ATR stop yok")
              + (", iz suren" if c.iz_suren else "")
              + (", kriter bozulunca" if c.kriter_bozulunca else ""), ""]

    L += ["", "---",
          "Fiyatlar kapanistir. Stop 'bu seviyeyi ilk goren kapanista cik' "
          "demektir; gap ile acilan dususte gerceklesen zarar daha kotu olur. "
          "Komisyon ve slipaj dahil degildir."]

    metin = "\n".join(L) + "\n"
    os.makedirs("sonuclar", exist_ok=True)
    with open("sonuclar/olcum.md", "w", encoding="utf-8") as f:
        f.write(metin)
    print(metin)
    print("\n[rapor] sonuclar/olcum.md yazildi.")


if __name__ == "__main__":
    main()
