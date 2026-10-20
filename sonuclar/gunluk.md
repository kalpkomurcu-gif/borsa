# Gunluk Tarama — 20.10.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-10-20 19:34

**Taranan gun (kapanis): 20.10.2026**

> ⚠️ **1 hissenin 20.10.2026 verisi yok**, taramaya alinmadilar. Parantez ici o hissenin son veri gunu: RALYH(19.10). Bu hisseler icin eski bir barin fiyatini bugunku gibi raporlamaktansa listeden cikarmak dogru olan.

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**20.10.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (12) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ENJSA** | 116.60 | **115.50** | -0.9% | 107.97 | rvol2 | 9.9% |
| **SOKM** | 58.05 | **60.00** | 3.4% | 55.75 | kirilim | 12.1% |
| **GARAN** | 134.60 | **135.90** | 1.0% | 128.74 | kirilim, rvol2 | 10.9% |
| **YKBNK** | 36.66 | **37.42** | 2.1% | 35.17 | kirilim, rvol2 | 11.4% |
| **SAHOL** | 89.20 | **92.40** | 3.6% | 86.83 | kirilim, rvol2 | 11.6% |
| **BRSAN** | 687.00 | **714.50** | 4.0% | 659.41 | kirilim, rvol2 | 15.4% |
| **ALARK** | 105.20 | **111.10** | 5.6% | 103.64 | kirilim, rvol2 | 13.9% |
| **EREGL** | 37.18 | **39.30** | 5.7% | 36.83 | kirilim, rvol2 | 10.7% |
| **MPARK** | 416.50 | **445.50** | 7.0% | 417.86 | kirilim, rvol2 | 11.5% |
| **KCHOL** | 208.40 | **224.30** | 7.6% | 211.33 | kirilim, rvol2 | 11.5% |
| **HALKB** | 44.32 | **47.92** | 8.1% | 44.38 | kirilim, rvol2 | 15.4% |
| **AEFES** | 17.69 | **19.36** | 9.4% | 18.26 | kirilim, rvol2 | 11.5% |

_Kirilim seviyesine %10'den uzak 2 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): CCOLA, TUPRS_

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
