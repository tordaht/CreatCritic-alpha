"""
Hata Yönetimi Sistemi
Seri No: CR-009-v1.0
"""

import os
import logging
import traceback
from datetime import datetime
from typing import Optional
from config.settings import ERROR_LOG_PATH, MAX_RETRY_ATTEMPTS

class ErrorHandler:
    """
    Sistem hatalarını yöneten ve loglayan sınıf
    """
    
    def __init__(self):
        self.serial_no = "CR-009-v1.0"
        self.max_retries = MAX_RETRY_ATTEMPTS
        
        # Logging yapılandırması
        self._setup_logging()
    
    def _setup_logging(self):
        """Logging sistemini yapılandırır"""
        # Log klasörünü oluştur
        log_dir = os.path.dirname(ERROR_LOG_PATH)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Logger'ı yapılandır
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('CreaCritic')
    
    def log_error(self, error: Exception, context: str = "", filename: str = None):
        """
        Hatayı loglar
        
        Args:
            error: Hata objesi
            context: Hata bağlamı
            filename: İlgili dosya adı
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        error_info = {
            "timestamp": timestamp,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "filename": filename or "N/A",
            "traceback": traceback.format_exc()
        }
        
        # Log mesajını oluştur
        log_message = f"""
HATA ÇÖZÜMLERİ - CreaCritic
============================
Tarih: {timestamp}
Hata Türü: {error_info['error_type']}
Mesaj: {error_info['error_message']}
Bağlam: {error_info['context']}
Dosya: {error_info['filename'] or 'N/A'}
Seri No: {self.serial_no}

Traceback:
{error_info['traceback']}
"""
        
        # Dosyaya yaz
        self.logger.error(log_message)
        
        # HATA ÇÖZÜMLERİ.txt dosyasına da ekle
        self._append_to_error_file(error_info)
    
    def _append_to_error_file(self, error_info: dict):
        """Hatayı HATA ÇÖZÜMLERİ.txt dosyasına ekler"""
        try:
            with open("HATA ÇÖZÜMLERİ.txt", "a", encoding="utf-8") as f:
                f.write(f"""
HATA ÇÖZÜMLERİ - Yeni Hata
===========================
Tarih: {error_info['timestamp']}
Hata Türü: {error_info['error_type']}
Mesaj: {error_info['error_message']}
Bağlam: {error_info['context']}
Dosya: {error_info['filename'] or 'N/A'}
Seri No: {self.serial_no}

ÇÖZÜM:
- Hata analiz edildi
- Log dosyasına kaydedildi
- Sistem durumu kontrol edildi

""")
        except Exception as e:
            print(f"Hata dosyasına yazma hatası: {str(e)}")
    
    def retry_operation(self, operation, *args, **kwargs):
        """
        İşlemi yeniden deneme mekanizması
        
        Args:
            operation: Çalıştırılacak fonksiyon
            *args: Fonksiyon argümanları
            **kwargs: Fonksiyon keyword argümanları
            
        Returns:
            İşlem sonucu veya None (başarısız)
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                result = operation(*args, **kwargs)
                if attempt > 0:
                    print(f"İşlem başarılı (deneme {attempt + 1}/{self.max_retries})")
                return result
                
            except Exception as e:
                last_error = e
                print(f"Deneme {attempt + 1}/{self.max_retries} başarısız: {str(e)}")
                
                # Hatayı logla
                self.log_error(e, f"Retry attempt {attempt + 1}")
                
                if attempt < self.max_retries - 1:
                    print("Yeniden deneniyor...")
        
        # Tüm denemeler başarısız
        print(f"İşlem {self.max_retries} deneme sonrası başarısız")
        if last_error:
            self.log_error(last_error, "Final retry failure")
        
        return None
    
    def validate_system_health(self) -> bool:
        """
        Sistem sağlığını kontrol eder
        
        Returns:
            bool: Sistem sağlıklı mı
        """
        health_checks = [
            self._check_log_directory(),
            self._check_dependencies(),
            self._check_permissions()
        ]
        
        return all(health_checks)
    
    def _check_log_directory(self) -> bool:
        """Log klasörünün varlığını kontrol eder"""
        try:
            log_dir = os.path.dirname(ERROR_LOG_PATH)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            return True
        except Exception as e:
            self.log_error(e, "Log directory check failed")
            return False
    
    def _check_dependencies(self) -> bool:
        """Gerekli kütüphanelerin varlığını kontrol eder"""
        required_modules = [
            'google.generativeai',
            'dropbox',
            'slack_sdk',
            'PIL'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            error_msg = f"Eksik kütüphaneler: {', '.join(missing_modules)}"
            self.log_error(Exception(error_msg), "Dependency check")
            return False
        
        return True
    
    def _check_permissions(self) -> bool:
        """Dosya yazma izinlerini kontrol eder"""
        try:
            # Test dosyası oluştur
            test_file = "test_write_permission.tmp"
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except Exception as e:
            self.log_error(e, "Permission check failed")
            return False 