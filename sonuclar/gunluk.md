# Gunluk Tarama — 04.08.2026

Strateji: **erken_dar** | Evren: BIST 100 | Rapor: 2026-08-04 10:59

## 🟢 BUGUN TETIKLENDI (0)

Tum giris kriterleri bugun saglandi.

Bugun tetiklenen hisse yok.

## 🟡 IZLEME LISTESI (21)

Kurulum tamam, tetik henuz gelmedi. **Asil liste bu:** kirilim gununde almak istiyorsan yarin hangi hisseye bakacagini buradan secersin. `Kirilim` sutunu, 20 gunluk zirveye ne kadar kaldigini gosterir — %0'a yakin olan bir sonraki guclu gunde tetiklenir.

| Hisse | Fiyat | Tetik | Eksik kriter | Kirilim seviyesi | Uzaklik | RVOL | Baz gen. |
|---|---|---|---|---|---|---|---|
| **MGROS** | 617.00 | 1/3 | kirilim, rvol2 | 656.50 | 6.4% | 0.37x | 9.9% |
| **MAVI** | 38.96 | 1/3 | kirilim, rvol2 | 41.58 | 6.7% | 0.43x | 11.1% |
| **EREGL** | 41.44 | 1/3 | kirilim, rvol2 | 45.10 | 8.8% | 0.53x | 15.5% |
| **IEYHO** | 168.60 | 0/3 | kirilim, rvol2, tepede_kapanis | 169.00 | 0.2% | 1.44x | 12.6% |
| **ENJSA** | 108.40 | 0/3 | kirilim, rvol2, tepede_kapanis | 111.80 | 3.1% | 1.08x | 12.8% |
| **ANSGR** | 27.20 | 0/3 | kirilim, rvol2, tepede_kapanis | 28.38 | 4.3% | 0.58x | 8.6% |
| **DOAS** | 185.80 | 0/3 | kirilim, rvol2, tepede_kapanis | 193.90 | 4.4% | 0.75x | 7.1% |
| **AEFES** | 21.52 | 0/3 | kirilim, rvol2, tepede_kapanis | 22.48 | 4.5% | 0.57x | 15.8% |
| **AKSA** | 12.37 | 0/3 | kirilim, rvol2, tepede_kapanis | 13.02 | 5.3% | 0.40x | 16.0% |
| **KCHOL** | 195.20 | 0/3 | kirilim, rvol2, tepede_kapanis | 205.70 | 5.4% | 0.51x | 13.0% |
| **TCELL** | 105.90 | 0/3 | kirilim, rvol2, tepede_kapanis | 112.40 | 6.1% | 0.84x | 13.6% |
| **BIMAS** | 382.25 | 0/3 | kirilim, rvol2, tepede_kapanis | 408.25 | 6.8% | 0.32x | 15.2% |
| **MPARK** | 400.00 | 0/3 | kirilim, rvol2, tepede_kapanis | 432.75 | 8.2% | 0.17x | 9.8% |
| **DOHOL** | 20.50 | 0/3 | kirilim, rvol2, tepede_kapanis | 22.18 | 8.2% | 0.19x | 10.6% |
| **SISE** | 41.92 | 0/3 | kirilim, rvol2, tepede_kapanis | 45.38 | 8.3% | 0.57x | 10.6% |
| **CCOLA** | 86.30 | 0/3 | kirilim, rvol2, tepede_kapanis | 93.50 | 8.3% | 0.29x | 17.2% |
| **ALARK** | 101.60 | 0/3 | kirilim, rvol2, tepede_kapanis | 111.00 | 9.3% | 0.44x | 14.3% |
| **GARAN** | 127.40 | 0/3 | kirilim, rvol2, tepede_kapanis | 139.90 | 9.8% | 0.58x | 16.6% |
| **THYAO** | 316.75 | 0/3 | kirilim, rvol2, tepede_kapanis | 355.50 | 12.2% | 0.42x | 16.5% |
| **TURSG** | 6.23 | 0/3 | kirilim, rvol2, tepede_kapanis | 7.00 | 12.4% | 0.37x | 17.6% |
| **BSOKE** | 34.08 | 0/3 | kirilim, rvol2, tepede_kapanis | 38.32 | 12.4% | 0.11x | 16.1% |

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
