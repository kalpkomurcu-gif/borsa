# Gunluk Tarama — 05.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-05 20:41

**Taranan gun (kapanis): 05.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**05.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (19) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ENJSA** | 113.00 | **111.80** | -1.1% | 104.71 | rvol2 | 12.8% |
| **KCHOL** | 206.00 | **205.70** | -0.1% | 194.67 | rvol2 | 13.0% |
| **ANSGR** | 28.32 | **28.38** | 0.2% | 26.88 | kirilim | 8.6% |
| **DOAS** | 191.80 | **193.90** | 1.1% | 185.03 | kirilim, rvol2 | 7.1% |
| **MGROS** | 631.00 | **656.50** | 4.0% | 617.32 | kirilim, rvol2 | 9.9% |
| **CCOLA** | 87.95 | **93.50** | 6.3% | 87.38 | kirilim, rvol2 | 17.2% |
| **MPARK** | 406.00 | **432.75** | 6.6% | 407.27 | kirilim, tepede_kapanis | 9.8% |
| **SAHOL** | 89.10 | **95.05** | 6.7% | 90.01 | kirilim, rvol2 | 15.8% |
| **BSOKE** | 35.70 | **38.32** | 7.3% | 35.14 | kirilim, tepede_kapanis | 16.1% |
| **EREGL** | 41.98 | **45.10** | 7.4% | 42.17 | kirilim, rvol2 | 15.5% |
| **IEYHO** | 171.00 | **171.10** | 0.1% | 163.37 | kirilim, rvol2, tepede_kapanis | 10.8% |
| **DOHOL** | 21.08 | **22.18** | 5.2% | 20.71 | kirilim, rvol2, tepede_kapanis | 10.6% |
| **GARAN** | 129.70 | **136.50** | 5.2% | 128.91 | kirilim, rvol2, tepede_kapanis | 13.8% |
| **AEFES** | 21.32 | **22.52** | 5.6% | 21.09 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **BIMAS** | 382.25 | **408.25** | 6.8% | 385.33 | kirilim, rvol2, tepede_kapanis | 12.5% |
| **SISE** | 42.44 | **45.38** | 6.9% | 42.93 | kirilim, rvol2, tepede_kapanis | 10.6% |
| **TCELL** | 105.10 | **112.40** | 6.9% | 105.77 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **TSKB** | 11.27 | **12.09** | 7.3% | 11.50 | kirilim, rvol2, tepede_kapanis | 12.3% |
| **ALARK** | 101.10 | **111.00** | 9.8% | 103.84 | kirilim, rvol2, tepede_kapanis | 14.3% |

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
