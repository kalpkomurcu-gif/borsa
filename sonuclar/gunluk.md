# Gunluk Tarama — 15.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-15 19:11

**Taranan gun (kapanis): 15.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**15.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (18) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ASELS** | 377.00 | **412.75** | 9.5% | 382.70 | kirilim, rvol2 | 11.3% |
| **TUPRS** | 412.50 | **423.00** | 2.5% | 395.77 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **TSKB** | 11.23 | **11.72** | 4.4% | 11.12 | kirilim, rvol2, tepede_kapanis | 9.2% |
| **MPARK** | 427.25 | **449.00** | 5.1% | 426.03 | kirilim, rvol2, tepede_kapanis | 10.0% |
| **AEFES** | 18.98 | **19.96** | 5.2% | 18.81 | kirilim, rvol2, tepede_kapanis | 12.5% |
| **BIMAS** | 415.75 | **437.50** | 5.2% | 415.92 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **TOASO** | 284.25 | **299.75** | 5.5% | 279.47 | kirilim, rvol2, tepede_kapanis | 16.6% |
| **EREGL** | 38.26 | **40.36** | 5.5% | 37.79 | kirilim, rvol2, tepede_kapanis | 11.1% |
| **TURSG** | 6.06 | **6.41** | 5.8% | 6.05 | kirilim, rvol2, tepede_kapanis | 7.9% |
| **ENJSA** | 112.80 | **119.60** | 6.0% | 112.18 | kirilim, rvol2, tepede_kapanis | 14.7% |
| **KCHOL** | 218.80 | **232.50** | 6.3% | 220.24 | kirilim, rvol2, tepede_kapanis | 14.6% |
| **DOHOL** | 21.34 | **22.86** | 7.1% | 21.55 | kirilim, rvol2, tepede_kapanis | 11.6% |
| **CCOLA** | 78.00 | **83.70** | 7.3% | 78.42 | kirilim, rvol2, tepede_kapanis | 11.3% |
| **GARAN** | 127.80 | **137.80** | 7.8% | 130.56 | kirilim, rvol2, tepede_kapanis | 7.8% |
| **ANSGR** | 26.78 | **28.88** | 7.8% | 27.49 | kirilim, rvol2, tepede_kapanis | 12.1% |
| **AKSA** | 10.92 | **11.88** | 8.8% | 11.21 | kirilim, rvol2, tepede_kapanis | 13.0% |
| **SAHOL** | 90.30 | **98.40** | 9.0% | 93.40 | kirilim, rvol2, tepede_kapanis | 12.3% |
| **THYAO** | 285.25 | **312.50** | 9.6% | 297.68 | kirilim, rvol2, tepede_kapanis | 8.0% |

_Kirilim seviyesine %10'den uzak 1 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): KRDMD_

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
