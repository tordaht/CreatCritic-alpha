"""
Ozan Üslup Motoru Test Dosyası
Seri No: CR-014-v1.0
"""

import unittest
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ozan_style_engine import OzanStyleEngine
from src.mathematical_model import OzanMathematicalModel

class TestOzanStyleEngine(unittest.TestCase):
    """Ozan üslup motoru testleri"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        self.ozan_engine = OzanStyleEngine()
        self.mathematical_model = OzanMathematicalModel()
        self.serial_no = "CR-014-v1.0"
    
    def test_serial_number(self):
        """Seri numarası testi"""
        print("Seri numarası testi ... ", end="")
        
        self.assertEqual(self.mathematical_model.serial_no, "CR-021-v1.1")
        print("✅")
    
    def test_action_patterns(self):
        """Aksiyon kalıpları kontrolü"""
        self.assertIsInstance(self.ozan_engine.action_patterns, list)
        self.assertGreater(len(self.ozan_engine.action_patterns), 0)
        
        # Fiil kalıplarının varlığını kontrol et
        expected_actions = ["Kullan", "Değiştir", "Artır", "Azalt"]
        for action in expected_actions:
            self.assertIn(action, self.ozan_engine.action_patterns)
    
    def test_design_elements(self):
        """Tasarım elemanları kontrolü"""
        self.assertIsInstance(self.ozan_engine.design_elements, list)
        self.assertGreater(len(self.ozan_engine.design_elements), 0)
        
        # Tasarım elemanlarının varlığını kontrol et
        expected_elements = ["renk kontrastı", "tipografi", "mizanpaj"]
        for element in expected_elements:
            self.assertIn(element, self.ozan_engine.design_elements)
    
    def test_parse_gemini_response(self):
        """Gemini yanıtı parse etme testi"""
        # Test JSON yanıtı
        json_response = '{"critiques": ["Kullan güçlü kontrast", "Değiştir tipografi"]}'
        result = self.ozan_engine._parse_gemini_response(json_response)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn("Kullan güçlü kontrast", result)
    
    def test_apply_ozan_style(self):
        """Ozan üslubuna dönüştürme testi"""
        test_point = "Renk kontrastı zayıf"
        result = self.ozan_engine._apply_ozan_style(test_point)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_is_brief_independent(self):
        """Brief dışı kontrol testi"""
        # Brief dışı öneri
        brief_independent = "Bu öneri benim deneyimlerimden"
        self.assertTrue(self.ozan_engine._is_brief_independent(brief_independent))
        
        # Brief'e uygun öneri
        brief_compliant = "Brief'te belirtilen renk kullan"
        self.assertFalse(self.ozan_engine._is_brief_independent(brief_compliant))
    
    def test_mathematical_model_utility_function(self):
        """Matematiksel model fayda fonksiyonu testi"""
        factors = {
            "grafik_tasarim_standartlari": 0.85,
            "piyasa_standartlari": 0.78,
            "estetik_islevsellik": 0.72,
            "tasarim_anlatimi": 0.68
        }
        
        utility = self.mathematical_model.calculate_utility_function(factors)
        
        self.assertIsInstance(utility, float)
        self.assertGreaterEqual(utility, 0.0)
        self.assertLessEqual(utility, 1.0)
    
    def test_analyze_critique_pattern(self):
        """Eleştiri örüntü analizi testi"""
        critique_text = "Tipografi hiyerarşisi düzenle, renk kontrastı güçlendir"
        patterns = self.mathematical_model.analyze_critique_pattern(critique_text)

        self.assertIsInstance(patterns, dict)
        self.assertIn("grafik_tasarim_standartlari", patterns)
        self.assertIn("piyasa_standartlari", patterns)
        self.assertIn("estetik_islevsellik", patterns)
        self.assertIn("brief_uygunlugu", patterns)
        print("✅")
    
    def test_generate_action_object_pairs(self):
        """Aksiyon-nesne çifti üretme testi"""
        critique_points = ["Kullan güçlü kontrast", "Değiştir tipografi"]
        pairs = self.mathematical_model.generate_action_object_pairs(critique_points)
        
        self.assertIsInstance(pairs, list)
        self.assertEqual(len(pairs), 2)
        
        # İlk çifti kontrol et
        first_pair = pairs[0]
        self.assertIsInstance(first_pair, tuple)
        self.assertEqual(len(first_pair), 2)
        self.assertEqual(first_pair[0], "Kullan")
        self.assertEqual(first_pair[1], "güçlü kontrast")
    
    def test_calculate_critique_quality_score(self):
        """Eleştiri kalite skoru testi"""
        critique = "Brief'e uygun renk kullan, global trendleri takip et"
        quality_score = self.mathematical_model.calculate_critique_quality_score(critique)
        
        self.assertIsInstance(quality_score, float)
        self.assertGreaterEqual(quality_score, 0.0)
        self.assertLessEqual(quality_score, 1.0)
    
    def test_generate_prompt_for_gemini(self):
        """Gemini prompt üretme testi"""
        filename = "test_design.pdf"
        prompt = self.ozan_engine.generate_prompt_for_gemini(filename)
        
        self.assertIsInstance(prompt, str)
        self.assertIn(filename, prompt)
        self.assertIn("Ozan", prompt)
        self.assertIn("Creative Director", prompt)

if __name__ == '__main__':
    print(f"🧪 Ozan Üslup Motoru Testleri Başlatılıyor...")
    print(f"Seri No: CR-014-v1.0")
    
    # Test suite'i çalıştır
    unittest.main(verbosity=2) 