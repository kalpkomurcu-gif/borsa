# Olcum Raporu — 2026-08-04 08:27

Evren: BIST 100 (100 hisse) | Periyot: 5y

> Tek basina getiri sayisi yorumlanamaz. Her strateji icin **evren kiyasi** satirina bakin: ayni tarihlerde ortalama hisse ne getirdiyse, stratejinin katkisi aradaki farktir.

### mevcut sistemi

- Islem: **1967** | Isabet: **44.8%** | Ort. tutma: 10.4 gun
- Ortalama getiri: **+4.75%** | Medyan: -1.00%
- Ort. kazanc: +16.92% | Ort. kayip: -5.13%
- **Beklenti: +4.75%** | Profit factor: 2.68
- Ozkaynak (x): 32250019.001 | Max dusus: -47.34%

**Evren kiyasi:** strateji +4.75% vs ayni tarihlerde ortalama hisse +3.67% → **fark +1.08%**  ✅ evreni geciyor

**Giris konumu:** dipten ortalama +23.4% yukarida | 20 gunluk aralikta konum 115/100 (>=100 = kirilim gunu girisi)

**Cikis sebepleri:** KRITER: 1962, ACIK: 5

**Rejime gore:**

| Rejim | Islem | Isabet | Ort. getiri | Beklenti |
|---|---|---|---|---|
| endeks MA50 alti | 362 | 33.7% | +1.02% | +1.02% |
| endeks MA50 ustu | 1605 | 47.3% | +5.59% | +5.59% |

### erken sistemi

- Islem: **283** | Isabet: **55.5%** | Ort. tutma: 14.8 gun
- Ortalama getiri: **+7.77%** | Medyan: +1.75%
- Ort. kazanc: +18.16% | Ort. kayip: -5.18%
- **Beklenti: +7.77%** | Profit factor: 4.37
- Ozkaynak (x): 64.413 | Max dusus: -10.38%

**Evren kiyasi:** strateji +7.77% vs ayni tarihlerde ortalama hisse +5.59% → **fark +2.17%**  ✅ evreni geciyor

**Giris konumu:** dipten ortalama +14.7% yukarida | 20 gunluk aralikta konum 156/100 (>=100 = kirilim gunu girisi)

**Cikis sebepleri:** STOP: 234, KRITER: 48, ACIK: 1

**Rejime gore:**

| Rejim | Islem | Isabet | Ort. getiri | Beklenti |
|---|---|---|---|---|
| endeks MA50 alti | 46 | 50.0% | +4.03% | +4.03% |
| endeks MA50 ustu | 237 | 56.5% | +8.49% | +8.49% |

## Ablasyon — her kriterin katkisi (erken sistem)

Bir kriteri cikarinca **beklenti yukseliyorsa** o kriter zarar veriyordur. Islem sayisi cok artip beklenti korunuyorsa kriter gereksiz yere firsat kaciriyordur.

| Varyant | Islem | Isabet | Ort. getiri | Beklenti | PF |
|---|---|---|---|---|---|
| TAM SISTEM | 283 | 55.5% | +7.77% | +7.77% | 4.37 |
| -sikisma | 366 | 54.9% | +8.33% | +8.33% | 4.53 |
| -dar_baz | 452 | 55.5% | +8.41% | +8.41% | 4.08 |
| -zirveye_yakin | 397 | 52.9% | +6.43% | +6.43% | 3.56 |
| -kirilim | 388 | 49.2% | +6.56% | +6.56% | 3.89 |
| -rvol2 | 678 | 49.6% | +6.13% | +6.13% | 3.41 |
| -tepede_kapanis | 363 | 52.9% | +7.51% | +7.51% | 4.14 |
| -kalma_ma21 | 278 | 56.5% | +8.68% | +8.68% | 4.65 |

## Kriterler

**mevcut:**

- `tetik` **hacim_ort** — Hacim > onceki 20 gun ortalamasi — zayif filtre, gunlerin ~%40'i gecer
- `tetik` **gg_seviye** — Son 21 gun getirisi > endeks — GEC: bir aydir zaten kosuyor
- `surekli` **macd** — MACD histogrami > 0 (MACD > sinyal cizgisi)
- `surekli` **rsi50** — RSI(14) > 50
- `surekli` **adx25** — ADX(14) > 25 — GEC: Wilder cift yumusatma ~2x14 bar gecikme
- `surekli` **ma5_ma21** — MA5 > MA21

  Cikis: ATR stop yok, kriter bozulunca

**erken:**

- `kurulum` **sikisma** — Son 10 gun icinde sikisma vardi (bant genisligi 6 ayin en dusuk %25'i)
- `kurulum` **dar_baz** — Son 20 gunluk baz genisligi < %18 — dar baz kaliteli kirilim verir
- `kurulum` **zirveye_yakin** — Fiyat 52 hafta zirvesinin %80'i uzerinde
- `tetik` **kirilim** — Kapanis > onceki 20 gunun en yuksegi — tanimi geregi hareketin 1. gunu
- `tetik` **rvol2** — Hacim, onceki 20 gun medyaninin 2 katindan fazla
- `tetik` **tepede_kapanis** — Kapanis gunun araliginin ust %30'unda — gun boyu alici baskisi
- `kalma` **kalma_ma21** — Fiyat MA21 uzerinde

  Cikis: ATR x2.0, iz suren, kriter bozulunca


---
Fiyatlar kapanistir. Stop 'bu seviyeyi ilk goren kapanista cik' demektir; gap ile acilan dususte gerceklesen zarar daha kotu olur. Komisyon ve slipaj dahil degildir.
