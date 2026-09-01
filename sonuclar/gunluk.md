# Gunluk Tarama — 01.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-01 18:48

**Taranan gun (kapanis): 01.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**01.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (12) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **BIMAS** | 408.25 | **422.75** | 3.6% | 400.04 | kirilim, rvol2 | 14.2% |
| **YKBNK** | 36.82 | **38.02** | 3.3% | 35.73 | kirilim, rvol2, tepede_kapanis | 15.2% |
| **GARAN** | 132.90 | **137.30** | 3.3% | 130.32 | kirilim, rvol2, tepede_kapanis | 11.2% |
| **SAHOL** | 93.20 | **96.50** | 3.5% | 92.05 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **TSKB** | 10.99 | **11.38** | 3.5% | 10.85 | kirilim, rvol2, tepede_kapanis | 6.5% |
| **TURSG** | 6.10 | **6.42** | 5.2% | 6.05 | kirilim, rvol2, tepede_kapanis | 7.9% |
| **KCHOL** | 214.70 | **226.80** | 5.6% | 214.85 | kirilim, rvol2, tepede_kapanis | 17.0% |
| **DOHOL** | 21.64 | **22.86** | 5.6% | 21.45 | kirilim, rvol2, tepede_kapanis | 12.2% |
| **ENJSA** | 110.80 | **118.60** | 7.0% | 110.58 | kirilim, rvol2, tepede_kapanis | 13.7% |
| **ALARK** | 107.90 | **116.30** | 7.8% | 108.44 | kirilim, rvol2, tepede_kapanis | 17.3% |
| **THYAO** | 301.50 | **325.50** | 8.0% | 311.00 | kirilim, rvol2, tepede_kapanis | 10.2% |
| **MPARK** | 413.50 | **449.00** | 8.6% | 425.67 | kirilim, rvol2, tepede_kapanis | 12.8% |

_Kirilim seviyesine %10'den uzak 2 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): ANSGR, EREGL_

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
