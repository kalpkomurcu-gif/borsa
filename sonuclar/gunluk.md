# Gunluk Tarama — 06.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-07 11:23

**Taranan gun (kapanis): 06.08.2026**

> 07.08.2026 bari tamamlanmamisti (seans suruyor), elendi. Tarama son KAPANAN gune gore: **06.08.2026**.

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**06.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (19) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ANSGR** | 28.22 | **28.38** | 0.6% | 26.87 | kirilim, tepede_kapanis | 8.6% |
| **KCHOL** | 195.90 | **206.80** | 5.6% | 195.28 | kirilim, tepede_kapanis | 13.6% |
| **MAVI** | 38.94 | **41.58** | 6.8% | 39.48 | kirilim, rvol2 | 11.1% |
| **ASELS** | 363.00 | **391.25** | 7.8% | 358.39 | kirilim, rvol2 | 17.9% |
| **MPARK** | 400.00 | **432.75** | 8.2% | 405.52 | kirilim, tepede_kapanis | 9.8% |
| **IEYHO** | 172.50 | **173.00** | 0.3% | 165.23 | kirilim, rvol2, tepede_kapanis | 12.0% |
| **ENJSA** | 113.40 | **114.00** | 0.5% | 106.86 | kirilim, rvol2, tepede_kapanis | 15.0% |
| **DOAS** | 190.20 | **193.90** | 1.9% | 185.22 | kirilim, rvol2, tepede_kapanis | 7.1% |
| **MGROS** | 626.00 | **656.50** | 4.9% | 617.87 | kirilim, rvol2, tepede_kapanis | 9.9% |
| **AEFES** | 21.46 | **22.52** | 4.9% | 21.10 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **GARAN** | 127.80 | **134.40** | 5.2% | 126.84 | kirilim, rvol2, tepede_kapanis | 12.0% |
| **DOHOL** | 20.90 | **22.18** | 6.1% | 20.74 | kirilim, rvol2, tepede_kapanis | 10.6% |
| **BSOKE** | 36.06 | **38.32** | 6.3% | 35.14 | kirilim, rvol2, tepede_kapanis | 16.1% |
| **CCOLA** | 87.70 | **93.50** | 6.6% | 87.47 | kirilim, rvol2, tepede_kapanis | 15.3% |
| **TCELL** | 105.30 | **112.40** | 6.7% | 105.84 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **BIMAS** | 382.25 | **408.25** | 6.8% | 385.65 | kirilim, rvol2, tepede_kapanis | 12.5% |
| **TSKB** | 11.24 | **12.09** | 7.6% | 11.52 | kirilim, rvol2, tepede_kapanis | 12.3% |
| **SISE** | 41.88 | **45.38** | 8.4% | 42.94 | kirilim, rvol2, tepede_kapanis | 10.6% |
| **EREGL** | 41.56 | **45.10** | 8.5% | 42.23 | kirilim, rvol2, tepede_kapanis | 15.5% |

_Kirilim seviyesine %10'den uzak 4 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): ALARK, ALTNY, THYAO, TURSG_

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
