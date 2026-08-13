"""
Gunluk teknik tarama degerlendirmesi — BIST 100.

Tarama dosyalari "ne oldu" sorusunu cevapliyor; bu dosya "ne anlama
geliyor" sorusunu cevapliyor. Uc bolum:

  1) VERI SAGLIGI  — tarama gercekten calisti mi. Once bu, cunku
     eksik taramanin uzerine kurulan hicbir yorum gecerli degildir.
  2) GUNUN SONUCU  — alim listesi, izleme listesi, diger sistemin
     aktif sinyalleri.
  3) PIYASA GENELI — breadth ve endeks rejimi. Tekil sinyal yokken
     piyasanin hangi fazda oldugunu soyler.

Veriyi YENIDEN INDIRMEZ. Tarama zaten indirip sonuclar/ altina
yazdi; burasi sadece o ciktilari okur. Boylece degerlendirme, Yahoo'nun
kapanis alanini bos biraktigi pencereye ikinci kez maruz kalmaz.

Kullanim: python degerlendirme.py
"""

from __future__ import annotations

import json
import os
import re

import pandas as pd

SONUC = "sonuclar"


def _oku_json(ad: str) -> dict | None:
    yol = os.path.join(SONUC, ad)
    if not os.path.exists(yol):
        return None
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _oku_metin(ad: str) -> str:
    yol = os.path.join(SONUC, ad)
    if not os.path.exists(yol):
        return ""
    with open(yol, encoding="utf-8") as f:
        return f.read()


def veri_sagligi_bolumu(piyasa: dict | None, gunluk_md: str) -> list[str]:
    L = ["## 1. Veri sagligi", ""]
    if not piyasa:
        L += [
            "⚠️ `sonuclar/piyasa.json` bulunamadi. Tarama bu ozeti yazmadan "
            "once mi calisti, yoksa hic mi calismadi — kontrol et. "
            "Degerlendirmenin geri kalani yalnizca gunluk.md metnine "
            "dayaniyor, sayisal dogrulama yapilamadi.",
            "",
        ]
        return L

    vs = piyasa.get("veri_sagligi", {})
    evren = vs.get("evren", 0)
    taranan = vs.get("taranan", 0)
    elenen = vs.get("elenen", 0)
    guvenilir = vs.get("guvenilir", False)
    gun = piyasa.get("tarama_gunu", "?")

    if guvenilir and elenen == 0:
        L += [f"✅ **Saglam.** {gun} kapanisinda evrenin **{taranan}/{evren}** "
              "hissesi tarandi, elenen yok."]
    elif guvenilir:
        L += [f"🟡 **Kismen eksik.** {gun} kapanisinda **{taranan}/{evren}** "
              f"hisse tarandi, {elenen} hisse veri eksikligi yuzunden "
              "elendi. Sonuc kullanilabilir ama elenen hisselerde sinyal "
              "olup olmadigi bilinmiyor."]
        elenenler = vs.get("elenen_hisseler", [])
        if elenenler:
            L += ["", "Elenenler: " + ", ".join(elenenler[:30])
                  + (" ..." if len(elenenler) > 30 else "")]
    else:
        L += [f"🚨 **GUVENILIR DEGIL.** Evrenin {elenen}/{evren} hissesi "
              f"taranamadi; yalnizca {taranan} hisse olculdu. Bu bir "
              "'sinyal yok' gunu DEGIL, eksik tarama. Alim karari verme; "
              "`python teshis.py` ile veri saglayicisini kontrol et."]

    # Tarama gunu bugunden ne kadar eski?
    try:
        fark = (pd.Timestamp.now().normalize()
                - pd.Timestamp(gun).normalize()).days
        if fark > 3:
            L += ["", f"⚠️ Taranan gun bugunden **{fark} gun** eski. Uzun "
                      "tatil disinda bu veri gecikmesine isaret eder."]
    except Exception:
        pass

    # gunluk.md'de hayalet bar notu var mi?
    if "kapanisi saglayicida yok" in gunluk_md:
        L += ["", "ℹ️ Saglayici son barin kapanisini bos birakmis; tarama "
                  "bir onceki kapanan gune dusmus. Bu beklenen davranis — "
                  "veri geri dolunca kendiliginden duzelir."]

    L.append("")
    return L


def gun_sonucu_bolumu(piyasa: dict | None, gunluk_md: str,
                      latest: dict | None) -> list[str]:
    L = ["## 2. Gunun sonucu", ""]

    alim = (piyasa or {}).get("alim_listesi", [])
    izleme = (piyasa or {}).get("izleme_listesi", [])
    strateji = (piyasa or {}).get("strateji", "erken_dar")

    if alim:
        L += [f"### 🟢 Alim listesi — {len(alim)} hisse ({strateji})", "",
              "**" + ", ".join(alim) + "**", "",
              "Bu hisselerde tum kriterler sinyal gunu kapanisinda saglandi. "
              "Ertesi islem gunu **acilista** alinir; stop, gerceklesen alis "
              "fiyatinin 2xATR altina kurulur. Detay tablo ve stop yuzdeleri "
              "`sonuclar/gunluk.md` icinde.", ""]
    else:
        L += ["### 🟢 Alim listesi — bos", "",
              "Bugun tetiklenen hisse yok. Kriter gevsetilmez; sinyalsiz "
              "gunler cogunluktadir (5 yillik olcumde ayda ~6 sinyal).", ""]

    if izleme:
        L += [f"### 🟡 Izleme listesi — {len(izleme)} hisse", "",
              "Kurulumu tamam, tetigi bekleyen hisseler. **Buradan alim "
              "yapilmaz**; yalnizca yarin hangi hisselerin kirilim adayi "
              "oldugunu gosterir.", "",
              ", ".join(izleme[:20]) + (" ..." if len(izleme) > 20 else ""),
              ""]

    # Ikinci sistem (MACD/RSI/ADX) — tarama.py ciktisi
    if latest:
        aktif = latest.get("aktif_sinyaller", [])
        if aktif:
            L += [f"### 📊 Diger sistem (MACD/RSI/ADX) — {len(aktif)} aktif "
                  "sinyal", "",
                  "| Hisse | Giris | Giris F. | Guncel | Getiri | Gun |",
                  "|---|---|---|---|---|---|"]
            for p in aktif[:15]:
                L.append(f"| {p.get('hisse')} | {p.get('giris_tarih')} "
                         f"| {p.get('giris_fiyat')} | {p.get('guncel_fiyat')} "
                         f"| {p.get('getiri'):+.1f}% | {p.get('gun')} |")
            L += ["", "Bu ayri bir sistem ve ayri olculdu — erken giris "
                      "listesiyle karistirma.", ""]

    return L


def piyasa_bolumu(piyasa: dict | None) -> list[str]:
    L = ["## 3. Piyasa geneli", ""]
    if not piyasa:
        L += ["Veri yok.", ""]
        return L

    b = piyasa.get("breadth", {})
    r = piyasa.get("endeks_rejimi", {})
    olculen = b.get("olculen", 0)
    if not olculen:
        L += ["Breadth olculemedi.", ""]
        return L

    zirve = b.get("zirveye_yakin_yuzde", 0)
    dar = b.get("dar_bazda_yuzde", 0)
    ma50 = b.get("ma50_ustunde_yuzde", 0)
    kirilim = b.get("kirilim_yapan", 0)

    if r:
        yon = []
        yon.append("MA50 **ustunde**" if r.get("ma50_ustunde")
                   else "MA50 **altinda**")
        yon.append("MA200 **ustunde**" if r.get("ma200_ustunde")
                   else "MA200 **altinda**")
        deg = r.get("gunluk_degisim_yuzde")
        L += [f"**XU100:** {r.get('kapanis')}"
              + (f" ({deg:+.2f}%)" if deg is not None else "")
              + " — " + ", ".join(yon)
              + (", MA50 > MA200 (altin kesisim konumu)"
                 if r.get("ma50_ma200_uzerinde") else
                 ", MA50 < MA200 (olum kesisimi konumu)"),
              ""]

    L += ["| Olcu | Deger | Ne demek |", "|---|---|---|",
          f"| 52h zirvesine yakin | %{zirve} | Evrenin bu kadari zirvenin "
          "%80'i uzerinde — katilimin genisligi |",
          f"| Dar bazda | %{dar} | Sikismis, kirilima hazir hisse orani |",
          f"| MA50 ustunde | %{ma50} | Klasik breadth; %50 ustu saglikli |",
          f"| Bugun kirilim yapan | {kirilim} hisse | 20 gunluk zirveyi "
          "gecen hisse sayisi |",
          ""]

    # Faz yorumu — sayilari tek cumleye cevir
    if ma50 >= 60 and zirve >= 50:
        faz = ("**Genis katilimli yukselis.** Evrenin cogunlugu MA50 "
               "ustunde ve zirveye yakin. Kirilim sinyalleri bu ortamda "
               "daha guvenilir calisir.")
    elif ma50 >= 60:
        faz = ("**Toparlanma, ama zirveden uzak.** Cogunluk MA50 ustunde "
               "olsa da zirveye yakin hisse azinlikta; hareket henuz "
               "olgunlasmamis.")
    elif ma50 <= 35:
        faz = ("**Zayif piyasa.** Evrenin cogunlugu MA50 altinda. Kirilim "
               "stratejileri bu ortamda daha cok yanlis sinyal uretir; "
               "sinyal ciksa bile pozisyon boyutunu kucuk tut.")
    else:
        faz = ("**Kararsiz/yatay.** Breadth ortada. Tekil sinyallere "
               "guvenmek yerine kurulumun tamamlanmasini beklemek daha "
               "makul.")
    L += [faz, ""]

    if dar >= 40:
        L += [f"Evrenin %{dar}'i dar bazda — sikisma yaygin. Sikismalar "
              "genelde yonlu bir hareketle cozulur; onumuzdeki gunlerde "
              "kirilim sayisinda artis olabilir.", ""]

    return L


def main() -> None:
    piyasa = _oku_json("piyasa.json")
    latest = _oku_json("latest.json")
    gunluk_md = _oku_metin("gunluk.md")

    gun = (piyasa or {}).get("tarama_gunu")
    if not gun:
        m = re.search(r"Taranan gun \(kapanis\): (\d{2}\.\d{2}\.\d{4})",
                      gunluk_md)
        gun = m.group(1) if m else "?"
    else:
        try:
            gun = f"{pd.Timestamp(gun):%d.%m.%Y}"
        except Exception:
            pass

    L = [f"# BIST 100 Teknik Tarama Degerlendirmesi — {gun}", "",
         f"Olusturuldu: {pd.Timestamp.now():%Y-%m-%d %H:%M} | "
         "Kaynak: `sonuclar/` altindaki tarama ciktilari (veri yeniden "
         "indirilmedi)", ""]
    L += veri_sagligi_bolumu(piyasa, gunluk_md)
    L += gun_sonucu_bolumu(piyasa, gunluk_md, latest)
    L += piyasa_bolumu(piyasa)
    L += ["---",
          "Bu degerlendirme tarama ciktilarinin yorumudur, yatirim "
          "tavsiyesi degildir. Alim kararlari icin `sonuclar/gunluk.md` "
          "icindeki tablo ve stop seviyeleri esastir."]

    metin = "\n".join(L) + "\n"
    os.makedirs(SONUC, exist_ok=True)
    with open(os.path.join(SONUC, "degerlendirme.md"), "w",
              encoding="utf-8") as f:
        f.write(metin)
    print(metin)
    print("\n[degerlendirme] sonuclar/degerlendirme.md yazildi.")


if __name__ == "__main__":
    main()
