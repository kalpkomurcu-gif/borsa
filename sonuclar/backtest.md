# Filtre Karsilastirmali Backtest

Veri: 1y | Taranan: 100 hisse | Veri alinamayan: 0
Filtre: sadece 3 gunden UZUN suren pozisyonlar

A = giris fiyatindan cikisa (ileriye donuk bilgi icerir, uygulanabilir DEGIL)
B = 4. gun kapanisindan cikisa (uygulanabilir)

| Senaryo | Kapali poz. | Ort. gun | A toplam | A ort | A kazanan | B toplam | B ort | B kazanan |
|---|---|---|---|---|---|---|---|---|
| ESKI (MACD/RSI/MA) | 678 | 7.1 | +4176.0% | +6.16% | 515/678 | +1023.9% | +1.51% | 279/678 |
| + ADX>25 | 320 | 7.4 | +2572.7% | +8.04% | 248/320 | +795.8% | +2.49% | 139/320 |
| + Hacim>20g ort | 582 | 7.1 | +3496.8% | +6.01% | 436/582 | +795.5% | +1.37% | 229/582 |
| YENI (ADX + Hacim) | 266 | 7.3 | +2076.6% | +7.81% | 200/266 | +635.0% | +2.39% | 113/266 |

## Acik pozisyonlar (rapor gunu itibariyle)

| Senaryo | Acik poz. | A toplam | B toplam |
|---|---|---|---|
| ESKI (MACD/RSI/MA) | 8 | +71.3% | +31.2% |
| + ADX>25 | 3 | +23.8% | +15.8% |
| + Hacim>20g ort | 7 | +39.3% | +14.6% |
| YENI (ADX + Hacim) | 1 | -1.5% | +0.0% |

## YENI kriterler — En iyi 10

| Hisse | Giris | Giris F. | Cikis | Cikis F. | A % | B % | Gun |
|---|---|---|---|---|---|---|---|
| DSTKF | 30.01.2026 | 800.00 | 13.03.2026 | 1749.00 | +118.6% | +105.8% | 30 |
| IEYHO | 18.09.2025 | 21.22 | 15.10.2025 | 36.62 | +72.6% | +41.4% | 19 |
| KLRHO | 05.12.2025 | 178.00 | 31.12.2025 | 306.25 | +72.1% | +44.4% | 18 |
| SARKY | 26.12.2025 | 17.24 | 19.01.2026 | 29.57 | +71.5% | +66.5% | 15 |
| ODINE | 13.02.2026 | 396.00 | 09.03.2026 | 636.00 | +60.6% | +33.9% | 16 |
| KLRHO | 12.09.2025 | 70.10 | 26.09.2025 | 111.00 | +58.3% | +19.0% | 10 |
| IEYHO | 05.11.2025 | 39.52 | 02.12.2025 | 58.40 | +47.8% | +21.5% | 19 |
| DSTKF | 08.06.2026 | 2470.00 | 06.07.2026 | 3585.00 | +45.1% | +37.9% | 20 |
| KTLEV | 31.12.2025 | 21.38 | 15.01.2026 | 30.41 | +42.3% | +29.9% | 10 |
| SKBNK | 02.02.2026 | 8.74 | 27.02.2026 | 12.14 | +39.0% | +32.0% | 19 |

## YENI kriterler — En kotu 10

| Hisse | Giris | Giris F. | Cikis | Cikis F. | A % | B % | Gun |
|---|---|---|---|---|---|---|---|
| DSTKF | 07.07.2026 | 3920.00 | 13.07.2026 | 3457.50 | -11.8% | -10.0% | 4 |
| EUPWR | 21.07.2026 | 105.60 | 27.07.2026 | 98.20 | -7.0% | -2.2% | 4 |
| CWENE | 20.11.2025 | 26.46 | 26.11.2025 | 24.70 | -6.7% | -4.4% | 4 |
| GESAN | 26.05.2026 | 75.50 | 01.06.2026 | 71.00 | -6.0% | -6.0% | 4 |
| GESAN | 11.05.2026 | 61.35 | 15.05.2026 | 58.05 | -5.4% | -10.0% | 4 |
| EUPWR | 08.04.2026 | 42.72 | 15.04.2026 | 40.54 | -5.1% | -9.6% | 5 |
| CWENE | 03.07.2026 | 41.00 | 09.07.2026 | 39.06 | -4.7% | -5.3% | 4 |
| HEKTS | 12.02.2026 | 3.46 | 19.02.2026 | 3.31 | -4.3% | -4.6% | 5 |
| KTLEV | 18.06.2026 | 185.80 | 24.06.2026 | 178.20 | -4.1% | -2.0% | 4 |
| MAGEN | 17.10.2025 | 24.88 | 23.10.2025 | 23.92 | -3.9% | -4.4% | 4 |

Not: Yuzdeler her isleme esit tutar konuldugu ve bilesiklenme olmadigi varsayimiyla toplanmistir; portfoy getirisi degildir. Komisyon/slipaj dahil degildir.
