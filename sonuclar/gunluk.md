# Gunluk Tarama — 09.10.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-10-09 20:19

**Taranan gun (kapanis): 09.10.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**09.10.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (12) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **CCOLA** | 83.75 | **82.55** | -1.4% | 77.56 | rvol2 | 10.7% |
| **MPARK** | 437.25 | **455.75** | 4.2% | 428.52 | kirilim, rvol2 | 12.8% |
| **GARAN** | 129.30 | **135.90** | 5.1% | 128.06 | kirilim, rvol2 | 15.4% |
| **SOKM** | 58.20 | **61.90** | 6.4% | 57.48 | kirilim, rvol2 | 15.7% |
| **ENJSA** | 113.40 | **118.00** | 4.1% | 110.50 | kirilim, rvol2, tepede_kapanis | 15.0% |
| **THYAO** | 287.50 | **302.75** | 5.3% | 286.93 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **EREGL** | 37.32 | **40.00** | 7.2% | 37.45 | kirilim, rvol2, tepede_kapanis | 16.1% |
| **AEFES** | 18.56 | **19.96** | 7.5% | 18.78 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **BRSAN** | 659.00 | **714.50** | 8.4% | 657.11 | kirilim, rvol2, tepede_kapanis | 16.7% |
| **AKSA** | 10.55 | **11.47** | 8.7% | 10.81 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **KCHOL** | 208.00 | **227.60** | 9.4% | 213.96 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **TUPRS** | 386.25 | **424.25** | 9.8% | 393.79 | kirilim, rvol2, tepede_kapanis | 13.7% |

_Kirilim seviyesine %10'den uzak 1 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): BIMAS_

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
