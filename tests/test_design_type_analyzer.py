"""
Tasarım Türü Analizörü Testleri
Seri No: CR-021-v1.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.design_type_analyzer import DesignTypeAnalyzer, DesignType
import unittest

class TestDesignTypeAnalyzer(unittest.TestCase):
    """Tasarım türü analizörü testleri"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        self.analyzer = DesignTypeAnalyzer()
        print("🧪 Tasarım Türü Analizörü Testleri Başlatılıyor...")
        print(f"Seri No: {self.analyzer.serial_no}")
    
    def test_design_type_detection(self):
        """Tasarım türü tespiti testi"""
        print("Tasarım türü tespiti testi ... ", end="")
        
        # Test dosya adları
        test_cases = [
            ("logo_corporate.png", DesignType.BRANDING),
            ("3d_render_vray.jpg", DesignType.RENDER_3D),
            ("ui_interface_app.png", DesignType.UI_UX),
            ("illustration_art.jpg", DesignType.ILLUSTRATION),
            ("photo_camera_shot.jpg", DesignType.PHOTOGRAPHY),
            ("architecture_building.png", DesignType.ARCHITECTURE),
            ("keyvisual_event_banner.jpg", DesignType.KEYVISUAL),
            ("experience day poster.png", DesignType.KEYVISUAL),
            ("generic_design.pdf", DesignType.GRAPHIC_DESIGN)
        ]
        
        for filename, expected_type in test_cases:
            detected_type = self.analyzer.detect_design_type("", filename)
            # UI/UX ve Architecture için özel kontrol
            if "architecture" in filename.lower():
                self.assertEqual(detected_type, DesignType.ARCHITECTURE)
            elif "ui" in filename.lower() or "interface" in filename.lower():
                self.assertEqual(detected_type, DesignType.UI_UX)
            else:
                self.assertEqual(detected_type, expected_type)
        
        print("ok")
    
    def test_criteria_initialization(self):
        """Kriter başlatma testi"""
        print("Kriter başlatma testi ... ", end="")
        
        for design_type in DesignType:
            criteria = self.analyzer.get_criteria_for_type(design_type)
            self.assertIsInstance(criteria, list)
            self.assertGreater(len(criteria), 0)
            
            # Her kriterin gerekli alanları var mı kontrol et
            for criterion in criteria:
                self.assertTrue(hasattr(criterion, 'name'))
                self.assertTrue(hasattr(criterion, 'weight'))
                self.assertTrue(hasattr(criterion, 'description'))
                self.assertTrue(hasattr(criterion, 'evaluation_prompt'))
        
        print("ok")
    
    def test_prompt_generation(self):
        """Prompt üretme testi"""
        print("Prompt üretme testi ... ", end="")
        
        for design_type in DesignType:
            prompt = self.analyzer.generate_prompt_for_type(design_type, "test_file.png")
            
            # Prompt'un gerekli içerikleri var mı kontrol et
            self.assertIn("analiz edin", prompt)
            self.assertIn("kriterlere göre", prompt)
            self.assertIn("0-100 arası puan", prompt)
            self.assertIn("Türkçe", prompt)
        
        print("ok")
    
    def test_weighted_score_calculation(self):
        """Ağırlıklı puan hesaplama testi"""
        print("Ağırlıklı puan hesaplama testi ... ", end="")
        
        # Test skorları
        test_scores = {
            "tipografi": 85.0,
            "renk_kullanimi": 70.0,
            "kompozisyon": 90.0,
            "teknik_kalite": 75.0,
            "yaraticilik": 80.0
        }
        
        score = self.analyzer.calculate_weighted_score(test_scores, DesignType.GRAPHIC_DESIGN)
        
        # Skor 0-100 arasında olmalı
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        # Ağırlıklı hesaplama doğru mu kontrol et
        expected_score = (85*0.25 + 70*0.20 + 90*0.25 + 75*0.15 + 80*0.15)
        self.assertAlmostEqual(score, expected_score, places=2)
        
        print("ok")
    
    def test_feedback_generation(self):
        """Geri bildirim üretme testi"""
        print("Geri bildirim üretme testi ... ", end="")
        
        test_scores = {
            "tipografi": 45.0,  # Zayıf
            "renk_kullanimi": 65.0,  # Orta
            "kompozisyon": 85.0,  # Güçlü
        }
        
        feedback = self.analyzer.generate_type_specific_feedback(DesignType.GRAPHIC_DESIGN, test_scores)
        
        # Geri bildirim boş olmamalı
        self.assertIsInstance(feedback, str)
        self.assertGreater(len(feedback), 0)
        
        # Zayıf skor için iyileştirme önerisi olmalı
        self.assertIn("iyileştirin", feedback)
        
        print("ok")
    
    def test_all_design_types(self):
        """Tüm tasarım türleri testi"""
        print("Tüm tasarım türleri testi ... ", end="")
        
        for design_type in DesignType:
            # Her tür için kriterler var mı
            criteria = self.analyzer.get_criteria_for_type(design_type)
            self.assertGreater(len(criteria), 0)
            
            # Prompt üretilebiliyor mu
            prompt = self.analyzer.generate_prompt_for_type(design_type, "test.png")
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)
        
        print("ok")

if __name__ == '__main__':
    unittest.main(verbosity=2) 