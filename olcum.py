"""
Olcum altyapisi — bir stratejinin GERCEKTEN edge'i var mi?

Eski raporun "Getiri toplami: -137.8%" satiri olcum degildi:
  1) Ust uste binen 75 isleme %100 sermaye konamaz; yuzdeleri toplamak
     hicbir portfoyun yasamadigi bir sayi uretir.
  2) Kiyas yok. -%1.84 ortalama kotu mu? O donemde ortalama hisse
     -%5 yaptiysa strateji IYI demektir. Kiyassiz sayi yorumlanamaz.
  3) Rejim ayrimi yok. Dusen piyasada uzun pozisyon stratejisinin
     kaybetmesi stratejinin degil rejimin sonucudur.

Bu modul dordunu de olcer:
  - metrikler()      : isabet, beklenti, profit factor, dusus
  - evren_kiyasi()   : AYNI tarihlerde ORTALAMA hisse ne yapti (asil kontrol)
  - rejim_ayir()     : endeks MA50 ustunde/altinda girisler
  - ablasyon()       : her kriteri tek tek cikarip katkisini olc
  - gecikme_olc()    : giris, hareketin neresinde? (erken mi gec mi)
"""

from __future__ import annotations

import pandas as pd

import gostergeler as G
import strateji as S
import veri as V


# ---------------------------------------------------------------
# Calistirma
# ---------------------------------------------------------------
def calistir(strat: S.Strateji, data: pd.DataFrame, semboller: list[str],
             endeks: pd.Series | None = None,
             baslangic: str | None = None) -> pd.DataFrame:
    """Stratejiyi tum evrende kosturur; islem tablosu doner."""
    if strat.endeks_ister() and endeks is None:
        raise ValueError(f"{strat.ad}: endeks isteyen kriter var, endeks verilmedi")

    satirlar, atlanan = [], []
    for sembol in semboller:
        d = V.hisse_cerceve(data, sembol)
        if d is None:
            atlanan.append(sembol)
            continue
        try:
            for p in S.pozisyonlar(strat, d, endeks):
                acik = p["sebep"] == "ACIK"
                satis = p["guncel_fiyat"] if acik else p["cikis_fiyat"]
                satirlar.append({
                    "hisse": sembol,
                    "giris_tarih": pd.Timestamp(p["giris_tarih"]),
                    "cikis_tarih": (pd.NaT if acik
                                    else pd.Timestamp(p["cikis_tarih"])),
                    "giris_fiyat": p["giris_fiyat"],
                    "satis_fiyat": satis,
                    "getiri": satis / p["giris_fiyat"] - 1,
                    "gun": p["gun"],
                    "sebep": p["sebep"],
                    "acik": acik,
                })
        except Exception as exc:
            atlanan.append(f"{sembol}({type(exc).__name__})")

    df = pd.DataFrame(satirlar)
    if not df.empty and baslangic:
        df = df[df["giris_tarih"] >= pd.Timestamp(baslangic)]
    if atlanan:
        print(f"[olcum] atlanan {len(atlanan)}: {', '.join(map(str, atlanan[:10]))}"
              + (" ..." if len(atlanan) > 10 else ""))
    return df.reset_index(drop=True)


# ---------------------------------------------------------------
# Metrikler
# ---------------------------------------------------------------
def metrikler(islemler: pd.DataFrame, agirlik: float = 0.2) -> dict:
    """
    agirlik: her isleme ayrilan sermaye orani (0.2 = ayni anda ~5 pozisyon).
    Ozkaynak egrisi cikis tarihine gore sirali bilesikleme ile kurulur —
    yuzde toplamaktan farkli olarak gercekten yasanabilir bir sayi.
    """
    if islemler.empty:
        return {"islem": 0}

    g = islemler["getiri"]
    kazanan, kaybeden = g[g > 0], g[g <= 0]
    isabet = len(kazanan) / len(g)
    ort_kazanc = kazanan.mean() if len(kazanan) else 0.0
    ort_kayip = kaybeden.mean() if len(kaybeden) else 0.0

    brut_kar = kazanan.sum()
    brut_zarar = -kaybeden.sum()

    sirali = islemler.sort_values("cikis_tarih", na_position="last")
    ozkaynak = (1 + agirlik * sirali["getiri"]).cumprod()
    zirve = ozkaynak.cummax()
    max_dusus = float((ozkaynak / zirve - 1).min()) if len(ozkaynak) else 0.0

    return {
        "islem": int(len(g)),
        "isabet": isabet,
        "ort_getiri": float(g.mean()),
        "medyan_getiri": float(g.median()),
        "ort_kazanc": float(ort_kazanc),
        "ort_kayip": float(ort_kayip),
        # Beklenti = islem basina beklenen getiri; sistemin tek sayilik ozeti
        "beklenti": float(isabet * ort_kazanc + (1 - isabet) * ort_kayip),
        "profit_factor": float(brut_kar / brut_zarar) if brut_zarar > 0 else float("inf"),
        "ort_gun": float(islemler["gun"].mean()),
        "ozkaynak": float(ozkaynak.iloc[-1]) if len(ozkaynak) else 1.0,
        "max_dusus": max_dusus,
    }


# ---------------------------------------------------------------
# Asil kontrol: ayni tarihlerde ORTALAMA hisse ne yapti?
# ---------------------------------------------------------------
def _kapanis_matrisi(data: pd.DataFrame, semboller: list[str]) -> pd.DataFrame:
    sutunlar = {}
    for s in semboller:
        d = V.hisse_cerceve(data, s)
        if d is not None:
            sutunlar[s] = d["Close"]
    return pd.DataFrame(sutunlar).sort_index()


def evren_kiyasi(islemler: pd.DataFrame, data: pd.DataFrame,
                 semboller: list[str]) -> pd.DataFrame:
    """
    Her islem icin: AYNI giris/cikis tarihleri arasinda evrendeki
    ortalama hisse ne getirdi? Fark = stratejinin katkisi.

    Bu, endeksle kiyastan daha durust bir kontrol: hem donem hem de
    tutma suresi birebir eslesir, yani "o gunlerde zaten her sey
    yukseliyordu" aciklamasini eler.
    """
    if islemler.empty:
        return islemler

    matris = _kapanis_matrisi(data, semboller)
    tarihler = matris.index
    ek = []
    for _, r in islemler.iterrows():
        gt = tarihler.asof(r["giris_tarih"])
        ct = (tarihler[-1] if pd.isna(r["cikis_tarih"])
              else tarihler.asof(r["cikis_tarih"]))
        if pd.isna(gt) or pd.isna(ct) or ct <= gt:
            ek.append(float("nan"))
            continue
        oran = matris.loc[ct] / matris.loc[gt] - 1
        ek.append(float(oran.mean(skipna=True)))

    out = islemler.copy()
    out["evren_getiri"] = ek
    out["fark"] = out["getiri"] - out["evren_getiri"]
    return out


# ---------------------------------------------------------------
# Rejim
# ---------------------------------------------------------------
def rejim_serisi(endeks: pd.Series, periyot: int = 50) -> pd.Series:
    """True = endeks MA50 uzerinde (uzun pozisyona elverisli rejim)."""
    return endeks > endeks.rolling(periyot).mean()


def rejim_ayir(islemler: pd.DataFrame, endeks: pd.Series,
               periyot: int = 50) -> pd.DataFrame:
    """Girisleri rejime gore gruplar; iki grubun metriklerini karsilastirir."""
    if islemler.empty:
        return pd.DataFrame()
    rejim = rejim_serisi(endeks, periyot)
    etiket = []
    for t in islemler["giris_tarih"]:
        idx = rejim.index.asof(t)
        v = rejim.get(idx) if pd.notna(idx) else None
        etiket.append("bilinmiyor" if v is None or pd.isna(v)
                      else ("endeks MA50 ustu" if bool(v) else "endeks MA50 alti"))
    x = islemler.copy()
    x["rejim"] = etiket
    return pd.DataFrame({
        ad: metrikler(grup) for ad, grup in x.groupby("rejim")
    }).T


# ---------------------------------------------------------------
# Ablasyon: her kriterin katkisi
# ---------------------------------------------------------------
def ablasyon(strat: S.Strateji, data: pd.DataFrame, semboller: list[str],
             endeks: pd.Series | None = None,
             baslangic: str | None = None) -> pd.DataFrame:
    """
    Kriterleri tek tek cikarip yeniden olcer.

    Okuma: bir kriteri cikarinca beklenti YUKSELIYORSA o kriter zarar
    veriyordur. Islem sayisi cok artip beklenti ayni kaliyorsa kriter
    sadece firsat kaciriyordur.
    """
    satirlar = {"TAM SISTEM": metrikler(
        calistir(strat, data, semboller, endeks, baslangic))}
    for k in strat.kriterler:
        alt = strat.haric(k.ad)
        try:
            satirlar[f"-{k.ad}"] = metrikler(
                calistir(alt, data, semboller, endeks, baslangic))
        except Exception as exc:
            satirlar[f"-{k.ad}"] = {"islem": 0, "hata": type(exc).__name__}
    return pd.DataFrame(satirlar).T


# ---------------------------------------------------------------
# Giris gecikmesi: hareketin neresinden aliyoruz?
# ---------------------------------------------------------------
def gecikme_olc(islemler: pd.DataFrame, data: pd.DataFrame,
                pencere: int = 20) -> pd.DataFrame:
    """
    Her giris icin hareketin ne kadarini kacirdigimizi olcer:

      dipten_yukselis : giris fiyati, onceki 'pencere' gunun dibinin % kaci ustunde
      aralik_konum    : giris, onceki pencerenin dip-tepe araliginda nerede
                        (0 = dipte alim, 100 = tepede, >100 = araligin
                        USTUNDE = kirilim). Cok dar bazda payda sifira
                        yaklasip sayiyi patlattigi icin 200'de kirpilir.
      onceki_getiri   : girise kadarki 'pencere' gunluk getiri

    "Ilk gununden yakalamak" hedefi sayisal olarak: dipten_yukselis
    dusuk, aralik_konum >=100 (kirilim) — yani DAR bir bazin tepesinden.
    Genis bazda aralik_konum yuksekken dipten_yukselis de yuksekse
    hareket coktan olmus demektir.
    """
    if islemler.empty:
        return islemler

    onbellek: dict[str, pd.DataFrame] = {}
    kayit = []
    for _, r in islemler.iterrows():
        sembol = r["hisse"]
        if sembol not in onbellek:
            d = V.hisse_cerceve(data, sembol)
            onbellek[sembol] = d if d is not None else pd.DataFrame()
        d = onbellek[sembol]
        if d.empty or r["giris_tarih"] not in d.index:
            kayit.append((float("nan"),) * 3)
            continue
        i = d.index.get_loc(r["giris_tarih"])
        if i < pencere:
            kayit.append((float("nan"),) * 3)
            continue
        onceki = d["Close"].iloc[i - pencere:i]
        dip, tepe = float(onceki.min()), float(onceki.max())
        gf = r["giris_fiyat"]
        konum = (gf - dip) / (tepe - dip) * 100 if tepe > dip else 100.0
        kayit.append((
            (gf / dip - 1) * 100,
            min(konum, 200.0),
            (gf / float(d["Close"].iloc[i - pencere]) - 1) * 100,
        ))

    out = islemler.copy()
    out[["dipten_yukselis", "aralik_konum", "onceki_getiri"]] = pd.DataFrame(
        kayit, index=out.index)
    return out


# ---------------------------------------------------------------
# Rapor
# ---------------------------------------------------------------
def _yuzde(x) -> str:
    return "—" if pd.isna(x) else f"{x * 100:+.2f}%"


def ozet_yaz(ad: str, m: dict) -> list[str]:
    if not m.get("islem"):
        return [f"### {ad}", "", "Islem yok.", ""]
    return [
        f"### {ad}", "",
        f"- Islem: **{m['islem']}** | Isabet: **{m['isabet']*100:.1f}%** "
        f"| Ort. tutma: {m['ort_gun']:.1f} gun",
        f"- Ortalama getiri: **{_yuzde(m['ort_getiri'])}** "
        f"| Medyan: {_yuzde(m['medyan_getiri'])}",
        f"- Ort. kazanc: {_yuzde(m['ort_kazanc'])} "
        f"| Ort. kayip: {_yuzde(m['ort_kayip'])}",
        f"- **Beklenti: {_yuzde(m['beklenti'])}** "
        f"| Profit factor: {m['profit_factor']:.2f}",
        f"- Ozkaynak (x): {m['ozkaynak']:.3f} "
        f"| Max dusus: {_yuzde(m['max_dusus'])}",
        "",
    ]


def karsilastir(stratejiler: list[S.Strateji], data: pd.DataFrame,
                semboller: list[str], endeks: pd.Series | None = None,
                baslangic: str | None = None) -> pd.DataFrame:
    """Birden fazla stratejiyi ayni veride yan yana olcer."""
    return pd.DataFrame({
        s.ad: metrikler(calistir(s, data, semboller, endeks, baslangic))
        for s in stratejiler
    }).T
