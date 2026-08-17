# Gunluk Tarama — 17.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-17 15:56

**Taranan gun (kapanis): 17.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 1 hisse

**17.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

| Hisse | Sinyal gunu kapanisi | RVOL | Kapanis konumu | ATR% | Stop (girise gore) |
|---|---|---|---|---|---|
| **KRDMD** | 45.62 | 2.46x | 100% | 4.0% | giris - 8.0% |

**Stop nasil kurulur:** giris fiyati acilista belli olacagi icin sabit bir TL degeri verilemez. Gerceklesen alis fiyatini al, tablodaki yuzde kadar asagisina stop koy (= 2 x ATR). Sonra hisse yukseldikce stopu yukari cek, asla asagi indirme.

**Bu sayilar olculdu:** ertesi gun acilistan giris, erken_dar stratejisinde islem basina **+%8.38** beklenti verdi (5 yil, BIST 100). Ayni sinyali kapanista almak +%9.18 veriyordu — aradaki 0.80 puan gecelik boslugun maliyeti.

## 🟡 Izleme listesi (13) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **IEYHO** | 181.90 | **182.00** | 0.1% | 174.74 | kirilim, rvol2 | 16.7% |
| **BIMAS** | 382.00 | **408.25** | 6.9% | 386.71 | kirilim, rvol2 | 10.3% |
| **ENJSA** | 107.80 | **117.40** | 8.9% | 110.01 | kirilim, rvol2 | 15.0% |
| **MPARK** | 438.00 | **439.25** | 0.3% | 412.33 | kirilim, rvol2, tepede_kapanis | 11.5% |
| **KCHOL** | 205.60 | **209.50** | 1.9% | 197.58 | kirilim, rvol2, tepede_kapanis | 10.0% |
| **GARAN** | 129.00 | **132.40** | 2.6% | 125.25 | kirilim, rvol2, tepede_kapanis | 10.3% |
| **SAHOL** | 88.90 | **91.70** | 3.1% | 86.97 | kirilim, rvol2, tepede_kapanis | 11.7% |
| **ANSGR** | 28.40 | **29.68** | 4.5% | 28.04 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **ALARK** | 103.80 | **111.00** | 6.9% | 103.95 | kirilim, rvol2, tepede_kapanis | 12.0% |
| **DOHOL** | 20.70 | **22.18** | 7.1% | 20.77 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **GRSEL** | 343.00 | **368.25** | 7.4% | 344.97 | kirilim, rvol2, tepede_kapanis | 17.1% |
| **TCELL** | 102.90 | **112.30** | 9.1% | 106.16 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **THYAO** | 301.00 | **330.25** | 9.7% | 313.53 | kirilim, rvol2, tepede_kapanis | 11.9% |

_Kirilim seviyesine %10'den uzak 6 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): BSOKE, ALTNY, TURSG, DOAS, AKSA, CCOLA_

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
