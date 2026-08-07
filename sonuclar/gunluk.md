# Gunluk Tarama — 07.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-07 16:30

**Taranan gun (kapanis): 07.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**07.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (17) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **DOAS** | 194.30 | **193.90** | -0.2% | 185.18 | rvol2 | 7.1% |
| **ANSGR** | 28.60 | **28.70** | 0.3% | 27.17 | kirilim | 9.8% |
| **MPARK** | 426.75 | **432.75** | 1.4% | 404.03 | kirilim | 9.8% |
| **MGROS** | 654.50 | **656.50** | 0.3% | 616.96 | kirilim, rvol2 | 9.9% |
| **KCHOL** | 198.50 | **206.80** | 4.2% | 195.36 | kirilim, tepede_kapanis | 13.6% |
| **MAVI** | 39.14 | **41.58** | 6.2% | 39.52 | kirilim, rvol2 | 11.1% |
| **BSOKE** | 35.88 | **38.32** | 6.8% | 35.20 | kirilim, tepede_kapanis | 16.1% |
| **ALARK** | 101.80 | **111.00** | 9.0% | 103.96 | kirilim, rvol2 | 14.3% |
| **IEYHO** | 174.20 | **174.30** | 0.1% | 166.63 | kirilim, rvol2, tepede_kapanis | 11.7% |
| **ENJSA** | 113.20 | **115.50** | 2.0% | 108.40 | kirilim, rvol2, tepede_kapanis | 16.5% |
| **GARAN** | 127.00 | **132.40** | 4.3% | 124.96 | kirilim, rvol2, tepede_kapanis | 10.3% |
| **AEFES** | 21.58 | **22.52** | 4.4% | 21.13 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **CCOLA** | 89.00 | **93.50** | 5.1% | 87.49 | kirilim, rvol2, tepede_kapanis | 15.3% |
| **BIMAS** | 385.75 | **408.25** | 5.8% | 385.88 | kirilim, rvol2, tepede_kapanis | 12.5% |
| **TCELL** | 105.10 | **112.40** | 6.9% | 105.95 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **DOHOL** | 20.50 | **22.18** | 8.2% | 20.74 | kirilim, rvol2, tepede_kapanis | 10.6% |
| **TSKB** | 11.12 | **12.09** | 8.7% | 11.53 | kirilim, rvol2, tepede_kapanis | 12.3% |

_Kirilim seviyesine %10'den uzak 5 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): EREGL, ALTNY, ASELS, TURSG, THYAO_

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
