# Gunluk Tarama — 15.10.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-10-15 19:22

**Taranan gun (kapanis): 15.10.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**15.10.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (13) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ENJSA** | 114.70 | **115.50** | 0.7% | 108.43 | kirilim, rvol2 | 10.7% |
| **GARAN** | 133.90 | **135.90** | 1.5% | 128.69 | kirilim, rvol2 | 12.4% |
| **ALARK** | 109.10 | **111.10** | 1.8% | 103.76 | kirilim, rvol2 | 13.9% |
| **YKBNK** | 36.30 | **37.42** | 3.1% | 35.10 | kirilim, rvol2 | 16.5% |
| **EREGL** | 37.40 | **39.30** | 5.1% | 36.91 | kirilim, rvol2 | 13.5% |
| **BRSAN** | 660.50 | **714.50** | 8.2% | 661.68 | kirilim, rvol2 | 15.4% |
| **ASELS** | 351.00 | **386.00** | 10.0% | 354.57 | kirilim, rvol2 | 15.5% |
| **VAKBN** | 34.08 | **35.04** | 2.8% | 32.53 | kirilim, rvol2, tepede_kapanis | 13.9% |
| **SOKM** | 58.00 | **59.95** | 3.4% | 55.67 | kirilim, rvol2, tepede_kapanis | 12.1% |
| **CCOLA** | 79.75 | **84.55** | 6.0% | 79.45 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **KCHOL** | 210.90 | **224.30** | 6.4% | 211.68 | kirilim, rvol2, tepede_kapanis | 9.3% |
| **MPARK** | 427.50 | **455.75** | 6.6% | 430.16 | kirilim, rvol2, tepede_kapanis | 12.8% |
| **AEFES** | 18.07 | **19.40** | 7.4% | 18.31 | kirilim, rvol2, tepede_kapanis | 10.4% |

_Kirilim seviyesine %10'den uzak 3 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): KRDMD, TUPRS, BIMAS_

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
