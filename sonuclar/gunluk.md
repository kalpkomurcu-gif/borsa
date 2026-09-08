# Gunluk Tarama — 08.09.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-09-08 18:57

**Taranan gun (kapanis): 08.09.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 5 hisse

**08.09.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

| Hisse | Sinyal gunu kapanisi | RVOL | Kapanis konumu | ATR% | Stop (girise gore) |
|---|---|---|---|---|---|
| **SISE** | 45.82 | 4.52x | 100% | 3.0% | giris - 6.0% |
| **ISCTR** | 14.35 | 3.22x | 100% | 2.8% | giris - 5.7% |
| **PETKM** | 24.26 | 3.09x | 100% | 3.8% | giris - 7.7% |
| **AKBNK** | 74.95 | 2.11x | 100% | 3.0% | giris - 6.1% |
| **TSKB** | 11.62 | 2.03x | 100% | 2.4% | giris - 4.9% |

**Stop nasil kurulur:** giris fiyati acilista belli olacagi icin sabit bir TL degeri verilemez. Gerceklesen alis fiyatini al, tablodaki yuzde kadar asagisina stop koy (= 2 x ATR). Sonra hisse yukseldikce stopu yukari cek, asla asagi indirme.

**Bu sayilar olculdu:** ertesi gun acilistan giris, erken_dar stratejisinde islem basina **+%8.38** beklenti verdi (5 yil, BIST 100). Ayni sinyali kapanista almak +%9.18 veriyordu — aradaki 0.80 puan gecelik boslugun maliyeti.

## 🟡 Izleme listesi (15) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **TOASO** | 291.75 | **286.50** | -1.8% | 266.66 | rvol2 | 11.5% |
| **SAHOL** | 96.50 | **96.50** | 0.0% | 91.78 | kirilim, rvol2 | 12.1% |
| **EREGL** | 39.92 | **40.10** | 0.5% | 37.44 | kirilim, rvol2 | 10.7% |
| **BIMAS** | 420.50 | **422.75** | 0.5% | 400.98 | kirilim, rvol2 | 14.2% |
| **ENKAI** | 89.65 | **90.35** | 0.8% | 85.31 | kirilim, rvol2 | 15.1% |
| **KCHOL** | 224.80 | **226.80** | 0.9% | 214.61 | kirilim, rvol2 | 15.0% |
| **GARAN** | 136.00 | **137.30** | 1.0% | 130.18 | kirilim, rvol2 | 11.2% |
| **YKBNK** | 37.62 | **38.02** | 1.1% | 35.65 | kirilim, rvol2 | 15.2% |
| **ALARK** | 115.00 | **116.30** | 1.1% | 108.50 | kirilim, rvol2 | 15.3% |
| **THYAO** | 305.00 | **312.50** | 2.5% | 297.50 | kirilim, rvol2 | 8.0% |
| **ENJSA** | 115.30 | **118.60** | 2.9% | 110.92 | kirilim, rvol2 | 13.7% |
| **TURSG** | 6.24 | **6.42** | 2.9% | 6.05 | kirilim, rvol2 | 7.9% |
| **OYAKC** | 22.44 | **23.28** | 3.7% | 21.91 | kirilim, rvol2 | 14.6% |
| **DOHOL** | 21.76 | **22.86** | 5.1% | 21.49 | kirilim, tepede_kapanis | 11.6% |
| **MPARK** | 427.00 | **449.00** | 5.2% | 425.95 | kirilim, rvol2 | 10.0% |

_Kirilim seviyesine %10'den uzak 2 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): ANSGR, DOAS_

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
