# Gunluk Tarama — 11.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-11 16:30

**Taranan gun (kapanis): 11.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**11.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (18) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ENJSA** | 110.00 | **115.50** | 5.0% | 108.10 | kirilim, tepede_kapanis | 16.5% |
| **AKSA** | 12.41 | **13.28** | 7.0% | 12.42 | kirilim, rvol2 | 15.4% |
| **CCOLA** | 86.65 | **93.50** | 7.9% | 87.33 | kirilim, tepede_kapanis | 14.6% |
| **ASELS** | 356.25 | **391.25** | 9.8% | 358.75 | kirilim, rvol2 | 17.9% |
| **IEYHO** | 178.80 | **178.80** | 0.0% | 171.09 | kirilim, rvol2, tepede_kapanis | 14.6% |
| **DOAS** | 193.90 | **198.20** | 2.2% | 189.37 | kirilim, rvol2, tepede_kapanis | 9.4% |
| **KCHOL** | 199.90 | **206.80** | 3.5% | 194.90 | kirilim, rvol2, tepede_kapanis | 12.0% |
| **MPARK** | 423.00 | **439.25** | 3.8% | 410.90 | kirilim, rvol2, tepede_kapanis | 11.5% |
| **ANSGR** | 28.20 | **29.50** | 4.6% | 27.89 | kirilim, rvol2, tepede_kapanis | 12.9% |
| **ALARK** | 104.70 | **111.00** | 6.0% | 103.38 | kirilim, rvol2, tepede_kapanis | 14.1% |
| **BSOKE** | 36.08 | **38.32** | 6.2% | 35.21 | kirilim, rvol2, tepede_kapanis | 14.8% |
| **MGROS** | 630.00 | **671.00** | 6.5% | 629.71 | kirilim, rvol2, tepede_kapanis | 12.3% |
| **DOHOL** | 20.80 | **22.18** | 6.6% | 20.76 | kirilim, rvol2, tepede_kapanis | 9.3% |
| **MAVI** | 38.94 | **41.58** | 6.8% | 39.58 | kirilim, rvol2, tepede_kapanis | 9.4% |
| **AEFES** | 21.02 | **22.52** | 7.1% | 21.09 | kirilim, rvol2, tepede_kapanis | 14.5% |
| **BIMAS** | 377.25 | **408.25** | 8.2% | 386.39 | kirilim, rvol2, tepede_kapanis | 11.8% |
| **TCELL** | 103.10 | **112.40** | 9.0% | 106.10 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **ALTNY** | 16.01 | **17.57** | 9.7% | 16.20 | kirilim, rvol2, tepede_kapanis | 16.2% |

_Kirilim seviyesine %10'den uzak 2 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): TURSG, THYAO_

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
