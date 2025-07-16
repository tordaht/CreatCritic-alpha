"""
CreaCritic Uygulama Ayarları
Seri No: CR-024-v1.1
"""

import os
from pathlib import Path

# Temel Ayarlar
PROJECT_NAME = "CreaCritic"
VERSION = "1.1.1"
SERIAL_NO = "CR-024-v1.1"

# Web Arayüzü Ayarları
UPLOAD_FOLDER = os.path.join("web_interface", "static", "uploads")
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# Dropbox Ayarları
DROPBOX_INBOX_PATH = "dropbox://inbox/"
DROPBOX_OUTBOX_PATH = "dropbox://outbox/"

# Gemini API Ayarları
GEMINI_MODEL = "gemini-1.5-flash-latest"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Ozan Üslup Ayarları
MAX_CRITIQUE_ITEMS = 5
CRITIQUE_FORMAT = "Fiil + Nesne"
BRIEF_INDEPENDENT_NOTE = "Bu benim bilgilerimden harmanlandı"

# Matematiksel Model Ağırlıkları
MATHEMATICAL_WEIGHTS = {
    "grafik_tasarim_standartlari": 0.35,
    "piyasa_standartlari": 0.30,
    "estetik_islevsellik": 0.20,
    "brief_uygunlugu": 0.15
}

# Hata Yönetimi
MAX_RETRY_ATTEMPTS = 3
ERROR_LOG_PATH = "logs/errors.log"

# Dosya İşleme
SUPPORTED_FORMATS = [".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp"]
MAX_FILE_SIZE_MB = 10

# Performans
BATCH_SIZE = 5
PROCESSING_TIMEOUT = 300  # saniye 