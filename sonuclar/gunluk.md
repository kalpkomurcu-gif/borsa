# Gunluk Tarama — 07.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-07 19:23

**Taranan gun (kapanis): 07.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**07.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (17) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **PETKM** | 22.06 | **21.08** | -4.4% | 19.43 | rvol2 | 15.8% |
| **TOASO** | 288.00 | **286.50** | -0.5% | 266.94 | rvol2 | 11.5% |
| **TSKB** | 11.11 | **11.34** | 2.1% | 10.82 | kirilim, rvol2 | 6.1% |
| **ALARK** | 113.90 | **116.30** | 2.1% | 108.53 | kirilim, rvol2 | 15.3% |
| **SISE** | 41.66 | **42.58** | 2.2% | 40.13 | kirilim, tepede_kapanis | 12.1% |
| **AKBNK** | 73.05 | **74.85** | 2.5% | 70.46 | kirilim, rvol2 | 16.2% |
| **SAHOL** | 94.05 | **96.50** | 2.6% | 91.98 | kirilim, rvol2 | 12.1% |
| **GARAN** | 133.50 | **137.30** | 2.8% | 130.37 | kirilim, rvol2 | 11.2% |
| **KCHOL** | 219.70 | **226.80** | 3.2% | 215.12 | kirilim, rvol2 | 15.0% |
| **TURSG** | 6.15 | **6.42** | 4.4% | 6.06 | kirilim, rvol2 | 7.9% |
| **EREGL** | 38.32 | **40.10** | 4.6% | 37.61 | kirilim, rvol2 | 10.7% |
| **YKBNK** | 36.26 | **38.02** | 4.9% | 35.75 | kirilim, rvol2 | 15.2% |
| **THYAO** | 296.75 | **312.50** | 5.3% | 297.97 | kirilim, rvol2 | 8.0% |
| **BIMAS** | 418.00 | **422.75** | 1.1% | 400.96 | kirilim, rvol2, tepede_kapanis | 14.2% |
| **DOHOL** | 21.82 | **22.86** | 4.8% | 21.54 | kirilim, rvol2, tepede_kapanis | 11.6% |
| **ENJSA** | 113.00 | **118.60** | 5.0% | 111.00 | kirilim, rvol2, tepede_kapanis | 13.7% |
| **MPARK** | 424.25 | **449.00** | 5.8% | 426.08 | kirilim, rvol2, tepede_kapanis | 10.0% |

_Kirilim seviyesine %10'den uzak 1 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): ANSGR_

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
