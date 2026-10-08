# Gunluk Tarama — 08.10.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-10-08 20:48

**Taranan gun (kapanis): 08.10.2026**

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 ALIM LISTESI — 0 hisse

**08.10.2026 kapanisinda tum kriterler saglandi. Bu hisseler ERTESI ISLEM GUNU ACILISTA alinir.**

Bugun tetiklenen hisse yok — **alim yok.**

Bu normaldir. 5 yillik olcumde erken_dar stratejisi 360 sinyal uretti, yani ortalama ayda ~6. Sinyalsiz gunler cogunluktadir; sinyal uretmek icin kriter gevsetmek sistemi bozar.

## 🟡 Izleme listesi (12) — bilgi amacli

Kurulum tamam (dar baz + zirveye yakin), tetik gelmedi. **Buradan alim YAPILMAZ** — alim listesi yukaridaki.

Bu liste sadece "hangi hisseler kurulmus durumda" sorusunu cevaplar. Alim seviyesine yakin olmak sinyal degildir: hacim ve tepede kapanis o gun ayrica gerceklesmeli ve bu ancak kapanista belli olur.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **KCHOL** | 212.40 | **227.60** | 7.2% | 214.13 | kirilim, rvol2 | 13.5% |
| **BRSAN** | 670.50 | **721.50** | 7.6% | 663.69 | kirilim, rvol2 | 17.9% |
| **AEFES** | 18.36 | **19.96** | 8.7% | 18.77 | kirilim, rvol2 | 13.5% |
| **SAHOL** | 88.75 | **96.60** | 8.8% | 91.21 | kirilim, rvol2 | 17.4% |
| **AKSA** | 10.49 | **11.47** | 9.3% | 10.80 | kirilim, rvol2 | 12.7% |
| **CCOLA** | 80.40 | **82.55** | 2.7% | 77.71 | kirilim, rvol2, tepede_kapanis | 10.7% |
| **ENJSA** | 113.00 | **119.60** | 5.8% | 111.98 | kirilim, rvol2, tepede_kapanis | 16.6% |
| **GARAN** | 128.50 | **136.10** | 5.9% | 128.09 | kirilim, rvol2, tepede_kapanis | 15.5% |
| **THYAO** | 284.25 | **304.00** | 6.9% | 287.92 | kirilim, rvol2, tepede_kapanis | 17.7% |
| **TUPRS** | 392.25 | **424.25** | 8.2% | 393.49 | kirilim, rvol2, tepede_kapanis | 13.7% |
| **MPARK** | 420.25 | **455.75** | 8.4% | 429.05 | kirilim, rvol2, tepede_kapanis | 12.8% |
| **EREGL** | 36.60 | **40.00** | 9.3% | 37.42 | kirilim, rvol2, tepede_kapanis | 16.1% |

_Kirilim seviyesine %10'den uzak 1 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): BIMAS_

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
