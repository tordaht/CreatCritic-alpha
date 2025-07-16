"""
CreaCritic - Ozan Tasarım Eleştiri Sistemi
Ana Uygulama Dosyası
Seri No: CR-010-v1.0
"""

import sys
import os
from datetime import datetime
from config.settings import PROJECT_NAME, VERSION, SERIAL_NO
from config.credentials import validate_credentials
from src.error_handler import ErrorHandler
from src.dropbox_watcher import DropboxWatcher


def main():
    """
    Ana uygulama fonksiyonu
    """
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    CreaCritic v{VERSION}                        ║
║              Ozan Tasarım Eleştiri Sistemi                  ║
║                    Seri No: {SERIAL_NO}                    ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Hata yöneticisini başlat
    error_handler = ErrorHandler()
    
    try:
        # Sistem sağlığını kontrol et
        print("🔍 Sistem sağlığı kontrol ediliyor...")
        if not error_handler.validate_system_health():
            print("❌ Sistem sağlık kontrolü başarısız!")
            return 1
        
        # API anahtarlarını doğrula
        print("🔑 API anahtarları kontrol ediliyor...")
        try:
            validate_credentials()
            print("✅ API anahtarları geçerli")
        except ValueError as e:
            print(f"❌ API anahtarı hatası: {str(e)}")
            return 1
        
        # Dropbox bağlantısını test et
        print("📁 Dropbox bağlantısı test ediliyor...")
        dropbox_watcher = DropboxWatcher()
        if not dropbox_watcher.validate_connection():
            print("❌ Dropbox bağlantısı başarısız!")
            return 1
        

        
        print("✅ Tüm bağlantılar başarılı!")
        print(f"🚀 {PROJECT_NAME} başlatılıyor...")
        print(f"📅 Başlangıç zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Dropbox izlemeyi başlat
        dropbox_watcher.start_watching()
        
    except KeyboardInterrupt:
        print("\n⏹️  Uygulama kullanıcı tarafından durduruldu.")
        return 0
        
    except Exception as e:
        error_handler.log_error(e, "Main application error")
        print(f"❌ Kritik hata: {str(e)}")
        return 1

def show_help():
    """Yardım mesajını gösterir"""
    print(f"""
CreaCritic - Ozan Tasarım Eleştiri Sistemi v{VERSION}

KULLANIM:
    python main.py              # Uygulamayı başlat
    python main.py --help       # Bu yardım mesajını göster
    python main.py --test       # Test modunda çalıştır

GEREKSİNİMLER:
    - .env dosyasında API anahtarları tanımlı olmalı
    - Dropbox ve Slack bağlantıları aktif olmalı
    - Gerekli Python kütüphaneleri yüklü olmalı

SERİ NO: {SERIAL_NO}
""")

def run_tests():
    """Test modunu çalıştırır"""
    print("🧪 Test modu başlatılıyor...")
    
    # Test dosyası oluştur
    test_file = "test_design.png"
    test_content = "Test tasarım dosyası"
    
    try:
        with open(test_file, "w") as f:
            f.write(test_content)
        
        print(f"✅ Test dosyası oluşturuldu: {test_file}")
        print("Test modu tamamlandı.")
        
        # Test dosyasını sil
        os.remove(test_file)
        
    except Exception as e:
        print(f"❌ Test hatası: {str(e)}")

if __name__ == "__main__":
    # Komut satırı argümanlarını kontrol et
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--help" or arg == "-h":
            show_help()
        elif arg == "--test" or arg == "-t":
            run_tests()
        else:
            print(f"❌ Bilinmeyen argüman: {arg}")
            show_help()
            sys.exit(1)
    else:
        # Normal modda çalıştır
        sys.exit(main()) 