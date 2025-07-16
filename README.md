# CreaCritic - Ozan Tasarım Eleştiri Sistemi

![CreaCritic Logo](https://img.shields.io/badge/CreaCritic-v1.1.1-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)
![Flask](https://img.shields.io/badge/Flask-3.1.1-red)
![Gemini AI](https://img.shields.io/badge/Gemini%20AI-1.5%20Flash-orange)

## Proje Özeti (Türkçe)
CreaCritic, Ozan karakter profiline dayalı, Google Gemini API ve özel Ozan stil motoru ile çalışan bir tasarım eleştiri sistemidir. Flask tabanlı web arayüzü, dosya yükleme, analiz, responsive UI, JSON/HTML çıktı, kullanıcı brief ve savunma promptları ile stabil ve kullanıcı dostu bir yapı sunar.

### Ana Özellikler
- Google Gemini API ile Ozan stili analiz
- Dosya yükleme ve analiz (görsel)
- Kullanıcıdan brief ve tasarım savunması alma
- Responsive, iki sütunlu analiz sayfası
- Seri no ve versiyon bilgisi arayüzde görünür

### Son Gelişmeler
- Hatalar giderildi, Gemini API key yönetimi geliştirildi
- history.html eklendi
- GitHub’a yüklendi
- IIS için deploy scriptleri hazırlandı

Daha fazla detay için: BRIEF_VE_YAPILANLAR.txt

## 📋 Proje Hakkında

CreaCritic, yapay zeka destekli tasarım analizi ve eleştiri sistemidir. Google Gemini AI kullanarak tasarım dosyalarını analiz eder ve Ozan Bayar'ın üslubunda eleştiri yapar.

**Seri No:** CR-023-v1.1  
**Versiyon:** 1.1.1  
**Son Güncelleme:** 16/07/2025

## ✨ Özellikler

- 🎨 **Görsel Analiz:** PDF, PNG, JPG, GIF, BMP formatlarını destekler
- 🤖 **AI Destekli:** Google Gemini 1.5 Flash modeli kullanır
- 📊 **Matematiksel Model:** Ozan üslubunda eleştiri algoritması
- 🌐 **Web Arayüzü:** Modern Flask tabanlı arayüz
- 💾 **API Key Kaydetme:** Otomatik localStorage kaydetme
- 📈 **Onay Sistemi:** Tasarım onay/revizyon/ret kararları
- 📱 **Responsive:** Mobil uyumlu tasarım

## 🚀 Kurulum

### Gereksinimler
- Python 3.12+
- Google Gemini API Key

### Adımlar

1. **Repo'yu klonlayın:**
```bash
git clone https://github.com/[kullanici-adi]/CreaCritic.git
cd CreaCritic
```

2. **Virtual environment oluşturun:**
```bash
python -m venv venv_creacritic
venv_creacritic\Scripts\activate  # Windows
source venv_creacritic/bin/activate  # Linux/Mac
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Uygulamayı başlatın:**
```bash
cd web_interface
python app.py
```

5. **Tarayıcıda açın:**
```
http://localhost:5000
```

## 🔧 Kullanım

1. **API Key Alın:** [Google AI Studio](https://aistudio.google.com/u/0/apikey) adresinden API key alın
2. **Dosya Yükleyin:** Tasarım dosyanızı sürükleyip bırakın
3. **Brief Girin:** (Opsiyonel) Müşteri briefini ekleyin
4. **Analiz Edin:** "Analiz Et" butonuna tıklayın
5. **Sonuçları İnceleyin:** Detaylı analiz raporunu görün

## 📁 Proje Yapısı

```
CreaCritic/
├── config/                 # Konfigürasyon dosyaları
├── src/                   # Ana kaynak kodları
│   ├── gemini_processor.py
│   ├── mathematical_model.py
│   ├── ozan_style_engine.py
│   └── design_type_analyzer.py
├── web_interface/         # Flask web arayüzü
│   ├── app.py
│   ├── static/
│   └── templates/
├── tests/                 # Test dosyaları
├── docs/                  # Dokümantasyon
└── logs/                  # Log dosyaları
```

## 🧠 Teknik Detaylar

### AI Modeli
- **Model:** Google Gemini 1.5 Flash
- **Görsel Analiz:** Çoklu format desteği
- **Prompt Engineering:** Ozan üslubuna özel promptlar

### Matematiksel Model
- **Utility Function:** Tasarım kalitesi hesaplama
- **Dynamic Weights:** Brief ve tasarım savunmasına göre ağırlık
- **Approval System:** ONAY/REVİZYON/RET kararları

### Web Arayüzü
- **Framework:** Flask 3.1.1
- **Frontend:** HTML5, CSS3, JavaScript
- **Responsive:** Bootstrap benzeri grid sistemi

## 📊 API Endpoints

- `GET /` - Ana sayfa
- `POST /analyze` - Tasarım analizi (HTML)
- `POST /analyze-json` - Tasarım analizi (JSON)
- `GET /api/health` - Sistem sağlık kontrolü
- `GET /api/analysis_stats` - Analiz istatistikleri

## 🔒 Güvenlik

- API key'ler localStorage'da şifrelenmeden saklanır
- Dosya yükleme güvenliği (secure_filename)
- Maksimum dosya boyutu: 10MB
- Desteklenen formatlar: PDF, PNG, JPG, GIF, BMP

## 🐛 Bilinen Sorunlar

- Görsel gösterme özelliği kaldırıldı (404 hatası)
- History sayfası template'i eksik
- Settings sayfası henüz implement edilmedi

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

- **Proje:** [CreaCritic GitHub](https://github.com/[kullanici-adi]/CreaCritic)
- **Geliştirici:** Ozan Bayar
- **Versiyon:** 1.1.1

## 🙏 Teşekkürler

- Google Gemini AI ekibi
- Flask framework geliştiricileri
- Tüm katkıda bulunanlar

---

**CreaCritic v1.1.1** - Seri No: CR-023-v1.1 