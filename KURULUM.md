# BIST 100 Günlük Tarama — Kurulum (5-10 dakika)

## Sistem nasıl çalışıyor?

1. **GitHub Actions** her hafta içi 18:40'ta (BIST kapanışından sonra) `tarama.py`'yi çalıştırır
2. Script Yahoo Finance'ten veri çekip kriterleri sağlayan hisseleri `sonuclar/latest.md` ve `latest.json` dosyalarına yazar
3. **Claude routine'in** bu dosyayı GitHub'dan okuyup sana yorumlu özet sunar

Kriterler: MACD > Sinyal çizgisi (al kesişimi bölgesi) · RSI(14) > 50 · Fiyat > MA5, MA9 ve MA21

## Adımlar

1. GitHub'da yeni bir **public** repo aç (örn. `bist-tarama`)
   - Not: Public olmalı ki routine `raw.githubusercontent.com` üzerinden okuyabilsin.
     Tarama sonucu hassas veri içermiyor, sadece herkese açık piyasa verisi.
2. Bu klasördeki tüm dosyaları repoya yükle (web arayüzünden "Add file > Upload files"
   ile sürükle-bırak yeterli; `.github/workflows/tarama.yml` klasör yapısıyla yüklenmeli)
3. Repo > **Settings > Actions > General > Workflow permissions** kısmında
   **"Read and write permissions"** seçili olduğundan emin ol (commit atabilmesi için)
4. **Actions** sekmesine gir, "BIST 100 Gunluk Tarama" workflow'unu seç,
   **"Run workflow"** ile bir kez manuel çalıştırıp test et
5. 1-2 dakika sonra `sonuclar/latest.md` dosyası oluşmuş olmalı — link şu formatta:
   `https://raw.githubusercontent.com/KULLANICI_ADIN/bist-tarama/main/sonuclar/latest.md`

## Claude routine'i kur

Claude'a şu routine'i tanımla (saat 18:50, hafta içi):

> Şu dosyayı bash ile oku:
> `curl -s https://raw.githubusercontent.com/KULLANICI_ADIN/bist-tarama/main/sonuclar/latest.md`
> Bu benim BIST 100 teknik taramamın günlük sonucu (MACD al kesişimi + RSI>50 +
> fiyat MA5/9/21 üstünde). Sonuçları bana tablo halinde sun, RSI'si en güçlü 3-5
> hisseyi öne çıkar, portföyümdeki hisselerden (THYAO, TUPRS, ASELS, DSTKF) listede
> olan varsa özellikle belirt. Tarih bugünden eskiyse verinin güncellenmediğini söyle.

## Notlar

- `tarama.py` içindeki `BIST100` listesi endeks değiştikçe güncellenmeli
  (BIST endeks revizyonları: Ocak/Nisan/Temmuz/Ekim)
- `MACD_MODE` değişkeni: `"histogram"` (al kesişimi, varsayılan) veya `"line"` (MACD çizgisi > 0)
- GitHub Actions ücretsiz kotası (public repo'da sınırsız) bu iş için fazlasıyla yeterli
- Yahoo Finance bazen tek tek hisselerde veri vermeyebilir; bunlar raporda
  "veri alınamayan" olarak listelenir
