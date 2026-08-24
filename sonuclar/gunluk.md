# Gunluk Tarama — 24.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-24 16:07

**Taranan gun (kapanis): 24.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**24.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (18) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **EKGYO** | 20.72 | **19.70** | -4.9% | 18.42 | rvol2 | 12.8% |
| **IEYHO** | 189.90 | **189.50** | -0.2% | 182.59 | rvol2 | 16.3% |
| **SAHOL** | 94.25 | **92.85** | -1.5% | 88.16 | rvol2, tepede_kapanis | 13.1% |
| **YKBNK** | 36.52 | **36.06** | -1.3% | 33.67 | rvol2, tepede_kapanis | 17.1% |
| **AKBNK** | 72.10 | **71.75** | -0.5% | 67.11 | rvol2, tepede_kapanis | 17.0% |
| **TURSG** | 6.18 | **6.69** | 8.3% | 6.34 | kirilim, tepede_kapanis | 8.8% |
| **MPARK** | 445.25 | **448.75** | 0.8% | 423.86 | kirilim, rvol2, tepede_kapanis | 13.9% |
| **OYAKC** | 22.30 | **22.54** | 1.1% | 21.28 | kirilim, rvol2, tepede_kapanis | 12.1% |
| **GARAN** | 131.60 | **133.40** | 1.4% | 126.19 | kirilim, rvol2, tepede_kapanis | 11.2% |
| **BIMAS** | 412.25 | **419.75** | 1.8% | 396.11 | kirilim, rvol2, tepede_kapanis | 13.4% |
| **KCHOL** | 218.80 | **223.80** | 2.3% | 211.42 | kirilim, rvol2, tepede_kapanis | 17.5% |
| **DOHOL** | 21.66 | **22.18** | 2.4% | 20.85 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **TOASO** | 277.25 | **286.00** | 3.2% | 265.56 | kirilim, rvol2, tepede_kapanis | 11.3% |
| **TSKB** | 11.15 | **11.63** | 4.3% | 11.11 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **ANSGR** | 28.32 | **29.68** | 4.8% | 28.14 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **TCELL** | 103.10 | **108.40** | 5.1% | 102.39 | kirilim, rvol2, tepede_kapanis | 9.6% |
| **ENJSA** | 110.60 | **117.40** | 6.1% | 110.12 | kirilim, rvol2, tepede_kapanis | 12.6% |
| **THYAO** | 300.50 | **328.75** | 9.4% | 313.43 | kirilim, rvol2, tepede_kapanis | 11.3% |

_Kirilim seviyesine %10'den uzak 5 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): BSOKE, GRSEL, CCOLA, ALARK, DOAS_

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
