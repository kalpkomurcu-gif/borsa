# Gunluk Tarama — 23.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-23 19:13

**Taranan gun (kapanis): 23.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**23.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (15) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **TUPRS** | 411.00 | **424.25** | 3.2% | 391.95 | kirilim, rvol2 | 15.8% |
| **SOKM** | 58.55 | **61.90** | 5.7% | 57.26 | kirilim, rvol2 | 13.2% |
| **MAVI** | 38.78 | **39.02** | 0.6% | 36.21 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **BIMAS** | 433.75 | **443.25** | 2.2% | 418.93 | kirilim, rvol2, tepede_kapanis | 13.7% |
| **GARAN** | 133.80 | **137.80** | 3.0% | 129.20 | kirilim, rvol2, tepede_kapanis | 17.0% |
| **EREGL** | 38.54 | **40.36** | 4.7% | 37.52 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **CCOLA** | 77.85 | **81.70** | 4.9% | 76.34 | kirilim, rvol2, tepede_kapanis | 9.5% |
| **KCHOL** | 221.10 | **232.50** | 5.2% | 218.68 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **MPARK** | 433.25 | **455.75** | 5.2% | 429.08 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **AKSA** | 11.00 | **11.66** | 6.0% | 10.94 | kirilim, rvol2, tepede_kapanis | 14.4% |
| **AEFES** | 18.82 | **19.96** | 6.1% | 18.67 | kirilim, rvol2, tepede_kapanis | 13.0% |
| **TURSG** | 6.02 | **6.40** | 6.3% | 6.01 | kirilim, rvol2, tepede_kapanis | 10.7% |
| **TOASO** | 279.00 | **299.75** | 7.4% | 277.50 | kirilim, rvol2, tepede_kapanis | 16.6% |
| **ANSGR** | 25.82 | **28.22** | 9.3% | 26.61 | kirilim, rvol2, tepede_kapanis | 13.2% |
| **ENJSA** | 109.10 | **119.60** | 9.6% | 111.53 | kirilim, rvol2, tepede_kapanis | 16.6% |

_Kirilim seviyesine %10'den uzak 1 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): DOHOL_

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
