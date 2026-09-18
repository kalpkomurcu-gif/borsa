# Gunluk Tarama — 18.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-18 18:38

**Taranan gun (kapanis): 18.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**18.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (13) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **TKFEN** | 244.80 | **237.90** | -2.8% | 211.78 | tepede_kapanis | 17.8% |
| **ANSGR** | 27.10 | **28.88** | 6.6% | 27.34 | kirilim | 15.9% |
| **TUPRS** | 417.25 | **423.00** | 1.4% | 393.41 | kirilim, rvol2 | 15.4% |
| **MPARK** | 436.75 | **449.00** | 2.8% | 423.25 | kirilim, rvol2 | 11.1% |
| **BIMAS** | 419.75 | **437.50** | 4.2% | 413.99 | kirilim, rvol2 | 11.5% |
| **TURSG** | 6.14 | **6.41** | 4.4% | 6.04 | kirilim, rvol2 | 10.7% |
| **CCOLA** | 80.00 | **83.70** | 4.6% | 78.27 | kirilim, rvol2 | 12.2% |
| **SOKM** | 58.80 | **61.90** | 5.3% | 57.40 | kirilim, rvol2 | 13.1% |
| **TOASO** | 284.50 | **299.75** | 5.4% | 277.63 | kirilim, rvol2, tepede_kapanis | 16.6% |
| **GARAN** | 129.90 | **137.80** | 6.1% | 129.01 | kirilim, rvol2, tepede_kapanis | 17.0% |
| **AEFES** | 18.79 | **19.96** | 6.2% | 18.71 | kirilim, rvol2, tepede_kapanis | 13.0% |
| **AKSA** | 10.85 | **11.66** | 7.5% | 10.94 | kirilim, rvol2, tepede_kapanis | 14.4% |
| **KCHOL** | 214.70 | **232.50** | 8.3% | 218.55 | kirilim, rvol2, tepede_kapanis | 16.0% |

_Kirilim seviyesine %10'den uzak 4 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): DOHOL, TRENJ, ENJSA, EREGL_

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
