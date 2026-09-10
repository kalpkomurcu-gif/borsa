# Gunluk Tarama — 10.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-10 18:40

**Taranan gun (kapanis): 10.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**10.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (19) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **BIMAS** | 430.00 | **428.50** | -0.3% | 406.89 | rvol2 | 15.7% |
| **MPARK** | 443.00 | **449.00** | 1.4% | 425.23 | kirilim, rvol2 | 10.0% |
| **KCHOL** | 224.30 | **232.50** | 3.7% | 220.07 | kirilim, rvol2 | 17.0% |
| **TOASO** | 290.75 | **295.25** | 1.5% | 275.72 | kirilim, rvol2, tepede_kapanis | 14.9% |
| **ENKAI** | 89.75 | **91.35** | 1.8% | 86.36 | kirilim, rvol2, tepede_kapanis | 16.4% |
| **ENJSA** | 117.00 | **119.10** | 1.8% | 111.43 | kirilim, rvol2, tepede_kapanis | 14.2% |
| **AEFES** | 19.58 | **20.16** | 3.0% | 18.99 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **GARAN** | 133.40 | **137.80** | 3.3% | 130.61 | kirilim, rvol2, tepede_kapanis | 9.5% |
| **EREGL** | 38.98 | **40.36** | 3.5% | 37.70 | kirilim, rvol2, tepede_kapanis | 11.4% |
| **ASELS** | 398.50 | **412.75** | 3.6% | 382.53 | kirilim, rvol2, tepede_kapanis | 14.7% |
| **SAHOL** | 94.80 | **98.40** | 3.8% | 93.59 | kirilim, rvol2, tepede_kapanis | 13.2% |
| **TSKB** | 11.29 | **11.72** | 3.8% | 11.14 | kirilim, rvol2, tepede_kapanis | 9.6% |
| **TURSG** | 6.15 | **6.41** | 4.2% | 6.04 | kirilim, rvol2, tepede_kapanis | 7.9% |
| **THYAO** | 299.25 | **312.50** | 4.4% | 297.69 | kirilim, rvol2, tepede_kapanis | 8.0% |
| **YKBNK** | 36.20 | **38.02** | 5.0% | 35.63 | kirilim, rvol2, tepede_kapanis | 11.8% |
| **OYAKC** | 22.16 | **23.28** | 5.1% | 21.93 | kirilim, rvol2, tepede_kapanis | 11.8% |
| **DOHOL** | 21.64 | **22.86** | 5.6% | 21.51 | kirilim, rvol2, tepede_kapanis | 11.6% |
| **AKBNK** | 72.10 | **76.30** | 5.8% | 71.58 | kirilim, rvol2, tepede_kapanis | 15.9% |
| **CCOLA** | 79.50 | **87.10** | 9.6% | 81.81 | kirilim, rvol2, tepede_kapanis | 15.8% |

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
