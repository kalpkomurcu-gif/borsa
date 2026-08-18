# Gunluk Tarama — 18.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-18 16:01

**Taranan gun (kapanis): 18.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**18.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (13) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **BIMAS** | 405.00 | **408.25** | 0.8% | 385.03 | kirilim | 10.3% |
| **IEYHO** | 183.10 | **182.00** | -0.6% | 174.98 | rvol2, tepede_kapanis | 14.8% |
| **KCHOL** | 207.90 | **209.50** | 0.8% | 197.55 | kirilim, rvol2 | 10.0% |
| **MPARK** | 438.00 | **442.25** | 1.0% | 415.75 | kirilim, rvol2 | 12.2% |
| **ALARK** | 107.00 | **110.70** | 3.5% | 103.38 | kirilim, rvol2 | 11.6% |
| **ENJSA** | 110.50 | **117.40** | 6.2% | 110.09 | kirilim, rvol2 | 17.4% |
| **DOHOL** | 20.82 | **22.18** | 6.5% | 20.79 | kirilim, rvol2 | 8.8% |
| **GARAN** | 129.30 | **132.40** | 2.4% | 125.38 | kirilim, rvol2, tepede_kapanis | 10.3% |
| **SAHOL** | 88.95 | **91.70** | 3.1% | 87.02 | kirilim, rvol2, tepede_kapanis | 11.7% |
| **KRDMD** | 44.00 | **45.62** | 3.7% | 41.82 | kirilim, rvol2, tepede_kapanis | 17.9% |
| **ANSGR** | 28.10 | **29.68** | 5.6% | 28.06 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **TCELL** | 103.50 | **112.30** | 8.5% | 106.24 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **GRSEL** | 338.50 | **368.25** | 8.8% | 344.84 | kirilim, rvol2, tepede_kapanis | 16.3% |

_Kirilim seviyesine %10'den uzak 6 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): CCOLA, THYAO, BSOKE, TURSG, AKSA, DOAS_

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
