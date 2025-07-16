"""
Ozan'ın Tasarım Karar Mekanizmalarının Matematiksel Modellemesi
Seri No: CR-021-v1.1
"""

import numpy as np
from typing import Dict, List, Tuple
from config.settings import MATHEMATICAL_WEIGHTS

class OzanMathematicalModel:
    """
    Ozan'ın tasarım eleştiri kararlarını matematiksel olarak modelleyen sınıf
    """
    
    def __init__(self):
        self.weights = MATHEMATICAL_WEIGHTS
        self.serial_no = "CR-021-v1.1"
        
        # Ozan'ın cevap yapısı kategorileri
        self.ozan_response_categories = {
            "brief_odakli": 0.40,      # Brief Odaklı Yaklaşım
            "teknik_detay": 0.25,      # Teknik Detay Odaklı
            "estetik_analitik": 0.20,  # Estetik-Analitik Denge
            "global_benchmark": 0.10,  # Global Benchmark Referansı
            "aksiyon_odakli": 0.05     # Aksiyon Odaklı Öneriler
        }
    
    def calculate_dynamic_weights(self, has_brief: bool = False, has_design_statement: bool = False) -> Dict[str, float]:
        """
        Brief ve tasarım savunması durumlarına göre dinamik ağırlık hesaplar
        
        Args:
            has_brief: Müşteri briefi var mı?
            has_design_statement: Tasarım savunması var mı?
            
        Returns:
            Dict: Dinamik ağırlıklar
        """
        # Temel ağırlıklar
        base_weights = {
            "grafik_tasarim_standartlari": 0.35,
            "piyasa_standartlari": 0.30,
            "estetik_islevsellik": 0.20,
            "brief_uygunlugu": 0.15
        }
        
        # Brief varsa %50 ağırlık ver
        if has_brief:
            base_weights["brief_uygunlugu"] = 0.50
            
            # Diğer ağırlıkları orantılı olarak azalt
            remaining_weight = 0.50  # 1.0 - 0.50 = 0.50
            other_factors = ["grafik_tasarim_standartlari", "piyasa_standartlari", "estetik_islevsellik"]
            
            # Tasarım savunması da varsa estetik_islevsellik'e %15 ver
            if has_design_statement:
                base_weights["estetik_islevsellik"] = 0.15
                remaining_weight = 0.35  # 0.50 - 0.15 = 0.35
                other_factors = ["grafik_tasarim_standartlari", "piyasa_standartlari"]
            
            # Kalan ağırlığı diğer faktörlere orantılı dağıt
            total_other_weight = sum(base_weights[factor] for factor in other_factors)
            for factor in other_factors:
                if total_other_weight > 0:
                    base_weights[factor] = (base_weights[factor] / total_other_weight) * remaining_weight
        
        # Brief yoksa tasarım savunması varsa estetik_islevsellik'e %15 ver
        elif has_design_statement:
            base_weights["estetik_islevsellik"] = 0.15
            
            # Diğer ağırlıkları orantılı olarak azalt
            remaining_weight = 0.85  # 1.0 - 0.15 = 0.85
            other_factors = ["grafik_tasarim_standartlari", "piyasa_standartlari", "brief_uygunlugu"]
            
            total_other_weight = sum(base_weights[factor] for factor in other_factors)
            for factor in other_factors:
                if total_other_weight > 0:
                    base_weights[factor] = (base_weights[factor] / total_other_weight) * remaining_weight
        
        return base_weights
    
    def calculate_ozan_response_weights(self, has_brief: bool = False, has_design_statement: bool = False) -> Dict[str, float]:
        """
        Ozan'ın cevap yapısı kategorilerinin dinamik ağırlıklarını hesaplar
        
        Args:
            has_brief: Müşteri briefi var mı?
            has_design_statement: Tasarım savunması var mı?
            
        Returns:
            Dict: Ozan cevap kategorileri ağırlıkları
        """
        weights = self.ozan_response_categories.copy()
        
        # Brief varsa brief_odakli ağırlığını artır
        if has_brief:
            weights["brief_odakli"] = 0.50
            weights["teknik_detay"] = 0.20
            weights["estetik_analitik"] = 0.15
            weights["global_benchmark"] = 0.10
            weights["aksiyon_odakli"] = 0.05
        
        # Tasarım savunması varsa estetik_analitik ağırlığını artır
        if has_design_statement:
            weights["estetik_analitik"] = 0.30
            weights["brief_odakli"] = 0.35
            weights["teknik_detay"] = 0.20
            weights["global_benchmark"] = 0.10
            weights["aksiyon_odakli"] = 0.05
        
        return weights
    
    def generate_ozan_style_prompt(self, has_brief: bool = False, has_design_statement: bool = False) -> str:
        """
        Ozan'ın cevap yapısına uygun LLM prompt'u oluşturur
        
        Args:
            has_brief: Müşteri briefi var mı?
            has_design_statement: Tasarım savunması var mı?
            
        Returns:
            str: Ozan üslubunda prompt
        """
        response_weights = self.calculate_ozan_response_weights(has_brief, has_design_statement)
        
        prompt = """
Ozan Bayar (Beezy Design Studio Creative Director) üslubunda tasarım eleştirisi yap:

CEVAP YAPISI (%40 Brief Odaklı, %25 Teknik Detay, %20 Estetik-Analitik, %10 Global Benchmark, %5 Aksiyon Odaklı):

1. BRIEF ODAKLI (%40): "Bu görsel öğe brief'e uygun değil; marka paletindeki onaylı renkleri kullanın."
2. TEKNİK DETAY (%25): "Işık–gölge dengesi çok yumuşak; global illumination'ı %15 artırın."
3. ESTETİK-ANALİTİK (%20): "Kompozisyon merkez kaçıyor; öğeyi altın oran noktasına kaydırın."
4. GLOBAL BENCHMARK (%10): "Bu versiyon, global benchmark'ları yüzde 5 geriden geliyor."
5. AKSİYON ODAKLI (%5): "Revizyon talebini ayrıntılı liste olarak paylaşın."

KURALLAR:
- Kısa, aksiyon odaklı cümleler kullan
- "Fiil + Nesne" formatında öneriler ver
- Spesifik sayısal değerler, yüzde oranları ekle
- Global trend ve benchmark referansları ver
- Teknik sınırlamalara dikkat et
- Her cümle direkt aksiyon önerisi içersin
- Doğal, samimi ama profesyonel ton kullan
- Gereksiz tekrar ve şablon kullanma
- Her madde gerçek bir tasarımcı gibi kısa, net ve açıklayıcı olsun

ÖRNEK CÜMLE KALIPLARI:
- "Tipografi kontrastı zayıf kalmış; başlığı yüksek ağırlıklı bir fontla vurgulayalım."
- "Mizanpajda asimetri fazla; grid'e geri dönün ve sola hizalayın."
- "CTA butonunun erişim alanı dar; padding'i %20 genişletin."
- "Dosya boyutu büyük; texture sıkıştırmasını 2:1'e çekin."
"""
        
        return prompt
    
    def calculate_utility_function(self, factors: Dict[str, float], has_brief: bool = False, has_design_statement: bool = False) -> float:
        """
        Fayda fonksiyonu: Dinamik ağırlıklarla U(x) = w1*x1 + w2*x2 + w3*x3 + w4*x4
        
        Args:
            factors: Faktör değerleri sözlüğü
            has_brief: Müşteri briefi var mı?
            has_design_statement: Tasarım savunması var mı?
            
        Returns:
            float: Fayda skoru (0-1 arası)
        """
        # Dinamik ağırlıkları hesapla
        dynamic_weights = self.calculate_dynamic_weights(has_brief, has_design_statement)
        
        utility = 0.0
        
        for factor_name, weight in dynamic_weights.items():
            if factor_name in factors:
                utility += weight * factors[factor_name]
        
        return min(max(utility, 0.0), 1.0)  # 0-1 arasına sınırla
    
    def analyze_critique_pattern(self, critique_text: str) -> Dict[str, float]:
        """
        Eleştiri metninden örüntü analizi yapar
        
        Args:
            critique_text: Eleştiri metni
            
        Returns:
            Dict: Örüntü skorları
        """
        patterns = {
            "grafik_tasarim_standartlari": 0.0,
            "piyasa_standartlari": 0.0,
            "estetik_islevsellik": 0.0,
            "brief_uygunlugu": 0.0
        }
        
        text_lower = critique_text.lower()
        
        # Grafik tasarım standartları analizi
        graphic_keywords = ["tipografi", "renk", "kontrast", "hizalama", "grid", "mizanpaj", "kompozisyon", "hierarşi"]
        patterns["grafik_tasarim_standartlari"] = self._calculate_keyword_score(text_lower, graphic_keywords)
        
        # Piyasa standartları analizi
        market_keywords = ["piyasa", "standart", "trend", "global", "modern", "güncel", "çağdaş", "sektör"]
        patterns["piyasa_standartlari"] = self._calculate_keyword_score(text_lower, market_keywords)
        
        # Estetik ve işlevsellik analizi
        aesthetic_keywords = ["estetik", "görsel", "işlevsel", "kullanılabilir", "ergonomik", "güzel", "uyumlu"]
        patterns["estetik_islevsellik"] = self._calculate_keyword_score(text_lower, aesthetic_keywords)
        
        # Brief uygunluğu analizi
        brief_keywords = ["brief", "müşteri", "istek", "uygun", "uyumlu", "beklenti", "talep"]
        patterns["brief_uygunlugu"] = self._calculate_keyword_score(text_lower, brief_keywords)
        
        return patterns
    
    def analyze_ozan_response_categories(self, critique_text: str, has_brief: bool = False) -> Dict[str, float]:
        """
        Eleştiri metninden Ozan'ın cevap kategorilerini analiz eder
        
        Args:
            critique_text: Eleştiri metni
            has_brief: Brief bilgisi var mı?
            
        Returns:
            Dict: Kategori skorları
        """
        categories = {
            "brief_odakli": 0.0,
            "teknik_detay": 0.0,
            "estetik_analitik": 0.0,
            "global_benchmark": 0.0,
            "aksiyon_odakli": 0.0
        }
        
        text_lower = critique_text.lower()
        
        # Brief odaklı analizi - sadece brief varsa hesapla
        if has_brief:
            brief_keywords = ["brief", "müşteri", "istek", "uygun", "uyumlu", "beklenti", "talep", "deneyimlerimden"]
            categories["brief_odakli"] = self._calculate_keyword_score(text_lower, brief_keywords)
        else:
            # Brief yoksa brief odaklı skoru 0 yap
            categories["brief_odakli"] = 0.0
        
        # Teknik detay analizi
        technical_keywords = ["%", "pixel", "px", "fps", "dpi", "resolution", "texture", "render", "poly", "offset", "bias", "hardness"]
        categories["teknik_detay"] = self._calculate_keyword_score(text_lower, technical_keywords)
        
        # Estetik-analitik analizi
        aesthetic_keywords = ["kompozisyon", "altın oran", "merkez", "dengeli", "uyumlu", "görsel", "estetik"]
        categories["estetik_analitik"] = self._calculate_keyword_score(text_lower, aesthetic_keywords)
        
        # Global benchmark analizi
        benchmark_keywords = ["global", "benchmark", "standart", "trend", "modern", "çağdaş", "sektör", "piyasa"]
        categories["global_benchmark"] = self._calculate_keyword_score(text_lower, benchmark_keywords)
        
        # Aksiyon odaklı analizi
        action_keywords = ["artırın", "azaltın", "değiştirin", "kaydırın", "ekleyin", "kaldırın", "güncelleyin", "düzeltin"]
        categories["aksiyon_odakli"] = self._calculate_keyword_score(text_lower, action_keywords)
        
        return categories
    
    def _calculate_keyword_score(self, text: str, keywords: List[str]) -> float:
        """Gelişmiş anahtar kelime skoru hesaplar"""
        score = 0.0
        text_words = text.split()
        
        for keyword in keywords:
            # Tam kelime eşleşmesi
            if keyword in text_words:
                score += 0.3
            # Kısmi eşleşme
            elif keyword in text:
                score += 0.15
            # Benzer kelimeler
            elif any(keyword in word or word in keyword for word in text_words):
                score += 0.1
        
        # Pozitif kelimeler için bonus
        positive_words = ["iyi", "güzel", "başarılı", "uygun", "doğru", "kaliteli", "profesyonel"]
        for word in positive_words:
            if word in text:
                score += 0.05
        
        # Negatif kelimeler için düşürme
        negative_words = ["kötü", "yanlış", "uygunsuz", "zayıf", "eksik", "hatalı"]
        for word in negative_words:
            if word in text:
                score -= 0.05
        
        return min(max(score, 0.0), 1.0)
    
    def optimize_critique(self, current_factors: Dict[str, float]) -> Dict[str, float]:
        """
        Eleştiriyi optimize eder - gradyan artışı ile
        
        Args:
            current_factors: Mevcut faktör değerleri
            
        Returns:
            Dict: Optimize edilmiş faktör değerleri
        """
        learning_rate = 0.1
        optimized_factors = current_factors.copy()
        
        # En düşük skorlu faktörü bul ve artır
        min_factor = min(current_factors.items(), key=lambda x: x[1])
        factor_name = min_factor[0]
        
        optimized_factors[factor_name] = min(
            current_factors[factor_name] + learning_rate, 
            1.0
        )
        
        return optimized_factors
    
    def generate_action_object_pairs(self, critique_points: List[str]) -> List[Tuple[str, str]]:
        """
        "Fiil + Nesne" formatında aksiyon-nesne çiftleri oluşturur
        
        Args:
            critique_points: Eleştiri noktaları
            
        Returns:
            List: (Fiil, Nesne) çiftleri
        """
        action_object_pairs = []
        
        for point in critique_points:
            # Basit fiil-nesne ayrıştırma
            words = point.split()
            if len(words) >= 2:
                # İlk kelime fiil, geri kalanı nesne
                action = words[0]
                object_part = " ".join(words[1:])
                action_object_pairs.append((action, object_part))
        
        return action_object_pairs
    
    def calculate_critique_quality_score(self, critique: str) -> float:
        """
        Eleştiri kalite skorunu hesaplar
        
        Args:
            critique: Eleştiri metni
            
        Returns:
            float: Kalite skoru (0-1)
        """
        factors = self.analyze_critique_pattern(critique)
        return self.calculate_utility_function(factors) 