"""
Ozan Üslup Motoru - Tasarım Eleştiri Üslubunu Simüle Eder
Seri No: CR-005-v1.0
"""

import re
from typing import List, Dict, Tuple
from config.settings import MAX_CRITIQUE_ITEMS, BRIEF_INDEPENDENT_NOTE
from .mathematical_model import OzanMathematicalModel

class OzanStyleEngine:
    """
    Ozan'ın tasarım eleştiri üslubunu simüle eden motor
    """
    
    def __init__(self):
        self.mathematical_model = OzanMathematicalModel()
        self.serial_no = "CR-005-v1.0"
        
        # Ozan'ın tipik fiil-nesne kalıpları
        self.action_patterns = [
            "Kullan", "Değiştir", "Artır", "Azalt", "Düzenle", "Yerleştir",
            "Kontrol et", "Test et", "Optimize et", "Basitleştir", "Güçlendir",
            "Yumuşat", "Netleştir", "Dengeli yap", "Öne çıkar", "Gizle"
        ]
        
        # Tasarım elemanları
        self.design_elements = [
            "renk kontrastı", "tipografi", "mizanpaj", "boşluk", "görsel hiyerarşi",
            "logo boyutu", "buton yerleşimi", "grid sistemi", "icon seti", "boşluk yönetimi",
            "metin uzunluğu", "font seçimi", "hizalama", "doygunluk", "animasyon",
            "arka plan", "görsel ağırlık", "hover efekti", "CTA", "navigation"
        ]
    
    def generate_ozan_critique(self, gemini_response: str, filename: str) -> str:
        """
        Gemini'den gelen cevabı doğal ve akıcı şekilde döndürür.
        """
        # Eğer cevap madde madde ise, cümleleri birleştir
        lines = [line.strip() for line in gemini_response.split('\n') if line.strip()]
        # Eğer çok kısa ve madde madde ise, cümleleri birleştir
        if len(lines) > 2 and all(len(line) < 100 for line in lines):
            return ' '.join(lines)
        # Eğer zaten doğal bir paragraf ise, olduğu gibi döndür
        return gemini_response.strip()
    
    def _parse_gemini_response(self, response: str) -> List[str]:
        """Gemini yanıtını eleştiri noktalarına ayırır"""
        # JSON formatından critiques alanını çıkar
        import json
        try:
            data = json.loads(response)
            if "critiques" in data:
                return data["critiques"]
        except:
            pass
        
        # JSON parse edilemezse satır satır ayır
        lines = response.strip().split('\n')
        critique_points = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Madde işaretlerini temizle
                line = re.sub(r'^[\d\-\.\s]+', '', line)
                if line:
                    critique_points.append(line)
        
        return critique_points[:MAX_CRITIQUE_ITEMS]
    
    def _convert_to_ozan_style(self, critique_points: List[str], filename: str) -> str:
        """Eleştiri noktalarını Ozan üslubuna dönüştürür"""
        ozan_critique = f"{filename} için Tasarım Eleştirisi / Yönlendirme:\n\n"
        
        for i, point in enumerate(critique_points, 1):
            # Ozan üslubuna dönüştür
            ozan_style_point = self._apply_ozan_style(point)
            
            # Brief dışı öneriler için not ekle
            if self._is_brief_independent(point):
                ozan_style_point += f" ({BRIEF_INDEPENDENT_NOTE})"
            
            ozan_critique += f"{i}. {ozan_style_point}\n"
        
        return ozan_critique
    
    def _apply_ozan_style(self, point: str) -> str:
        """Tek bir eleştiri noktasını Ozan üslubuna dönüştürür"""
        # Kısa ve aksiyon odaklı yap
        point = point.strip()
        
        # Tekrarlanan "Kullan" kelimelerini temizle
        point = re.sub(r'kullan\s+kullan', 'kullan', point, flags=re.IGNORECASE)
        
        # Fiil-nesne formatına dönüştür
        if not any(action in point.lower() for action in self.action_patterns):
            # Fiil ekle
            point = f"Kullan {point.lower()}"
        
        # Kısa tut (maksimum 10 kelime)
        words = point.split()
        if len(words) > 10:
            point = " ".join(words[:10])
        
        return point
    
    def _is_brief_independent(self, point: str) -> bool:
        """Eleştiri noktasının brief dışı olup olmadığını kontrol eder"""
        brief_keywords = ["brief", "müşteri", "talep", "istek", "belirtilen"]
        point_lower = point.lower()
        
        # Brief anahtar kelimeleri yoksa brief dışı kabul et
        return not any(keyword in point_lower for keyword in brief_keywords)
    
    def _improve_critique_quality(self, critique: str) -> str:
        """Eleştiri kalitesini iyileştirir"""
        # Matematiksel model ile analiz et
        factors = self.mathematical_model.analyze_critique_pattern(critique)
        
        # En düşük skorlu faktörü iyileştir
        min_factor = min(factors.items(), key=lambda x: x[1])
        
        if min_factor[0] == "brief_uyumu":
            critique += "\n\nNot: Brief'e daha sıkı bağlı kalın."
        elif min_factor[0] == "global_trend":
            critique += "\n\nNot: Global trendleri göz önüne alın."
        elif min_factor[0] == "teknik_uygulanabilirlik":
            critique += "\n\nNot: Teknik sınırlamaları kontrol edin."
        
        return critique
    
    def generate_prompt_for_gemini(self, filename: str) -> str:
        """Gemini API için prompt oluşturur"""
        return f"""You are Ozan, Creative Director at Beezy Design Studio. 

İncelediğin tasarım: {filename}

Lütfen şu kriterlere göre eleştiri yap:

1. Brief'e sıkı sıkıya bağlı kal; eksikse belirt.
2. Global trend ve teknik sınırlamaları göz önüne al.
3. Eleştirileri madde madde, kısa ve aksiyon odaklı ver.
4. Eğer öneriniz brief'ten bağımsızsa, 'bu benim bilgilerimden harmanlandı' notunu ekle.

Yanıtını JSON formatında ver:
{{
    "critiques": [
        "Fiil + Nesne formatında eleştiri 1",
        "Fiil + Nesne formatında eleştiri 2",
        ...
    ]
}}

Maksimum 5 madde ver.""" 