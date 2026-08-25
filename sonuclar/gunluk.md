# Gunluk Tarama — 25.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-25 16:17

**Taranan gun (kapanis): 25.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**25.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (16) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **OYAKC** | 22.86 | **22.54** | -1.4% | 21.24 | rvol2 | 12.1% |
| **ALARK** | 105.90 | **116.30** | 9.8% | 108.09 | kirilim | 17.3% |
| **YKBNK** | 36.66 | **36.06** | -1.6% | 33.66 | rvol2, tepede_kapanis | 17.1% |
| **SAHOL** | 93.50 | **92.85** | -0.7% | 88.26 | rvol2, tepede_kapanis | 13.1% |
| **IEYHO** | 190.50 | **189.50** | -0.5% | 182.45 | rvol2, tepede_kapanis | 16.3% |
| **BIMAS** | 417.50 | **419.75** | 0.5% | 396.43 | kirilim, rvol2 | 13.4% |
| **MAVI** | 38.62 | **39.66** | 2.7% | 37.80 | kirilim, rvol2 | 5.8% |
| **KCHOL** | 217.50 | **223.80** | 2.9% | 211.25 | kirilim, rvol2 | 17.5% |
| **GARAN** | 132.60 | **133.40** | 0.6% | 126.31 | kirilim, rvol2, tepede_kapanis | 11.2% |
| **MPARK** | 440.00 | **448.75** | 2.0% | 423.54 | kirilim, rvol2, tepede_kapanis | 13.9% |
| **DOHOL** | 21.02 | **22.18** | 5.5% | 20.82 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **TCELL** | 102.70 | **108.40** | 5.6% | 102.53 | kirilim, rvol2, tepede_kapanis | 9.6% |
| **ANSGR** | 27.72 | **29.68** | 7.1% | 28.11 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **ENJSA** | 108.10 | **117.40** | 8.6% | 109.99 | kirilim, rvol2, tepede_kapanis | 12.6% |
| **THYAO** | 302.50 | **328.75** | 8.7% | 313.71 | kirilim, rvol2, tepede_kapanis | 11.3% |
| **TURSG** | 6.14 | **6.69** | 9.0% | 6.35 | kirilim, rvol2, tepede_kapanis | 8.8% |

_Kirilim seviyesine %10'den uzak 4 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): BSOKE, GRSEL, DOAS, CCOLA_

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
