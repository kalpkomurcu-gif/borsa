# Gunluk Tarama — 22.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-22 19:07

**Taranan gun (kapanis): 22.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**22.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (15) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **EREGL** | 37.82 | **40.36** | 6.7% | 37.54 | kirilim, rvol2 | 17.2% |
| **ENJSA** | 109.10 | **119.60** | 9.6% | 111.37 | kirilim, rvol2 | 16.6% |
| **BIMAS** | 430.25 | **437.50** | 1.7% | 412.72 | kirilim, rvol2, tepede_kapanis | 11.5% |
| **GARAN** | 133.90 | **137.80** | 2.9% | 129.04 | kirilim, rvol2, tepede_kapanis | 17.0% |
| **CCOLA** | 78.60 | **81.70** | 3.9% | 76.25 | kirilim, rvol2, tepede_kapanis | 9.5% |
| **MPARK** | 437.75 | **455.75** | 4.1% | 428.46 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **KCHOL** | 221.10 | **232.50** | 5.2% | 218.37 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **TURSG** | 6.08 | **6.40** | 5.3% | 6.01 | kirilim, rvol2, tepede_kapanis | 10.7% |
| **TOASO** | 283.75 | **299.75** | 5.6% | 277.36 | kirilim, rvol2, tepede_kapanis | 16.6% |
| **AEFES** | 18.83 | **19.96** | 6.0% | 18.65 | kirilim, rvol2, tepede_kapanis | 13.0% |
| **TRENJ** | 106.30 | **113.00** | 6.3% | 102.96 | kirilim, rvol2, tepede_kapanis | 17.5% |
| **TUPRS** | 397.00 | **424.25** | 6.9% | 392.52 | kirilim, rvol2, tepede_kapanis | 15.8% |
| **AKSA** | 10.91 | **11.66** | 6.9% | 10.93 | kirilim, rvol2, tepede_kapanis | 14.4% |
| **SOKM** | 57.60 | **61.90** | 7.5% | 57.21 | kirilim, rvol2, tepede_kapanis | 13.2% |
| **ANSGR** | 25.96 | **28.46** | 9.6% | 26.81 | kirilim, rvol2, tepede_kapanis | 14.2% |

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
