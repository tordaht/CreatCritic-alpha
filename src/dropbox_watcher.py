"""
Dropbox Klasör İzleyici
Seri No: CR-007-v1.0
"""

import os
import time
import shutil
from typing import List, Optional
from config.settings import DROPBOX_INBOX_PATH, DROPBOX_OUTBOX_PATH, SUPPORTED_FORMATS
from config.credentials import DROPBOX_ACCESS_TOKEN, GEMINI_API_KEY
from .gemini_processor import GeminiProcessor

# Conditional imports for optional dependencies
try:
    from dropbox import Dropbox, exceptions as dbx_exceptions
    from dropbox.files import FileMetadata, FolderMetadata, WriteMode, ListFolderResult
except ImportError:
    Dropbox = None
    files = None

class DropboxWatcher:
    """
    Dropbox klasörünü izleyen ve yeni dosyaları işleyen sınıf
    """
    
    def __init__(self):
        self.access_token = DROPBOX_ACCESS_TOKEN
        self.inbox_path = DROPBOX_INBOX_PATH
        self.outbox_path = DROPBOX_OUTBOX_PATH
        self.serial_no = "CR-007-v1.0"
        
        # Dependency kontrolü
        if Dropbox is None:
            raise ImportError("dropbox kütüphanesi yüklü değil")
        
        # Dropbox client'ı başlat
        if self.access_token:
            self.dbx = Dropbox(self.access_token)
        else:
            self.dbx = None
        
        # Gemini işleyici
        self.gemini_processor = GeminiProcessor()
        
        # API key (config'den al veya sabit kullan)
        self.api_key = GEMINI_API_KEY
        
        # İşlenen dosyaları takip et
        self.processed_files = set()
    
    def start_watching(self, interval: int = 30):
        """
        Dropbox klasörünü izlemeye başlar
        
        Args:
            interval: Kontrol aralığı (saniye)
        """
        print(f"Dropbox izleme başlatıldı: {self.inbox_path}")
        print(f"Seri No: {self.serial_no}")
        
        while True:
            try:
                self._check_for_new_files()
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("Dropbox izleme durduruldu.")
                break
            except Exception as e:
                print(f"Dropbox izleme hatası: {str(e)}")
                time.sleep(interval)
    
    def _list_dropbox_files(self, folder_path: str) -> List:
        """Dropbox klasöründeki dosyaları listeler"""
        if not self.dbx:
            return []
        try:
            result = self.dbx.files_list_folder(folder_path)
            if result and hasattr(result, 'entries'):
                entries = result.entries
                if entries is not None and hasattr(entries, '__iter__'):
                    return list(entries)  # Kesin liste garantisi
            return []
        except Exception as e:
            print(f"Dropbox listeleme hatası: {str(e)}")
            return []

    def _check_for_new_files(self):
        """Yeni dosyaları kontrol eder"""
        if not self.dbx:
            print("Dropbox erişim token'ı bulunamadı")
            return
        
        try:
            # Inbox klasöründeki dosyaları listele - her zaman liste döner
            files = self._list_dropbox_files(self.inbox_path)
            
            # Artık files kesinlikle bir liste (boş olsa bile)
            for file_info in files:
                filename = file_info.name
                file_path = f"{self.inbox_path}{filename}"
                # Dosya daha önce işlenmiş mi kontrol et
                if filename in self.processed_files:
                    continue
                # Dosya formatını kontrol et
                if not self._is_supported_format(filename):
                    print(f"Desteklenmeyen format: {filename}")
                    continue
                # Dosyayı işle
                self._process_file(file_path, filename)
        except Exception as e:
            print(f"Dosya kontrol hatası: {str(e)}")
    
    def _is_supported_format(self, filename: str) -> bool:
        """Dosya formatının desteklenip desteklenmediğini kontrol eder"""
        file_ext = os.path.splitext(filename)[1].lower()
        return file_ext in SUPPORTED_FORMATS
    
    def _process_file(self, file_path: str, filename: str):
        """Dosyayı işler"""
        try:
            print(f"İşleniyor: {filename}")
            
            # Dosyayı geçici olarak indir
            temp_path = self._download_file(file_path, filename)
            
            if temp_path:
                # Gemini ile işle (API key ile)
                critique = self.gemini_processor.process_design_file(temp_path, filename, self.api_key)
                
                # Sonucu Dropbox'a yükle
                self._upload_critique(critique, filename)
                
                # Geçici dosyayı sil
                os.remove(temp_path)
                
                # İşlenen dosyalara ekle
                self.processed_files.add(filename)
                
                print(f"Tamamlandı: {filename}")
            
        except Exception as e:
            print(f"Dosya işleme hatası ({filename}): {str(e)}")
    
    def _download_file(self, dropbox_path: str, filename: str) -> Optional[str]:
        """Dropbox dosyasını geçici olarak indirir"""
        if not self.dbx:
            print("Dropbox bağlantısı yok!")
            return None
        try:
            # Geçici dosya yolu
            temp_path = os.path.join(os.getcwd(), f"temp_{filename}")
            # Dosyayı indir
            with open(temp_path, 'wb') as f:
                metadata, response = self.dbx.files_download(dropbox_path)
                if hasattr(response, 'raw'):
                    shutil.copyfileobj(response.raw, f)
                else:
                    print("Yanıt nesnesinde 'raw' yok!")
                    return None
            return temp_path
        except Exception as e:
            print(f"Dosya indirme hatası: {str(e)}")
            return None
    
    def _upload_critique(self, critique: str, original_filename: str):
        """Eleştiriyi Dropbox'a yükler"""
        if not self.dbx:
            print("Dropbox bağlantısı yok!")
            return
        try:
            # Yeni dosya adı
            base_name = os.path.splitext(original_filename)[0]
            critique_filename = f"{base_name}.comments.txt"
            dropbox_path = f"{self.outbox_path}{critique_filename}"
            # Dosyayı yükle
            self.dbx.files_upload(
                critique.encode('utf-8'),
                dropbox_path,
                mode=WriteMode.overwrite
            )
            print(f"Eleştiri yüklendi: {critique_filename}")
        except Exception as e:
            print(f"Eleştiri yükleme hatası: {str(e)}")

    def validate_connection(self) -> bool:
        """Dropbox bağlantısını test eder"""
        if not self.dbx:
            return False
        try:
            # Hesap bilgilerini al
            account = self.dbx.users_get_current_account()
            email = getattr(account, 'email', None)
            print(f"Dropbox bağlantısı başarılı: {email if email else 'Bilinmiyor'}")
            return True
        except Exception as e:
            print(f"Dropbox bağlantı hatası: {str(e)}")
            return False 