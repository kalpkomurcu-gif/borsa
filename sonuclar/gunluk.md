# Gunluk Tarama — 20.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-20 16:03

**Taranan gun (kapanis): 20.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 1 hisse

**20.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

| Hisse | Sinyal gunu kapanisi | RVOL | Kapanis konumu | ATR% | Stop (girise gore) |
|---|---|---|---|---|---|
| **ALTNY** | 18.63 | 6.14x | 84% | 4.2% | giris - 8.3% |

**Stop nasil kurulur:** giris fiyati acilista belli olacagi icin sabit bir TL degeri verilemez. Gerceklesen alis fiyatini al, tablodaki yuzde kadar asagisina stop koy (= 2 x ATR). Sonra hisse yukseldikce stopu yukari cek, asla asagi indirme.

**Bu sayilar olculdu:** ertesi gun acilistan giris, erken_dar stratejisinde islem basina **+%8.38** beklenti verdi (5 yil, BIST 100). Ayni sinyali kapanista almak +%9.18 veriyordu — aradaki 0.80 puan gecelik boslugun maliyeti.

## 🟡 Izleme listesi (15) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **IEYHO** | 188.00 | **183.90** | -2.2% | 176.81 | rvol2 | 16.0% |
| **KCHOL** | 218.00 | **214.90** | -1.4% | 202.72 | rvol2 | 12.8% |
| **OYAKC** | 22.14 | **22.10** | -0.2% | 20.81 | rvol2, tepede_kapanis | 10.0% |
| **MPARK** | 444.00 | **445.75** | 0.4% | 419.53 | kirilim, rvol2 | 13.1% |
| **BSOKE** | 34.60 | **37.16** | 7.4% | 34.20 | kirilim, rvol2 | 13.4% |
| **ALARK** | 107.70 | **116.30** | 8.0% | 108.00 | kirilim, tepede_kapanis | 17.3% |
| **BIMAS** | 411.00 | **417.25** | 1.5% | 393.22 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **SAHOL** | 90.15 | **91.70** | 1.7% | 87.01 | kirilim, rvol2, tepede_kapanis | 11.7% |
| **GARAN** | 129.30 | **132.80** | 2.7% | 125.66 | kirilim, rvol2, tepede_kapanis | 8.0% |
| **DOHOL** | 21.24 | **22.18** | 4.4% | 20.83 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **ANSGR** | 28.38 | **29.68** | 4.6% | 28.09 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **ENJSA** | 109.10 | **117.40** | 7.6% | 109.93 | kirilim, rvol2, tepede_kapanis | 12.6% |
| **TURSG** | 6.32 | **6.89** | 9.0% | 6.54 | kirilim, rvol2, tepede_kapanis | 12.0% |
| **THYAO** | 301.25 | **328.75** | 9.1% | 312.68 | kirilim, rvol2, tepede_kapanis | 11.3% |
| **TCELL** | 102.80 | **112.30** | 9.2% | 106.30 | kirilim, rvol2, tepede_kapanis | 13.5% |

_Kirilim seviyesine %10'den uzak 3 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): GRSEL, CCOLA, DOAS_

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
