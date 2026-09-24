# Gunluk Tarama — 24.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-24 19:29

**Taranan gun (kapanis): 24.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**24.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (12) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **TUPRS** | 410.75 | **424.25** | 3.3% | 392.57 | kirilim, rvol2, tepede_kapanis | 12.0% |
| **BIMAS** | 422.75 | **443.25** | 4.8% | 418.85 | kirilim, rvol2, tepede_kapanis | 13.7% |
| **CCOLA** | 77.00 | **81.70** | 6.1% | 76.44 | kirilim, rvol2, tepede_kapanis | 9.5% |
| **EREGL** | 37.94 | **40.36** | 6.4% | 37.52 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **GARAN** | 129.40 | **137.80** | 6.5% | 129.10 | kirilim, rvol2, tepede_kapanis | 17.0% |
| **AEFES** | 18.69 | **19.96** | 6.8% | 18.70 | kirilim, rvol2, tepede_kapanis | 13.0% |
| **MPARK** | 426.50 | **455.75** | 6.9% | 429.16 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **TOASO** | 279.50 | **299.75** | 7.2% | 277.91 | kirilim, rvol2, tepede_kapanis | 16.6% |
| **KCHOL** | 216.00 | **232.50** | 7.6% | 218.66 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **SOKM** | 57.50 | **61.90** | 7.7% | 57.24 | kirilim, rvol2, tepede_kapanis | 13.2% |
| **TURSG** | 5.93 | **6.40** | 7.9% | 6.01 | kirilim, rvol2, tepede_kapanis | 10.7% |
| **AKSA** | 10.66 | **11.66** | 9.4% | 10.94 | kirilim, rvol2, tepede_kapanis | 14.4% |

_Kirilim seviyesine %10'den uzak 3 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): ANSGR, ENJSA, DOHOL_

## Nasil kullanilir

1. Tarama her islem gunu **kapanistan sonra** calisir.
2. **ALIM LISTESI**'ndeki hisseleri ertesi islem gunu **acilista** al. Baska sart aramana gerek yok — kriterlerin hepsi sinyal gununun kapanisinda zaten dogrulandi.
3. Gerceklesen alis fiyatina gore stopu kur (tablodaki yuzde kadar asagi). Hisse yukseldikce stopu yukari cek, asla asagi indirme.
4. Alim listesi bossa o gun islem yok. Zorlamak yok.

Bu akis kasten basit: gun ici takip, seviye bekleme, emir kurma yok. Bedeli olculdu — kapanista almaya gore islem basina 0.80 puan. Karsiliginda her gun ekran basinda olmak zorunda kalmiyorsun.

## Kriterler

- `kurulum` **dar_baz** — Son 20 gunluk baz genisligi < %18 — dar baz kaliteli kirilim verir
- `kurulum` **zirveye_yakin** — Fiyat 52 hafta zirvesinin %80'i uzerinde
- `tetik` **kirilim** — Kapanis > onceki 20 gunun en yuksegi — tanimi geregi hareketin 1. gunu
- `tetik` **rvol2** — Hacim, onceki 20 gun medyaninin 2 katindan fazla
- `tetik` **tepede_kapanis** — Kapanis gunun araliginin ust %30'unda — gun boyu alici baskisi

## Sutunlar

- **RVOL** — bugunku hacim / onceki 20 gunun medyani. 2x uzeri = patlama.
- **Baz gen.** — son 20 gunun dip-tepe genisligi. Dar baz (<%18) daha temiz kirilim verir.
- **52h zirve** — fiyatin 52 haftalik zirveye orani.
- **Kapanis konum** — kapanisin gun ici araliktaki yeri. %70 uzeri = gun boyu alici baskisi.
- **Kirilim seviyesi** — onceki 20 gunun en yuksegi. Kapanis bunu gecerse tetik olusur.
- **Uzaklik** — kirilim seviyesine kalan mesafe. **Negatif ise fiyat seviyeyi ZATEN gecmis**, sinyal baska bir kriterle bekliyor (genelde hacim). Eksik kriter sutunu hangisi oldugunu soyler.
- **Onerilen stop** — giris - 2 x ATR(20). Sabit yuzde degil, hissenin kendi oynakligina gore.

---
Fiyatlar kapanistir; gercek islem fiyati ertesi gun acilisina gore degisir. Bu bir yatirim tavsiyesi degildir.
