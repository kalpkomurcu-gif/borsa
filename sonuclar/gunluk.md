# Gunluk Tarama — 14.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-14 16:29

**Taranan gun (kapanis): 14.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**14.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (15) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **MPARK** | 438.25 | **439.25** | 0.2% | 411.53 | kirilim, rvol2 | 11.5% |
| **GARAN** | 131.00 | **132.40** | 1.1% | 125.19 | kirilim, rvol2 | 7.6% |
| **KCHOL** | 207.20 | **209.50** | 1.1% | 197.40 | kirilim, rvol2 | 10.0% |
| **IEYHO** | 178.60 | **180.90** | 1.3% | 173.60 | kirilim, rvol2, tepede_kapanis | 16.0% |
| **YKBNK** | 35.42 | **36.06** | 1.8% | 33.53 | kirilim, rvol2, tepede_kapanis | 17.1% |
| **SAHOL** | 89.40 | **91.70** | 2.6% | 86.75 | kirilim, rvol2, tepede_kapanis | 11.7% |
| **ANSGR** | 28.68 | **29.68** | 3.5% | 28.05 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **ALTNY** | 16.77 | **17.57** | 4.8% | 16.22 | kirilim, rvol2, tepede_kapanis | 16.2% |
| **DOHOL** | 20.86 | **22.18** | 6.3% | 20.73 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **ALARK** | 103.40 | **111.00** | 7.4% | 103.72 | kirilim, rvol2, tepede_kapanis | 12.2% |
| **TCELL** | 104.10 | **112.40** | 8.0% | 106.27 | kirilim, rvol2, tepede_kapanis | 13.6% |
| **KRDMD** | 41.48 | **45.10** | 8.7% | 41.66 | kirilim, rvol2, tepede_kapanis | 16.5% |
| **BIMAS** | 374.75 | **408.25** | 8.9% | 386.59 | kirilim, rvol2, tepede_kapanis | 10.3% |
| **THYAO** | 305.25 | **333.00** | 9.1% | 315.59 | kirilim, rvol2, tepede_kapanis | 12.8% |
| **SISE** | 41.40 | **45.38** | 9.6% | 42.94 | kirilim, rvol2, tepede_kapanis | 13.5% |

_Kirilim seviyesine %10'den uzak 6 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): AKSA, BSOKE, ENJSA, TURSG, CCOLA, DOAS_

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
