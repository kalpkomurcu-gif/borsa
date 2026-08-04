# Olcum Raporu — 2026-08-04 08:37

Evren: BIST 100 (100 hisse) | Periyot: 5y

> **Tek basina getiri sayisi yorumlanamaz.** Her strateji icin **evren kiyasi** satirina bakin: ayni tarihlerde ortalama hisse ne getirdiyse, stratejinin katkisi aradaki farktir. TL bazli getiriler enflasyonla siser; mutlak sayilar degil FARK anlamlidir.

> ⚠️ **Hayatta kalma yanliligi.** Evren, BIST 100'un BUGUNKU bilesimidir; gecmise dogru uygulanmasi 'bugun endekste olmayi basarmis' hisseleri test etmek demektir. Cokup endeksten dusenler listede yok, bu da mutlak getirileri yukari sisirir. Evren kiyasi bu yanliligi KISMEN giderir (kiyas da ayni carpik evreni kullanir), bu yuzden **fark satirina mutlak getiriden cok daha fazla guvenilebilir**. Periyot uzadikca yanlilik buyur.

### mevcut sistemi

- Islem: **1967** | Isabet: **44.8%** | Ort. tutma: 10.5 gun
- Ortalama getiri: **+4.76%** | Medyan: -1.00%
- Ort. kazanc: +16.95% | Ort. kayip: -5.13%
- **Beklenti: +4.76%** | Profit factor: 2.68
- Portfoy (5 pozisyon): ozkaynak **10.88x** | yillik +62.92% | max dusus -34.17%
- Sinyalin **%72'i atlandi** (slot doluydu): 551 alindi / 1416 atlandi

**Evren kiyasi:** strateji +4.76% vs ayni tarihlerde ortalama hisse +3.68% → **fark +1.09%**  ✅ evreni geciyor

**Giris konumu:** dipten ortalama +23.4% yukarida | 20 gunluk aralikta konum 115/100 (>=100 = kirilim gunu girisi)

**Cikis sebepleri:** KRITER: 1963, ACIK: 4

**Rejime gore:**

| Rejim | Islem | Isabet | Ort. getiri | Beklenti |
|---|---|---|---|---|
| endeks MA50 alti | 362 | 33.7% | +1.02% | +1.02% |
| endeks MA50 ustu | 1605 | 47.3% | +5.61% | +5.61% |

### erken sistemi

- Islem: **284** | Isabet: **55.3%** | Ort. tutma: 14.7 gun
- Ortalama getiri: **+7.73%** | Medyan: +1.63%
- Ort. kazanc: +18.16% | Ort. kayip: -5.17%
- **Beklenti: +7.73%** | Profit factor: 4.34
- Portfoy (5 pozisyon): ozkaynak **6.99x** | yillik +55.43% | max dusus -11.77%
- Sinyalin **%37'i atlandi** (slot doluydu): 179 alindi / 105 atlandi

**Evren kiyasi:** strateji +7.73% vs ayni tarihlerde ortalama hisse +5.57% → **fark +2.15%**  ✅ evreni geciyor

**Giris konumu:** dipten ortalama +14.7% yukarida | 20 gunluk aralikta konum 155/100 (>=100 = kirilim gunu girisi)

**Cikis sebepleri:** STOP: 234, KRITER: 48, ACIK: 2

**Rejime gore:**

| Rejim | Islem | Isabet | Ort. getiri | Beklenti |
|---|---|---|---|---|
| endeks MA50 alti | 47 | 48.9% | +3.86% | +3.86% |
| endeks MA50 ustu | 237 | 56.5% | +8.49% | +8.49% |

### erken_yalin sistemi

- Islem: **775** | Isabet: **54.8%** | Ort. tutma: 16.1 gun
- Ortalama getiri: **+9.74%** | Medyan: +2.16%
- Ort. kazanc: +23.30% | Ort. kayip: -6.71%
- **Beklenti: +9.74%** | Profit factor: 4.21
- Portfoy (5 pozisyon): ozkaynak **14.57x** | yillik +81.48% | max dusus -34.94%
- Sinyalin **%63'i atlandi** (slot doluydu): 285 alindi / 490 atlandi

**Evren kiyasi:** strateji +9.74% vs ayni tarihlerde ortalama hisse +6.47% → **fark +3.27%**  ✅ evreni geciyor

**Giris konumu:** dipten ortalama +24.7% yukarida | 20 gunluk aralikta konum 142/100 (>=100 = kirilim gunu girisi)

**Cikis sebepleri:** STOP: 771, ACIK: 4

**Rejime gore:**

| Rejim | Islem | Isabet | Ort. getiri | Beklenti |
|---|---|---|---|---|
| endeks MA50 alti | 124 | 41.9% | +4.21% | +4.21% |
| endeks MA50 ustu | 651 | 57.3% | +10.80% | +10.80% |

## Ablasyon — her kriterin katkisi (erken_yalin)

Bir kriteri cikarinca **beklenti yukseliyorsa** o kriter zarar veriyordur. Islem sayisi cok artip beklenti korunuyorsa kriter gereksiz yere firsat kaciriyordur.

| Varyant | Islem | Isabet | Ort. getiri | Beklenti | PF |
|---|---|---|---|---|---|
| TAM SISTEM | 775 | 54.8% | +9.74% | +9.74% | 4.21 |
| -zirveye_yakin | 1124 | 53.1% | +8.55% | +8.55% | 3.67 |
| -kirilim | 1140 | 52.4% | +8.96% | +8.96% | 3.66 |
| -rvol2 | 1508 | 50.9% | +8.37% | +8.37% | 3.57 |
| -tepede_kapanis | 961 | 51.8% | +8.58% | +8.58% | 3.64 |

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

**erken_yalin:**

- `kurulum` **zirveye_yakin** — Fiyat 52 hafta zirvesinin %80'i uzerinde
- `tetik` **kirilim** — Kapanis > onceki 20 gunun en yuksegi — tanimi geregi hareketin 1. gunu
- `tetik` **rvol2** — Hacim, onceki 20 gun medyaninin 2 katindan fazla
- `tetik` **tepede_kapanis** — Kapanis gunun araliginin ust %30'unda — gun boyu alici baskisi

  Cikis: ATR x2.0, iz suren


---
Fiyatlar kapanistir. Stop 'bu seviyeyi ilk goren kapanista cik' demektir; gap ile acilan dususte gerceklesen zarar daha kotu olur. Komisyon ve slipaj dahil degildir.
