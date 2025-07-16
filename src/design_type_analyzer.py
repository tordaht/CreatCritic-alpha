"""
Tasarım Türü Analiz Sistemi
Seri No: CR-020-v1.0
"""

import os
from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
import numpy as np

class DesignType(Enum):
    """Tasarım türleri"""
    GRAPHIC_DESIGN = "grafik_tasarim"
    BRANDING = "giydirme_markalama"
    BRANDING_APPLICATION = "markalama_giydirme"
    RENDER_3D = "3d_render"
    THREE_D_RENDER = "3d_render"
    UI_UX = "ui_ux"
    ILLUSTRATION = "illustration"
    PHOTOGRAPHY = "photography"
    ARCHITECTURE = "architecture"
    KEYVISUAL = "keyvisual_poster_event"

@dataclass
class DesignCriteria:
    """Tasarım kriterleri"""
    name: str
    weight: float
    description: str
    evaluation_prompt: str

class DesignTypeAnalyzer:
    """
    Farklı tasarım türleri için özelleştirilmiş analiz sistemi
    """
    
    def __init__(self):
        self.serial_no = "CR-020-v1.0"
        self.design_criteria = self._initialize_criteria()
    
    def _initialize_criteria(self) -> Dict[DesignType, List[DesignCriteria]]:
        """Tasarım türlerine göre kriterleri başlat"""
        
        criteria = {}
        
        # Grafik Tasarım Kriterleri
        criteria[DesignType.GRAPHIC_DESIGN] = [
            DesignCriteria("tipografi", 0.25, "Yazı tipi seçimi ve hiyerarşi", 
                         "Tipografi kalitesi, font seçimi, okunabilirlik"),
            DesignCriteria("renk_kullanimi", 0.20, "Renk paleti ve kontrast", 
                         "Renk uyumu, kontrast, marka tutarlılığı"),
            DesignCriteria("kompozisyon", 0.25, "Görsel düzen ve hiyerarşi", 
                         "Kompozisyon dengesi, görsel akış, odak noktası"),
            DesignCriteria("teknik_kalite", 0.15, "Çözünürlük ve baskı uyumluluğu", 
                         "Çözünürlük, dosya formatı, baskı kalitesi"),
            DesignCriteria("yaraticilik", 0.15, "Özgünlük ve yaratıcı yaklaşım", 
                         "Yaratıcı konsept, özgünlük, trend uyumu")
        ]
        
        # Markalama/Giydirme Kriterleri
        criteria[DesignType.BRANDING] = [
            DesignCriteria("marka_tutarliligi", 0.30, "Marka kimliği tutarlılığı", 
                         "Marka değerleri, tutarlılık, kimlik uyumu"),
            DesignCriteria("uygulanabilirlik", 0.25, "Farklı ortamlarda kullanım", 
                         "Ölçeklenebilirlik, farklı medya uyumu"),
            DesignCriteria("ayirt_edilebilirlik", 0.20, "Rakip markalardan farklılaşma", 
                         "Benzersizlik, ayırt edilebilirlik"),
            DesignCriteria("sadelik", 0.15, "Basit ve anlaşılır tasarım", 
                         "Sadelik, anlaşılabilirlik, netlik"),
            DesignCriteria("surdurulebilirlik", 0.10, "Uzun vadeli kullanım", 
                         "Zaman aşımına dayanıklılık, güncellenebilirlik")
        ]
        
        # BRANDING_APPLICATION için aynı kriterler
        criteria[DesignType.BRANDING_APPLICATION] = criteria[DesignType.BRANDING]
        
        # 3D Render Kriterleri
        criteria[DesignType.RENDER_3D] = [
            DesignCriteria("isiklandirma", 0.25, "Işık-gölge kalitesi", 
                         "Global illumination, gölge detayları, ışık kalitesi"),
            DesignCriteria("materyal_kalitesi", 0.25, "Yüzey materyalleri ve dokular", 
                         "Materyal gerçekçiliği, doku kalitesi, yüzey detayları"),
            DesignCriteria("kompozisyon", 0.20, "Görsel düzen ve kamera açısı", 
                         "Kamera açısı, kompozisyon, görsel hiyerarşi"),
            DesignCriteria("teknik_kalite", 0.20, "Render kalitesi ve optimizasyon", 
                         "Anti-aliasing, çözünürlük, render kalitesi"),
            DesignCriteria("gerceklik", 0.10, "Fotorealistik görünüm", 
                         "Gerçekçilik, detay seviyesi, inandırıcılık")
        ]
        
        # THREE_D_RENDER için aynı kriterler
        criteria[DesignType.THREE_D_RENDER] = criteria[DesignType.RENDER_3D]
        
        # UI/UX Kriterleri
        criteria[DesignType.UI_UX] = [
            DesignCriteria("kullanilabilirlik", 0.30, "Kullanıcı deneyimi", 
                         "Kullanım kolaylığı, sezgisellik, erişilebilirlik"),
            DesignCriteria("gorsel_hierarsi", 0.25, "Görsel düzen ve navigasyon", 
                         "Bilgi hiyerarşisi, navigasyon, görsel akış"),
            DesignCriteria("tutarlilik", 0.20, "Tasarım sistemi tutarlılığı", 
                         "Tutarlı tasarım dili, component sistemi"),
            DesignCriteria("responsive", 0.15, "Farklı cihaz uyumluluğu", 
                         "Responsive tasarım, cihaz uyumluluğu"),
            DesignCriteria("performans", 0.10, "Teknik performans", 
                         "Yükleme hızı, optimizasyon, teknik kalite")
        ]
        
        # İllüstrasyon Kriterleri
        criteria[DesignType.ILLUSTRATION] = [
            DesignCriteria("sanatsal_kalite", 0.30, "Sanatsal değer ve yaratıcılık", 
                         "Sanatsal kalite, yaratıcılık, özgünlük"),
            DesignCriteria("teknik_beceri", 0.25, "Çizim ve teknik beceri", 
                         "Çizim kalitesi, teknik beceri, detay seviyesi"),
            DesignCriteria("stil_tutarliligi", 0.20, "Sanat stili tutarlılığı", 
                         "Stil tutarlılığı, sanat dili"),
            DesignCriteria("kompozisyon", 0.15, "Görsel düzen", 
                         "Kompozisyon, görsel akış, denge"),
            DesignCriteria("renk_kullanimi", 0.10, "Renk paleti", 
                         "Renk uyumu, palet seçimi")
        ]
        
        # Fotoğraf Kriterleri
        criteria[DesignType.PHOTOGRAPHY] = [
            DesignCriteria("teknik_kalite", 0.25, "Fotoğraf teknik kalitesi", 
                         "Netlik, çözünürlük, teknik kalite"),
            DesignCriteria("kompozisyon", 0.25, "Fotoğraf kompozisyonu", 
                         "Kompozisyon kuralları, görsel düzen"),
            DesignCriteria("isiklandirma", 0.20, "Işık kullanımı", 
                         "Işık kalitesi, pozlama, ışık dengesi"),
            DesignCriteria("yaraticilik", 0.15, "Yaratıcı yaklaşım", 
                         "Yaratıcı konsept, özgün bakış açısı"),
            DesignCriteria("konu_secimi", 0.15, "Konu ve içerik", 
                         "Konu seçimi, içerik kalitesi, anlatım")
        ]
        
        # Mimari Kriterleri
        criteria[DesignType.ARCHITECTURE] = [
            DesignCriteria("fonksiyonellik", 0.30, "Mimari fonksiyonellik", 
                         "Kullanım amacına uygunluk, fonksiyonel tasarım"),
            DesignCriteria("estetik_kalite", 0.25, "Görsel estetik", 
                         "Estetik kalite, görsel çekicilik"),
            DesignCriteria("teknik_detay", 0.20, "Teknik detaylar", 
                         "Teknik çözümler, yapısal detaylar"),
            DesignCriteria("cevre_uyumu", 0.15, "Çevre ile uyum", 
                         "Çevre uyumu, sürdürülebilirlik"),
            DesignCriteria("yaraticilik", 0.10, "Yaratıcı yaklaşım", 
                         "Özgün tasarım, yaratıcı çözümler")
        ]
        
        # Keyvisual/Poster/Event Kriterleri
        criteria[DesignType.KEYVISUAL] = [
            DesignCriteria("grafik_tasarim_standartlari", 0.35, "Grafik tasarım standartları", "Tipografi, renk, kompozisyon, marka uyumu"),
            DesignCriteria("piyasa_standartlari", 0.30, "Piyasa trendleri ve güncellik", "Güncel trendler, sektörel uyum, çağdaşlık"),
            DesignCriteria("etki_gucu", 0.20, "Görsel etki ve dikkat çekicilik", "Dikkat çekicilik, ilk izlenim, vurgu"),
            DesignCriteria("teknik_kalite", 0.10, "Teknik kalite ve baskı uyumu", "Çözünürlük, baskı uyumu, dosya kalitesi"),
            DesignCriteria("yaraticilik", 0.05, "Yaratıcılık ve özgünlük", "Özgün fikir, yaratıcı yaklaşım")
        ]
        
        return criteria
    
    def detect_design_type(self, file_path: str, filename: str) -> DesignType:
        """Dosya adı ve içeriğe göre tasarım türünü tespit et"""
        
        filename_lower = filename.lower()
        
        # Önce mimariyi kontrol et
        if any(keyword in filename_lower for keyword in ['architecture', 'building', 'plan', 'section']):
            return DesignType.ARCHITECTURE
        elif any(keyword in filename_lower for keyword in ['keyvisual', 'poster', 'event', 'afiş', 'banner', 'invitation', 'experience day']):
            return DesignType.KEYVISUAL
        elif any(keyword in filename_lower for keyword in ['logo', 'brand', 'identity', 'corporate']):
            return DesignType.BRANDING
        elif any(keyword in filename_lower for keyword in ['render', '3d', 'model', 'vray', 'arnold']):
            return DesignType.RENDER_3D
        elif any(keyword in filename_lower for keyword in ['ui', 'ux', 'interface', 'app', 'web']):
            return DesignType.UI_UX
        elif any(keyword in filename_lower for keyword in ['illustration', 'drawing', 'art', 'sketch']):
            return DesignType.ILLUSTRATION
        elif any(keyword in filename_lower for keyword in ['photo', 'image', 'shot', 'camera']):
            return DesignType.PHOTOGRAPHY
        else:
            # Dosya adından anlaşılamıyorsa, görsel analiz yapılacak
            return DesignType.GRAPHIC_DESIGN  # Varsayılan
    
    def get_criteria_for_type(self, design_type: DesignType) -> List[DesignCriteria]:
        """Tasarım türüne göre kriterleri döndür"""
        return self.design_criteria.get(design_type, [])
    
    def generate_prompt_for_type(self, design_type: DesignType, filename: str) -> str:
        """Tasarım türüne özel prompt oluştur"""
        
        criteria = self.get_criteria_for_type(design_type)
        
        prompt = f"""
Bu {filename} dosyasını {design_type.value.replace('_', ' ')} açısından analiz edin.

Aşağıdaki kriterlere göre değerlendirin:

"""
        
        for criterion in criteria:
            prompt += f"- {criterion.name.replace('_', ' ').title()}: {criterion.description}\n"
        
        prompt += f"""
Her kriter için 0-100 arası puan verin ve detaylı açıklama yapın.
Sonuçları Türkçe olarak sunun.
"""
        
        return prompt
    
    def calculate_weighted_score(self, scores: Dict[str, float], design_type: DesignType) -> float:
        """Ağırlıklı puan hesapla"""
        
        criteria = self.get_criteria_for_type(design_type)
        total_score = 0.0
        total_weight = 0.0
        
        for criterion in criteria:
            if criterion.name in scores:
                total_score += scores[criterion.name] * criterion.weight
                total_weight += criterion.weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def generate_type_specific_feedback(self, design_type: DesignType, scores: Dict[str, float]) -> str:
        """Tasarım türüne özel geri bildirim oluştur"""
        
        criteria = self.get_criteria_for_type(design_type)
        feedback = []
        
        for criterion in criteria:
            if criterion.name in scores:
                score = scores[criterion.name]
                if score < 60:
                    feedback.append(f"{criterion.description} zayıf; {criterion.evaluation_prompt} iyileştirin.")
                elif score < 80:
                    feedback.append(f"{criterion.description} orta; {criterion.evaluation_prompt} geliştirin.")
                else:
                    feedback.append(f"{criterion.description} güçlü; bu alanı koruyun.")
        
        return "\n".join(feedback) 