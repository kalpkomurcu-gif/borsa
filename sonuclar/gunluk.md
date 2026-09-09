# Gunluk Tarama — 09.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-09 18:50

**Taranan gun (kapanis): 09.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**09.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (18) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **BIMAS** | 427.50 | **422.75** | -1.1% | 400.92 | rvol2 | 14.2% |
| **TOASO** | 292.75 | **291.75** | -0.3% | 271.98 | rvol2 | 13.5% |
| **ENJSA** | 118.60 | **118.60** | 0.0% | 110.91 | kirilim, rvol2 | 13.7% |
| **AKBNK** | 72.95 | **74.95** | 2.7% | 70.27 | kirilim, tepede_kapanis | 16.4% |
| **DOHOL** | 21.50 | **22.86** | 6.3% | 21.49 | kirilim, tepede_kapanis | 11.6% |
| **ALARK** | 116.30 | **116.30** | 0.0% | 108.30 | kirilim, rvol2, tepede_kapanis | 15.3% |
| **ENKAI** | 90.35 | **90.35** | 0.0% | 85.31 | kirilim, rvol2, tepede_kapanis | 15.1% |
| **SAHOL** | 96.05 | **96.50** | 0.5% | 91.74 | kirilim, rvol2, tepede_kapanis | 12.1% |
| **KCHOL** | 223.70 | **226.80** | 1.4% | 214.15 | kirilim, rvol2, tepede_kapanis | 15.0% |
| **ODAS** | 7.67 | **7.80** | 1.7% | 7.15 | kirilim, rvol2, tepede_kapanis | 11.9% |
| **TSKB** | 11.39 | **11.62** | 2.0% | 11.04 | kirilim, rvol2, tepede_kapanis | 8.7% |
| **TURSG** | 6.27 | **6.41** | 2.2% | 6.05 | kirilim, rvol2, tepede_kapanis | 7.9% |
| **GARAN** | 134.30 | **137.30** | 2.2% | 130.14 | kirilim, rvol2, tepede_kapanis | 11.2% |
| **EREGL** | 39.08 | **40.36** | 3.3% | 37.69 | kirilim, rvol2, tepede_kapanis | 11.4% |
| **MPARK** | 434.75 | **449.00** | 3.3% | 425.48 | kirilim, rvol2, tepede_kapanis | 10.0% |
| **THYAO** | 301.00 | **312.50** | 3.8% | 297.65 | kirilim, rvol2, tepede_kapanis | 8.0% |
| **YKBNK** | 36.60 | **38.02** | 3.9% | 35.63 | kirilim, rvol2, tepede_kapanis | 15.2% |
| **OYAKC** | 22.38 | **23.28** | 4.0% | 21.93 | kirilim, rvol2, tepede_kapanis | 14.6% |

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
