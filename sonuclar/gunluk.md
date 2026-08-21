# Gunluk Tarama — 21.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-21 16:03

**Taranan gun (kapanis): 21.08.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**21.08.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (14) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **KCHOL** | 222.40 | **219.10** | -1.5% | 206.94 | rvol2 | 15.0% |
| **SAHOL** | 92.40 | **91.70** | -0.8% | 87.08 | rvol2 | 11.7% |
| **BIMAS** | 416.50 | **419.75** | 0.8% | 396.02 | kirilim, rvol2 | 13.4% |
| **ALARK** | 106.30 | **116.30** | 9.4% | 108.09 | kirilim, tepede_kapanis | 17.3% |
| **MPARK** | 445.00 | **445.75** | 0.2% | 420.34 | kirilim, rvol2, tepede_kapanis | 13.1% |
| **IEYHO** | 186.50 | **189.50** | 1.6% | 182.60 | kirilim, rvol2, tepede_kapanis | 18.0% |
| **TOASO** | 281.25 | **287.25** | 2.1% | 266.89 | kirilim, rvol2, tepede_kapanis | 11.8% |
| **DOHOL** | 21.60 | **22.18** | 2.7% | 20.82 | kirilim, rvol2, tepede_kapanis | 8.8% |
| **GARAN** | 129.90 | **133.40** | 2.7% | 126.33 | kirilim, rvol2, tepede_kapanis | 11.2% |
| **TCELL** | 104.30 | **108.40** | 3.9% | 102.41 | kirilim, rvol2, tepede_kapanis | 9.6% |
| **ANSGR** | 28.50 | **29.68** | 4.1% | 28.11 | kirilim, rvol2, tepede_kapanis | 13.5% |
| **TURSG** | 6.33 | **6.71** | 6.0% | 6.37 | kirilim, rvol2, tepede_kapanis | 9.1% |
| **ENJSA** | 110.40 | **117.40** | 6.3% | 109.94 | kirilim, rvol2, tepede_kapanis | 12.6% |
| **THYAO** | 301.00 | **328.75** | 9.2% | 313.41 | kirilim, rvol2, tepede_kapanis | 11.3% |

_Kirilim seviyesine %10'den uzak 4 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): CCOLA, BSOKE, GRSEL, DOAS_

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
