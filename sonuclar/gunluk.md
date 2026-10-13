# Gunluk Tarama — 13.10.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-10-13 20:49

**Taranan gun (kapanis): 13.10.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**13.10.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (14) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **CCOLA** | 83.65 | **84.35** | 0.8% | 79.44 | kirilim, rvol2 | 13.1% |
| **ENJSA** | 114.40 | **115.50** | 1.0% | 108.24 | kirilim, rvol2 | 12.6% |
| **GARAN** | 131.30 | **135.90** | 3.5% | 128.50 | kirilim, rvol2 | 15.4% |
| **KCHOL** | 212.50 | **226.90** | 6.8% | 213.72 | kirilim, rvol2 | 13.2% |
| **BIMAS** | 411.25 | **443.25** | 7.8% | 420.26 | kirilim, rvol2 | 13.7% |
| **VAKBN** | 34.40 | **35.86** | 4.2% | 33.26 | kirilim, rvol2, tepede_kapanis | 17.6% |
| **SOKM** | 57.95 | **60.80** | 4.9% | 56.51 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **EREGL** | 37.26 | **39.30** | 5.5% | 36.83 | kirilim, rvol2, tepede_kapanis | 14.1% |
| **ALARK** | 108.40 | **114.40** | 5.5% | 106.81 | kirilim, rvol2, tepede_kapanis | 17.3% |
| **THYAO** | 286.25 | **302.75** | 5.8% | 287.86 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **MPARK** | 429.50 | **455.75** | 6.1% | 429.27 | kirilim, rvol2, tepede_kapanis | 12.8% |
| **AEFES** | 18.50 | **19.80** | 7.0% | 18.67 | kirilim, rvol2, tepede_kapanis | 12.6% |
| **BRSAN** | 660.00 | **714.50** | 8.3% | 659.50 | kirilim, rvol2, tepede_kapanis | 16.7% |
| **TUPRS** | 385.75 | **424.25** | 10.0% | 393.60 | kirilim, rvol2, tepede_kapanis | 13.7% |

_Kirilim seviyesine %10'den uzak 2 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): ASELS, HALKB_

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
