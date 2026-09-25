# Gunluk Tarama — 25.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-25 19:31

**Taranan gun (kapanis): 25.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**25.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (12) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **TOASO** | 290.00 | **299.75** | 3.4% | 277.81 | kirilim, rvol2 | 16.6% |
| **CCOLA** | 77.90 | **81.70** | 4.9% | 76.48 | kirilim, rvol2 | 9.5% |
| **AEFES** | 18.83 | **19.96** | 6.0% | 18.72 | kirilim, rvol2 | 13.0% |
| **BIMAS** | 424.75 | **443.25** | 4.4% | 419.22 | kirilim, rvol2, tepede_kapanis | 13.7% |
| **TUPRS** | 406.00 | **424.25** | 4.5% | 392.83 | kirilim, rvol2, tepede_kapanis | 11.6% |
| **GARAN** | 129.80 | **137.80** | 6.2% | 129.33 | kirilim, rvol2, tepede_kapanis | 17.0% |
| **MPARK** | 427.00 | **455.75** | 6.7% | 429.79 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **EREGL** | 37.74 | **40.36** | 6.9% | 37.57 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **KCHOL** | 216.50 | **232.50** | 7.4% | 218.94 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **AKSA** | 10.81 | **11.66** | 7.9% | 10.95 | kirilim, rvol2, tepede_kapanis | 14.4% |
| **SOKM** | 57.25 | **61.90** | 8.1% | 57.31 | kirilim, rvol2, tepede_kapanis | 13.2% |
| **TURSG** | 5.89 | **6.40** | 8.7% | 6.02 | kirilim, rvol2, tepede_kapanis | 10.7% |

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
