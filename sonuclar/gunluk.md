# Gunluk Tarama — 12.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-12 16:32

**Taranan gun (kapanis): 12.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**12.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (16) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **YKBNK** | 35.70 | **35.32** | -1.1% | 32.84 | rvol2 | 14.7% |
| **DOHOL** | 21.56 | **22.18** | 2.9% | 20.73 | kirilim | 8.8% |
| **KCHOL** | 205.80 | **206.80** | 0.5% | 194.67 | kirilim, rvol2 | 12.0% |
| **GARAN** | 131.00 | **132.40** | 1.1% | 124.98 | kirilim, rvol2 | 10.3% |
| **MPARK** | 432.25 | **439.25** | 1.6% | 411.61 | kirilim, rvol2 | 11.5% |
| **DOAS** | 194.40 | **198.20** | 2.0% | 189.51 | kirilim, tepede_kapanis | 9.4% |
| **ANSGR** | 28.94 | **29.68** | 2.6% | 28.02 | kirilim, rvol2 | 13.5% |
| **ASELS** | 381.00 | **391.25** | 2.7% | 358.07 | kirilim, rvol2 | 17.9% |
| **BSOKE** | 36.38 | **38.32** | 5.3% | 35.17 | kirilim, rvol2 | 14.8% |
| **BIMAS** | 384.00 | **408.25** | 6.3% | 385.92 | kirilim, rvol2 | 9.3% |
| **ALTNY** | 16.38 | **17.57** | 7.3% | 16.23 | kirilim, rvol2 | 17.6% |
| **THYAO** | 308.75 | **333.00** | 7.9% | 315.12 | kirilim, rvol2 | 12.8% |
| **TCELL** | 104.10 | **112.40** | 8.0% | 106.10 | kirilim, rvol2 | 13.6% |
| **IEYHO** | 179.00 | **180.90** | 1.1% | 173.51 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **MAVI** | 39.00 | **41.58** | 6.6% | 39.59 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **ALARK** | 101.50 | **111.00** | 9.4% | 103.47 | kirilim, rvol2, tepede_kapanis | 14.1% |

_Kirilim seviyesine %10'den uzak 4 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): CCOLA, AEFES, TURSG, AKSA_

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
