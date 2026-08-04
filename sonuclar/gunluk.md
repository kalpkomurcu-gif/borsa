# Gunluk Tarama — 03.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-04 11:45

**Taranan gun (kapanis): 03.08.2026**

> 04.08.2026 bari tamamlanmamisti (seans suruyor), elendi. Tarama son KAPANAN gune gore: **03.08.2026**.

Fiyatlar **ham** (duzeltilmemis) kapanistir; aracı kurum ekranindaki fiyatla ayni olmalidir. Gostergeler ise bolunme/bedelsiz duzeltmesi yapilmis seri uzerinde hesaplanir.

## 🟢 BUGUN TETIKLENDI (0)

Tum giris kriterleri bugun saglandi.

Bugun tetiklenen hisse yok.

## 🟡 IZLEME LISTESI (16)

Kurulum tamam, tetik henuz gelmedi. **Asil liste bu:** kirilim gununde almak istiyorsan yarin hangi hisseye bakacagini buradan secersin. `Kirilim` sutunu, 20 gunluk zirveye ne kadar kaldigini gosterir — %0'a yakin olan bir sonraki guclu gunde tetiklenir.

| Hisse | Bugunku fiyat | **ALIM SEVIYESI** | Uzaklik | Stop (bu seviyeden) | Eksik kriter | Baz gen. |
|---|---|---|---|---|---|---|
| **AEFES** | 22.08 | **22.48** | 1.8% | 21.05 | kirilim, rvol2 | 15.8% |
| **DOHOL** | 21.26 | **21.90** | 3.0% | 20.41 | kirilim, tepede_kapanis | 9.2% |
| **MAVI** | 39.14 | **41.58** | 6.2% | 39.44 | kirilim, rvol2 | 11.1% |
| **BSOKE** | 35.80 | **38.32** | 7.0% | 35.10 | kirilim, rvol2 | 16.1% |
| **IEYHO** | 164.30 | **167.00** | 1.6% | 159.36 | kirilim, rvol2, tepede_kapanis | 15.7% |
| **ENJSA** | 109.50 | **111.80** | 2.1% | 105.23 | kirilim, rvol2, tepede_kapanis | 12.8% |
| **AKSA** | 12.32 | **12.65** | 2.7% | 11.78 | kirilim, rvol2, tepede_kapanis | 12.7% |
| **CCOLA** | 90.50 | **93.50** | 3.3% | 87.25 | kirilim, rvol2, tepede_kapanis | 17.2% |
| **ANSGR** | 26.88 | **28.38** | 5.6% | 26.89 | kirilim, rvol2, tepede_kapanis | 8.6% |
| **EREGL** | 42.40 | **45.10** | 6.4% | 42.13 | kirilim, rvol2, tepede_kapanis | 15.5% |
| **ODAS** | 8.69 | **9.26** | 6.6% | 8.54 | kirilim, rvol2, tepede_kapanis | 16.9% |
| **BIMAS** | 383.00 | **408.25** | 6.6% | 385.11 | kirilim, rvol2, tepede_kapanis | 15.6% |
| **DOAS** | 181.50 | **193.90** | 6.8% | 185.43 | kirilim, rvol2, tepede_kapanis | 8.1% |
| **KCHOL** | 191.50 | **205.70** | 7.4% | 194.90 | kirilim, rvol2, tepede_kapanis | 13.0% |
| **MGROS** | 623.00 | **671.50** | 7.8% | 632.57 | kirilim, rvol2, tepede_kapanis | 12.4% |
| **MPARK** | 400.25 | **432.75** | 8.1% | 406.49 | kirilim, rvol2, tepede_kapanis | 9.8% |

_Kirilim seviyesine %10'den uzak 3 hisse listeden cikarildi (tek gunde o mesafeyi kapatmasi beklenmez): ALARK, TURSG, THYAO_

### Nasil kullanilir

1. Bu liste **kapanistan sonra** uretilir.
2. Ertesi gun, hissenin fiyati **ALIM SEVIYESI**'ni gecerse aday olur.
3. **Ama seviyeyi gecmesi tek basina yetmez.** Sinyalin tamamlanmasi icin o gun ayrica hacmin patlamasi (20 gun medyaninin 2 kati) ve kapanisin gun icindeki en yuksek %30'luk dilimde olmasi gerekir. Bu ikisi ancak KAPANISTA belli olur.
4. Yani seviyeyi gun icinde gecerken alirsan, sinyalin onaylanip onaylanmayacagini bilmeden almis olursun. Olcumler kapanis fiyatina gore yapildi; en yakin uygulama kapanisa dogru veya ertesi acilista almaktir.
5. Stop sutunu, alim seviyesinden girildigi varsayimiyla hesaplanmistir (seviye - 2 x ATR).

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
