"""
Sentetik veriyle uctan uca dogrulama — AG BAGLANTISI GEREKTIRMEZ.

Neden sentetik: Yahoo verisiyle test edilirse ne gostergelerin dogru
hesaplandigi ne de girisin ne zaman tetiklendigi kanitlanabilir; gercek
veride "dogru cevap" bilinmez. Burada kirilim gunu BILEREK uretilir,
boylece "sistem hareketin kacinci gununde giriyor" sorusu olculebilir.

ONEMLI — bu test neyi KANITLAMAZ:
Sentetik seri, erken sistemin aradigi kalibi (sikisma -> hacimli kirilim
-> trend) bilerek icerir. Dolayisiyla buradaki yuksek beklenti sayilari
stratejinin PIYASADA calistiginin delili DEGILDIR; sadece boru hattinin
dogru kuruldugunun ve giris zamanlamasinin iddia edildigi gibi
davrandiginin delilidir. Gercek edge yalnizca rapor.py ile gercek
veride, evren kiyasina bakilarak olculur.

Kullanim: python test_olcum.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

import gostergeler as G
import olcum as O
import strateji as S

RNG = np.random.default_rng(7)
N_GUN = 500
TARIHLER = pd.bdate_range("2024-01-02", periods=N_GUN)

_hata = 0


def kontrol(kosul: bool, mesaj: str) -> None:
    global _hata
    if kosul:
        print(f"  [TAMAM] {mesaj}")
    else:
        _hata += 1
        print(f"  [HATA ] {mesaj}")


def sentetik_hisse(kirilim_gun: int | None, gurultu: float = 0.012) -> pd.DataFrame:
    """
    Uc fazli seri:
      1) sikisma : dusuk volatilite yatay baz (kirilimdan onceki 60 gun)
      2) kirilim : hacim patlamasi + guclu yukari gun
      3) trend   : suren yukselis
    kirilim_gun None ise sadece gurultu (kontrol grubu).
    """
    getiri = RNG.normal(0.0003, gurultu, N_GUN)
    hacim = RNG.lognormal(13.5, 0.35, N_GUN)

    if kirilim_gun is not None:
        b0 = kirilim_gun - 60
        getiri[b0:kirilim_gun] = RNG.normal(0.0, gurultu * 0.28, 60)
        hacim[b0:kirilim_gun] *= 0.65
        hacim[kirilim_gun - 12:kirilim_gun] *= 1.5
        getiri[kirilim_gun] = 0.055
        hacim[kirilim_gun] *= 4.5
        n = min(45, N_GUN - kirilim_gun - 1)
        getiri[kirilim_gun + 1:kirilim_gun + 1 + n] = RNG.normal(0.006, gurultu, n)
        hacim[kirilim_gun + 1:kirilim_gun + 1 + n] *= 1.6

    kapanis = 100 * np.exp(np.cumsum(getiri))
    aralik = np.abs(RNG.normal(0.012, 0.004, N_GUN)) * kapanis
    guclu = getiri > 0.004
    konum = np.where(guclu, RNG.uniform(0.78, 0.97, N_GUN),
                     RNG.uniform(0.2, 0.8, N_GUN))
    low = kapanis - aralik * konum
    high = low + aralik
    acilis = low + aralik * RNG.uniform(0.2, 0.8, N_GUN)
    return pd.DataFrame(
        {"Open": acilis, "High": np.maximum(high, kapanis),
         "Low": np.minimum(low, kapanis), "Close": kapanis, "Volume": hacim},
        index=TARIHLER)


def evren() -> tuple[pd.DataFrame, dict, dict, pd.Series]:
    kirilimlar, cerceveler = {}, {}
    for i in range(20):
        ad = f"KIR{i:02d}"
        kirilimlar[ad] = int(RNG.integers(180, 420))
        cerceveler[ad] = sentetik_hisse(kirilimlar[ad])
    for i in range(20):
        cerceveler[f"GUR{i:02d}"] = sentetik_hisse(None)

    data = pd.concat(cerceveler, axis=1)
    data.columns = pd.MultiIndex.from_tuples(data.columns)
    endeks = pd.DataFrame({s: c["Close"] for s, c in cerceveler.items()}).mean(axis=1)
    return data, cerceveler, kirilimlar, endeks


def test_gostergeler(d: pd.DataFrame) -> None:
    print("\n1) GOSTERGE SINIRLARI VE shift(1) DOGRULUGU")
    kontrol(G.rsi(d["Close"]).dropna().between(0, 100).all(), "RSI 0-100 araliginda")
    kontrol(G.adx(d["High"], d["Low"], d["Close"]).dropna().between(0, 100).all(),
            "ADX 0-100 araliginda")
    kontrol(G.kapanis_konumu(d["High"], d["Low"], d["Close"]).dropna()
            .between(0, 1).all(), "kapanis_konumu 0-1 araliginda")
    kontrol((G.atr(d["High"], d["Low"], d["Close"]).dropna() > 0).all(),
            "ATR pozitif")

    i = 300
    kontrol(abs(G.donchian_ust(d["High"], 20).iloc[i]
                - d["High"].iloc[i - 20:i].max()) < 1e-9,
            "donchian_ust bugunku bari esige KATMIYOR (shift(1))")
    kontrol(abs(G.rvol(d["Volume"], 20).iloc[i]
                - d["Volume"].iloc[i] / d["Volume"].iloc[i - 20:i].median()) < 1e-9,
            "rvol onceki 20 gunun MEDYANINI kullaniyor (shift(1))")

    # yakin_gecmiste: bugunku degeri ICERMEMELI
    s = pd.Series([False] * 20 + [True] + [False] * 20, index=TARIHLER[:41])
    y = G.yakin_gecmiste(s, gun=5)
    kontrol(not bool(y.iloc[20]), "yakin_gecmiste bugunku bari ICERMIYOR")
    kontrol(bool(y.iloc[21]) and bool(y.iloc[25]) and not bool(y.iloc[26]),
            "yakin_gecmiste penceresi dogru (5 gun sonra kapanir)")


def test_giris_zamanlamasi(cerceveler: dict, kirilimlar: dict,
                           endeks: pd.Series) -> None:
    """Asil test: giris, bilinen kirilim gununden kac gun sonra?"""
    print("\n2) GIRIS ZAMANLAMASI — hareketin kacinci gunu?")
    ortalama = {}
    for strat in (S.mevcut_sistem(), S.erken_giris()):
        gecikme, yakalanan = [], 0
        for sembol, kg in kirilimlar.items():
            d = cerceveler[sembol]
            for p in S.pozisyonlar(strat, d, endeks):
                fark = d.index.get_loc(pd.Timestamp(p["giris_tarih"])) - kg
                if 0 <= fark <= 45:
                    gecikme.append(fark)
                    yakalanan += 1
                    break
        ortalama[strat.ad] = float(np.mean(gecikme)) if gecikme else float("nan")
        print(f"     {strat.ad:8s}: {yakalanan}/{len(kirilimlar)} kirilim "
              f"yakalandi | ortalama gecikme {ortalama[strat.ad]:.1f} gun")

    kontrol(ortalama["erken"] < ortalama["mevcut"],
            f"erken sistem daha ONCE giriyor "
            f"({ortalama['mevcut']:.1f} -> {ortalama['erken']:.1f} gun)")
    kontrol(ortalama["erken"] <= 1.0,
            "erken sistem kirilim gununde/ertesinde giriyor")


def test_olcum(data: pd.DataFrame, semboller: list[str],
               endeks: pd.Series) -> None:
    print("\n3) OLCUM FONKSIYONLARI")
    erken = S.erken_giris()
    isl = O.calistir(erken, data, semboller, endeks)
    kontrol(not isl.empty, f"calistir() islem uretti ({len(isl)})")

    m = O.metrikler(isl)
    kontrol(0 <= m["isabet"] <= 1, "isabet 0-1 araliginda")
    kontrol(abs(m["beklenti"] - (m["isabet"] * m["ort_kazanc"]
                                 + (1 - m["isabet"]) * m["ort_kayip"])) < 1e-9,
            "beklenti = isabet*ort_kazanc + (1-isabet)*ort_kayip")
    kontrol("ozkaynak" not in m and "max_dusus" not in m,
            "metrikler() portfoy sayisi DONDURMUYOR (ayri fonksiyon)")

    p = O.portfoy(isl, max_pozisyon=5)
    kontrol(p["alinan"] + p["atlanan"] == p["islem"],
            "portfoy: alinan + atlanan = toplam sinyal")
    kontrol(p["max_dusus"] <= 0, "portfoy: max_dusus negatif (veya sifir)")
    kontrol(p["ozkaynak"] > 0, "portfoy: ozkaynak pozitif")

    # Slot limiti gercekten baglayici mi? Az slot -> daha cok atlanan.
    dar = O.portfoy(isl, max_pozisyon=1)
    genis = O.portfoy(isl, max_pozisyon=50)
    kontrol(dar["atlanan"] >= genis["atlanan"],
            f"az slot daha cok sinyal atliyor ({dar['atlanan']} >= "
            f"{genis['atlanan']})")
    kontrol(dar["alinan"] <= genis["alinan"], "az slot daha az islem aliyor")

    # Asil regresyon: ust uste binen islemler SIRALI bilesiklenmemeli.
    # Eski hatali metrik burada milyonlarca kat ozkaynak uretiyordu.
    kontrol(p["ozkaynak"] < 1e6,
            f"ozkaynak makul buyuklukte ({p['ozkaynak']:.2f}x) — "
            "ust uste binen islemler sirali bilesiklenmiyor")

    kiyas = O.evren_kiyasi(isl, data, semboller)
    kontrol("evren_getiri" in kiyas and kiyas["evren_getiri"].notna().any(),
            "evren_kiyasi ayni tarihler icin evren getirisi hesapladi")
    kontrol(abs((kiyas["getiri"] - kiyas["evren_getiri"] - kiyas["fark"]).sum()) < 1e-9,
            "fark = strateji getirisi - evren getirisi")

    gec = O.gecikme_olc(isl, data)
    kontrol(gec["aralik_konum"].max() <= 200, "aralik_konum 200'de kirpiliyor")
    kontrol(gec["aralik_konum"].mean() >= 100,
            "erken sistem araligin USTUNDEN giriyor (kirilim)")

    kontrol(p["getiri_dusus"] > 0 or p["getiri_dusus"] != p["getiri_dusus"],
            "getiri/dusus orani hesaplandi")

    ab = O.ablasyon(erken, data, semboller, endeks)
    kontrol("TAM SISTEM" in ab.index and len(ab) == len(erken.kriterler) + 1,
            f"ablasyon her kriter icin satir uretti ({len(ab)} satir)")

    orta = str(pd.Timestamp(data.index[len(data.index) // 2]).date())
    db = O.donem_bol(erken, data, semboller, endeks, orta)
    kontrol(len(db) == 2, f"donem_bol iki donem uretti ({len(db)})")
    kontrol(int(db["islem"].sum()) == len(isl),
            "donem parcalarinin islem toplami = toplam islem "
            f"({int(db['islem'].sum())} = {len(isl)})")

    rej = O.rejim_ayir(isl, endeks)
    kontrol(not rej.empty, "rejim_ayir sonuc uretti")


def test_sinir_durumlari(cerceveler: dict, endeks: pd.Series) -> None:
    print("\n4) SINIR DURUMLARI")
    bos = pd.DataFrame(columns=["hisse", "giris_tarih", "cikis_tarih",
                                "giris_fiyat", "satis_fiyat", "getiri",
                                "gun", "sebep", "acik"])
    kontrol(O.metrikler(bos) == {"islem": 0}, "bos tablo cokmuyor (metrikler)")
    kontrol(O.portfoy(bos) == {"islem": 0}, "bos tablo cokmuyor (portfoy)")
    kontrol(S.pozisyonlar(S.erken_giris(), cerceveler["KIR00"].head(30),
                          endeks) == [],
            "MIN_VERI altinda islem uretilmiyor")

    try:
        S.pozisyonlar(S.Strateji("x", [S.K_GG_KIRILIM]), cerceveler["KIR00"], None)
        kontrol(False, "endeks eksikken hata verilmeli")
    except ValueError:
        kontrol(True, "endeks eksikse ValueError (sessizce atlanmiyor)")

    try:
        S.Kriter("x", "yanlis", lambda d, e: None)
        kontrol(False, "gecersiz tip reddedilmeli")
    except ValueError:
        kontrol(True, "gecersiz kriter tipi reddediliyor")

    # NaN'li seri sinyal uretmemeli
    bozuk = cerceveler["KIR00"].copy()
    bozuk.loc[bozuk.index[:200], "Volume"] = np.nan
    S.pozisyonlar(S.erken_giris(), bozuk, endeks)
    kontrol(True, "NaN'li hacim serisinde cokme yok")


def main() -> int:
    data, cerceveler, kirilimlar, endeks = evren()
    semboller = list(cerceveler)

    print("=" * 64)
    print("SENTETIK DOGRULAMA  (ag baglantisi gerekmez)")
    print("=" * 64)
    test_gostergeler(cerceveler["KIR00"])
    test_giris_zamanlamasi(cerceveler, kirilimlar, endeks)
    test_olcum(data, semboller, endeks)
    test_sinir_durumlari(cerceveler, endeks)

    print("\n" + "=" * 64)
    if _hata:
        print(f"{_hata} KONTROL BASARISIZ")
    else:
        print("TUM KONTROLLER BASARILI")
    print("=" * 64)
    return 1 if _hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
