# Gunluk Tarama — 13.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-13 16:31

**Taranan gun (kapanis): 13.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**13.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (20) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ASELS** | 395.75 | **391.25** | -1.1% | 357.98 | rvol2 | 17.9% |
| **IEYHO** | 180.00 | **180.90** | 0.5% | 173.61 | kirilim, rvol2 | 15.1% |
| **ALTNY** | 16.89 | **17.57** | 4.0% | 16.21 | kirilim, rvol2 | 17.6% |
| **KRDMD** | 41.76 | **45.10** | 8.0% | 41.67 | kirilim, rvol2 | 16.5% |
| **AKSA** | 12.29 | **13.28** | 8.1% | 12.41 | kirilim, rvol2 | 15.4% |
| **ALARK** | 102.50 | **111.00** | 8.3% | 103.68 | kirilim, rvol2 | 12.2% |
| **SISE** | 41.64 | **45.38** | 9.0% | 42.99 | kirilim, rvol2 | 13.5% |
| **YKBNK** | 35.54 | **35.78** | 0.7% | 33.17 | kirilim, rvol2, tepede_kapanis | 16.2% |
| **SAHOL** | 88.80 | **90.60** | 2.0% | 85.74 | kirilim, rvol2, tepede_kapanis | 10.4% |
| **MPARK** | 430.00 | **439.25** | 2.2% | 412.00 | kirilim, rvol2, tepede_kapanis | 11.5% |
| **GARAN** | 129.60 | **132.40** | 2.2% | 124.95 | kirilim, rvol2, tepede_kapanis | 7.6% |
| **KCHOL** | 202.40 | **206.80** | 2.2% | 194.72 | kirilim, rvol2, tepede_kapanis | 8.6% |
| **ANSGR** | 28.80 | **29.68** | 3.1% | 28.02 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **DOHOL** | 21.12 | **22.18** | 5.0% | 20.72 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **MAVI** | 38.76 | **41.58** | 7.3% | 39.63 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **THYAO** | 308.00 | **333.00** | 8.1% | 315.64 | kirilim, rvol2, tepede_kapanis | 12.8% |
| **BIMAS** | 376.50 | **408.25** | 8.4% | 385.96 | kirilim, rvol2, tepede_kapanis | 10.5% |
| **TCELL** | 103.10 | **112.40** | 9.0% | 106.15 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **ENJSA** | 107.40 | **117.40** | 9.3% | 110.02 | kirilim, rvol2, tepede_kapanis | 18.0% |
| **BSOKE** | 35.00 | **38.32** | 9.5% | 35.10 | kirilim, rvol2, tepede_kapanis | 14.8% |

_Kirilim seviyesine %10'den uzak 3 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): CCOLA, DOAS, TURSG_

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
