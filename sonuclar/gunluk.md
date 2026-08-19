# Gunluk Tarama — 19.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-19 16:02

**Taranan gun (kapanis): 19.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 1 hisse

**19.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

| Hisse | Sinyal gunu kapanisi | RVOL | Kapanis konumu | ATR% | Stop (girise gore) |
|---|---|---|---|---|---|
| **SOKM** | 57.50 | 2.13x | 72% | 3.8% | giris - 7.7% |

**Stop nasil kurulur:** giris fiyati acilista belli olacagi icin sabit bir TL degeri verilemez. Gerceklesen alis fiyatini al, tablodaki yuzde kadar asagisina stop koy (= 2 x ATR). Sonra hisse yukseldikce stopu yukari cek, asla asagi indirme.

**Bu sayilar olculdu:** ertesi gun acilistan giris, erken_dar stratejisinde islem basina **+%8.38** beklenti verdi (5 yil, BIST 100). Ayni sinyali kapanista almak +%9.18 veriyordu — aradaki 0.80 puan gecelik boslugun maliyeti.

## 🟡 Izleme listesi (14) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **KCHOL** | 214.60 | **209.50** | -2.4% | 197.40 | rvol2 | 10.0% |
| **ALARK** | 113.10 | **110.70** | -2.1% | 102.72 | tepede_kapanis | 11.6% |
| **BIMAS** | 416.50 | **409.50** | -1.7% | 385.97 | rvol2 | 10.6% |
| **MPARK** | 442.75 | **442.25** | -0.1% | 415.74 | rvol2 | 12.2% |
| **ALTNY** | 17.12 | **17.57** | 2.6% | 16.11 | kirilim | 15.7% |
| **GARAN** | 132.00 | **132.40** | 0.3% | 125.30 | kirilim, rvol2 | 7.6% |
| **YKBNK** | 35.62 | **36.06** | 1.2% | 33.61 | kirilim, rvol2 | 17.1% |
| **SAHOL** | 90.35 | **91.70** | 1.5% | 86.91 | kirilim, rvol2 | 11.7% |
| **ANSGR** | 28.50 | **29.68** | 4.1% | 28.06 | kirilim, rvol2 | 13.5% |
| **DOHOL** | 21.16 | **22.18** | 4.8% | 20.80 | kirilim, rvol2 | 8.8% |
| **IEYHO** | 183.30 | **183.80** | 0.3% | 177.01 | kirilim, rvol2, tepede_kapanis | 15.9% |
| **ENJSA** | 111.00 | **117.40** | 5.8% | 109.95 | kirilim, rvol2, tepede_kapanis | 12.6% |
| **TCELL** | 104.00 | **112.30** | 8.0% | 106.27 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **THYAO** | 301.25 | **330.25** | 9.6% | 313.75 | kirilim, rvol2, tepede_kapanis | 11.9% |

_Kirilim seviyesine %10'den uzak 6 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): TURSG, BSOKE, GRSEL, CCOLA, DOAS, AKSA_

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
