# Gunluk Tarama — 17.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-17 19:14

**Taranan gun (kapanis): 17.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**17.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (16) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **TKFEN** | 258.00 | **237.90** | -7.8% | 212.84 | rvol2 | 17.8% |
| **GARAN** | 132.50 | **137.80** | 4.0% | 129.02 | kirilim | 17.0% |
| **TUPRS** | 412.00 | **423.00** | 2.7% | 393.69 | kirilim, rvol2 | 15.4% |
| **CCOLA** | 80.40 | **83.70** | 4.1% | 78.01 | kirilim, rvol2 | 12.2% |
| **TOASO** | 287.00 | **299.75** | 4.4% | 277.30 | kirilim, rvol2 | 16.6% |
| **TSKB** | 11.22 | **11.72** | 4.5% | 10.98 | kirilim, rvol2 | 15.1% |
| **AEFES** | 19.08 | **19.96** | 4.6% | 18.64 | kirilim, rvol2 | 13.0% |
| **AKSA** | 11.12 | **11.66** | 4.9% | 10.91 | kirilim, rvol2 | 14.4% |
| **KCHOL** | 218.70 | **232.50** | 6.3% | 218.17 | kirilim, rvol2 | 16.0% |
| **TURSG** | 6.00 | **6.41** | 6.8% | 6.02 | kirilim, tepede_kapanis | 10.7% |
| **ENJSA** | 111.50 | **119.60** | 7.3% | 111.06 | kirilim, rvol2 | 16.6% |
| **ANSGR** | 26.32 | **28.88** | 9.7% | 27.33 | kirilim, rvol2 | 15.9% |
| **MPARK** | 435.00 | **449.00** | 3.2% | 421.23 | kirilim, rvol2, tepede_kapanis | 11.1% |
| **BIMAS** | 418.00 | **437.50** | 4.7% | 413.39 | kirilim, rvol2, tepede_kapanis | 11.5% |
| **SOKM** | 57.15 | **61.90** | 8.3% | 57.23 | kirilim, rvol2, tepede_kapanis | 14.4% |
| **DOHOL** | 20.86 | **22.86** | 9.6% | 21.45 | kirilim, rvol2, tepede_kapanis | 14.6% |

_Kirilim seviyesine %10'den uzak 1 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): EREGL_

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
