# Gunluk Tarama — 03.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-04 11:55

**Taranan gun (kapanis): 03.08.2026**

> Tarama **03.08.2026** tarihine gore yapildi (sonraki gunler veriden cikarildi).

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 1 hisse

**03.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

| Hisse | Sinyal gunu kapanisi | RVOL | Kapanis konumu | ATR% | Stop (girise gore) |
|---|---|---|---|---|---|
| **AKSA** | 13.00 | 2.55x | 97% | 3.5% | giris - 6.9% |

**Stop nasil kurulur:** giris fiyati acilista belli olacagi icin sabit bir TL degeri verilemez. Gerceklesen alis fiyatini al, tablodaki yuzde kadar asagisina stop koy (= 2 x ATR). Sonra hisse yukseldikce stopu yukari cek, asla asagi indirme.

**Bu sayilar olculdu:** ertesi gun acilistan giris, erken_dar stratejisinde islem basina **+%8.38** beklenti verdi (5 yil, BIST 100). Ayni sinyali kapanista almak +%9.18 veriyordu — aradaki 0.80 puan gecelik boslugun maliyeti.

## 🟡 Izleme listesi (16) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **IEYHO** | 167.50 | **167.00** | -0.3% | 159.28 | rvol2, tepede_kapanis | 15.7% |
| **DOAS** | 190.40 | **193.90** | 1.8% | 184.96 | kirilim, rvol2 | 7.1% |
| **CCOLA** | 91.05 | **93.50** | 2.7% | 87.30 | kirilim, rvol2 | 17.2% |
| **AEFES** | 21.88 | **22.48** | 2.7% | 21.05 | kirilim, rvol2 | 15.8% |
| **ANSGR** | 27.20 | **28.38** | 4.3% | 26.89 | kirilim, rvol2 | 8.6% |
| **KCHOL** | 196.90 | **205.70** | 4.5% | 194.90 | kirilim, rvol2 | 13.0% |
| **BIMAS** | 390.25 | **408.25** | 4.6% | 385.17 | kirilim, rvol2 | 15.6% |
| **MGROS** | 625.50 | **661.50** | 5.8% | 622.82 | kirilim, rvol2 | 10.7% |
| **DOHOL** | 20.92 | **22.18** | 6.0% | 20.66 | kirilim, tepede_kapanis | 10.6% |
| **MPARK** | 405.00 | **432.75** | 6.9% | 407.13 | kirilim, rvol2 | 9.8% |
| **BSOKE** | 35.56 | **38.32** | 7.8% | 35.11 | kirilim, rvol2 | 16.1% |
| **SISE** | 41.74 | **45.38** | 8.7% | 42.82 | kirilim, rvol2 | 10.3% |
| **ALARK** | 101.00 | **111.00** | 9.9% | 103.73 | kirilim, rvol2 | 14.3% |
| **ENJSA** | 108.90 | **111.80** | 2.7% | 105.04 | kirilim, rvol2, tepede_kapanis | 12.8% |
| **EREGL** | 42.54 | **45.10** | 6.0% | 42.17 | kirilim, rvol2, tepede_kapanis | 15.5% |
| **MAVI** | 39.12 | **41.58** | 6.3% | 39.44 | kirilim, rvol2, tepede_kapanis | 11.1% |

_Kirilim seviyesine %10'den uzak 3 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): THYAO, TURSG, ODAS_

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
