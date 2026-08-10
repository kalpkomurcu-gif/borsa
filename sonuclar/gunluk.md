# Gunluk Tarama — 10.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-10 16:28

**Taranan gun (kapanis): 10.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 1 hisse

**10.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

| Hisse | Sinyal gunu kapanisi | RVOL | Kapanis konumu | ATR% | Stop (girise gore) |
|---|---|---|---|---|---|
| **BRSAN** | 629.00 | 3.30x | 100% | 4.0% | giris - 8.0% |

**Stop nasil kurulur:** giris fiyati acilista belli olacagi icin sabit bir TL degeri verilemez. Gerceklesen alis fiyatini al, tablodaki yuzde kadar asagisina stop koy (= 2 x ATR). Sonra hisse yukseldikce stopu yukari cek, asla asagi indirme.

**Bu sayilar olculdu:** ertesi gun acilistan giris, erken_dar stratejisinde islem basina **+%8.38** beklenti verdi (5 yil, BIST 100). Ayni sinyali kapanista almak +%9.18 veriyordu — aradaki 0.80 puan gecelik boslugun maliyeti.

## 🟡 Izleme listesi (18) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **ANSGR** | 29.38 | **28.70** | -2.3% | 27.16 | rvol2 | 9.8% |
| **IEYHO** | 178.30 | **175.40** | -1.6% | 167.55 | rvol2 | 12.4% |
| **ALARK** | 107.00 | **111.00** | 3.7% | 103.56 | kirilim | 14.3% |
| **MGROS** | 658.00 | **656.50** | -0.2% | 616.30 | rvol2, tepede_kapanis | 9.9% |
| **DOAS** | 194.10 | **194.90** | 0.4% | 186.08 | kirilim, tepede_kapanis | 7.7% |
| **MPARK** | 429.25 | **432.75** | 0.8% | 403.67 | kirilim, tepede_kapanis | 9.8% |
| **KCHOL** | 203.90 | **206.80** | 1.4% | 195.07 | kirilim, rvol2 | 13.6% |
| **BSOKE** | 36.50 | **38.32** | 5.0% | 35.17 | kirilim, tepede_kapanis | 16.1% |
| **ALTNY** | 16.20 | **17.57** | 8.5% | 16.18 | kirilim, rvol2 | 16.2% |
| **ENJSA** | 113.10 | **115.50** | 2.1% | 108.63 | kirilim, rvol2, tepede_kapanis | 16.5% |
| **AEFES** | 21.72 | **22.52** | 3.7% | 21.12 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **CCOLA** | 90.05 | **93.50** | 3.8% | 87.53 | kirilim, rvol2, tepede_kapanis | 15.3% |
| **DOHOL** | 21.10 | **22.18** | 5.1% | 20.75 | kirilim, rvol2, tepede_kapanis | 10.6% |
| **BIMAS** | 384.25 | **408.25** | 6.2% | 386.21 | kirilim, rvol2, tepede_kapanis | 12.5% |
| **MAVI** | 39.10 | **41.58** | 6.3% | 39.54 | kirilim, rvol2, tepede_kapanis | 11.1% |
| **TCELL** | 105.30 | **112.40** | 6.7% | 106.11 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **SISE** | 41.48 | **45.38** | 9.4% | 42.96 | kirilim, rvol2, tepede_kapanis | 10.3% |
| **ASELS** | 356.25 | **391.25** | 9.8% | 358.19 | kirilim, rvol2, tepede_kapanis | 17.9% |

_Kirilim seviyesine %10'den uzak 3 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): EREGL, TURSG, THYAO_

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
