"""
Google Gemini Vision+Text API İşleyici
Seri No: CR-022-v1.1
"""

import os
import base64
import io
from typing import List, Optional
from PIL import Image
from config.settings import GEMINI_MODEL, MAX_TOKENS, TEMPERATURE
from .ozan_style_engine import OzanStyleEngine
from .design_type_analyzer import DesignTypeAnalyzer, DesignType
from .mathematical_model import OzanMathematicalModel

# Conditional imports for optional dependencies
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import fitz  # PyMuPDF for PDF processing
except ImportError:
    fitz = None

class GeminiProcessor:
    """
    Google Gemini Vision+Text API ile tasarım dosyalarını işler
    """
    
    def __init__(self):
        self.model = GEMINI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        self.serial_no = "CR-022-v1.1"
        
        # Dependency kontrolü
        if genai is None:
            raise ImportError("google-generativeai kütüphanesi yüklü değil")
        if fitz is None:
            raise ImportError("PyMuPDF kütüphanesi yüklü değil")
        
        # Ozan üslup motoru
        self.ozan_engine = OzanStyleEngine()
        # Tasarım türü analizörü
        self.design_analyzer = DesignTypeAnalyzer()
        # Matematiksel model
        self.math_model = OzanMathematicalModel()
    
    def process_design_file(self, file_path: str, filename: str, api_key: str) -> str:
        """
        Tasarım dosyasını işler ve Ozan üslubunda eleştiri döner
        
        Args:
            file_path: Dosya yolu
            filename: Dosya adı
            
        Returns:
            str: Ozan üslubunda eleştiri
        """
        try:
            # Dosyayı görsel olarak işle
            images = self._extract_images_from_file(file_path)
            
            if not images:
                raise ValueError("Dosyadan görsel çıkarılamadı")
            
            # Gemini'ye tasarım türünü tamamen bırak
            type_verification_prompt = self._create_type_verification_prompt(filename)
            type_response = self._call_gemini_api(images, type_verification_prompt, api_key)
            
            # Tasarım türünü yanıttan çıkar
            verified_type = self._extract_design_type_from_response(type_response, DesignType.GRAPHIC_DESIGN)
            
            # Tasarım türüne özel prompt oluştur
            prompt = self.design_analyzer.generate_prompt_for_type(verified_type, filename)
            
            # Ozan'ın cevap yapısına uygun prompt ekle
            ozan_prompt = self.math_model.generate_ozan_style_prompt()
            enhanced_prompt = f"{prompt}\n\n{ozan_prompt}"
            
            gemini_response = self._call_gemini_api(images, enhanced_prompt, api_key)
            
            # Ozan üslubuna dönüştür
            ozan_critique = self.ozan_engine.generate_ozan_critique(gemini_response, filename)
            
            # Tasarım türüne göre başlık oluştur
            title = self._get_title_for_design_type(verified_type)
            critique_with_type = f"{title}\n\n{ozan_critique}"
            
            return critique_with_type
            
        except Exception as e:
            raise Exception(f"Gemini işleme hatası: {str(e)}")
    
    def process_design_file_with_context(self, file_path: str, filename: str, additional_context: str = "", api_key: str = "") -> str:
        """
        Brief bilgisi ile tasarım dosyasını işler
        
        Args:
            file_path: Dosya yolu
            filename: Dosya adı
            additional_context: Ek bilgiler (brief, tasarım savunması)
            
        Returns:
            str: Ozan üslubunda eleştiri
        """
        try:
            # Dosyayı görsel olarak işle
            images = self._extract_images_from_file(file_path)
            
            if not images:
                raise ValueError("Dosyadan görsel çıkarılamadı")
            
            # Gemini'ye tasarım türünü tamamen bırak
            type_verification_prompt = self._create_type_verification_prompt(filename)
            type_response = self._call_gemini_api(images, type_verification_prompt, api_key)
            
            # Tasarım türünü yanıttan çıkar
            verified_type = self._extract_design_type_from_response(type_response, DesignType.GRAPHIC_DESIGN)
            
            # Tasarım türüne özel prompt oluştur ve brief bilgisini ekle
            base_prompt = self.design_analyzer.generate_prompt_for_type(verified_type, filename)
            
            # Brief ve tasarım savunması analizi
            has_brief = "brief" in additional_context.lower() or "müşteri" in additional_context.lower()
            has_design_statement = "tasarım" in additional_context.lower() and "savunma" in additional_context.lower()
            
            # Ozan'ın cevap yapısına uygun prompt oluştur
            ozan_prompt = self.math_model.generate_ozan_style_prompt(has_brief, has_design_statement)
            
            # Brief bilgisini prompt'a ekle
            if additional_context:
                enhanced_prompt = f"{base_prompt}\n\n{ozan_prompt}\n\nEk Bilgiler:\n{additional_context}\n\nBu bilgileri dikkate alarak analiz yapın."
            else:
                enhanced_prompt = f"{base_prompt}\n\n{ozan_prompt}"
            
            gemini_response = self._call_gemini_api(images, enhanced_prompt, api_key)
            
            # Ozan üslubuna dönüştür
            ozan_critique = self.ozan_engine.generate_ozan_critique(gemini_response, filename)
            
            # Tasarım türü bilgisini ekle
            title = self._get_title_for_design_type(verified_type)
            critique_with_type = f"{title}\n\n{ozan_critique}"
            
            return critique_with_type
            
        except Exception as e:
            raise Exception(f"Gemini işleme hatası: {str(e)}")
    
    def _extract_images_from_file(self, file_path: str) -> List[Image.Image]:
        """
        Dosyadan görselleri çıkarır
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            List[Image.Image]: Görsel listesi
        """
        images = []
        
        # Dosya uzantısını kontrol et
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            images = self._extract_images_from_pdf(file_path)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            image = Image.open(file_path)
            images.append(image)
        else:
            raise ValueError(f"Desteklenmeyen dosya formatı: {file_ext}")
        
        return images
    
    def _extract_images_from_pdf(self, pdf_path: str) -> List[Image.Image]:
        """
        PDF'den görselleri çıkarır
        
        Args:
            pdf_path: PDF dosya yolu
            
        Returns:
            List[Image.Image]: Görsel listesi
        """
        if fitz is None:
            raise ImportError("PyMuPDF kütüphanesi yüklü değil")
            
        images = []
        
        try:
            # PyMuPDF ile PDF'i aç
            pdf_document = fitz.Document(pdf_path)
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Sayfayı görsel olarak render et
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom
                
                # PIL Image'e dönüştür
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                images.append(image)
            
            pdf_document.close()
            
        except Exception as e:
            raise Exception(f"PDF işleme hatası: {str(e)}")
        
        return images
    
    def _call_gemini_api(self, images: List[Image.Image], prompt: str, api_key: str) -> str:
        """
        Gemini API'yi çağırır
        
        Args:
            images: Görsel listesi
            prompt: API prompt'u
            
        Returns:
            str: API yanıtı
        """
        try:
            # API key'i her çağrıda ayarla
            if hasattr(genai, 'configure'):
                genai.configure(api_key=api_key)
            if hasattr(genai, 'GenerativeModel'):
                model_instance = genai.GenerativeModel(self.model)
            else:
                model_instance = None
            
            # Görselleri PIL formatında hazırla
            image_parts = []
            for image in images:
                import io
                img_byte_arr = io.BytesIO()
                
                # RGBA modundaki görselleri RGB'ye dönüştür
                if image.mode == 'RGBA':
                    # Beyaz arka plan oluştur
                    rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                    # RGBA görseli beyaz arka plan üzerine yerleştir
                    rgb_image.paste(image, mask=image.split()[-1])  # Alpha kanalını mask olarak kullan
                    image = rgb_image
                elif image.mode != 'RGB':
                    # Diğer modları RGB'ye dönüştür
                    image = image.convert('RGB')
                
                image.save(img_byte_arr, format='JPEG', quality=95)
                img_byte_arr = img_byte_arr.getvalue()
                image_part = {
                    "mime_type": "image/jpeg",
                    "data": img_byte_arr
                }
                image_parts.append(image_part)
            
            # Ozan'ın cevap yapısına uygun prompt ekle
            ozan_style_instruction = """
Lütfen Ozan Bayar (Beezy Design Studio Creative Director) üslubunda yanıt ver:

ÖNEMLİ KURAL: Brief bilgisi verilmediyse, brief odaklı yorum yapma!

CEVAP YAPISI:
1. TEKNİK DETAY (%35): "Işık–gölge dengesi çok yumuşak; global illumination'ı %15 artırın."
2. ESTETİK-ANALİTİK (%30): "Kompozisyon merkez kaçıyor; öğeyi altın oran noktasına kaydırın."
3. GLOBAL BENCHMARK (%20): "Bu versiyon, global benchmark'ları yüzde 5 geriden geliyor."
4. AKSİYON ODAKLI (%15): "Revizyon talebini ayrıntılı liste olarak paylaşın."

BRIEF VARSA:
- Brief odaklı yorumlar ekle (%40 ağırlık)
- Diğer kategorilerin ağırlığını azalt

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
            
            enhanced_prompt = f"{prompt}\n\n{ozan_style_instruction}"
            
            if hasattr(genai, 'GenerationConfig'):
                generation_config = genai.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            else:
                generation_config = None
            response = model_instance.generate_content(
                [enhanced_prompt] + image_parts,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API hatası: {str(e)}")
    
    def _create_type_verification_prompt(self, filename: str) -> str:
        """
        Tasarım türü doğrulama prompt'u oluşturur
        
        Args:
            filename: Dosya adı
            
        Returns:
            str: Doğrulama prompt'u
        """
        return f"""
Bu dosyayı analiz et: {filename}

Önce 2D mi 3D mi olduğunu belirle, sonra tasarım türünü tespit et.

TASARIM TÜRLERİ:
1. GRAFIK TASARIM: Logo, kartvizit, broşür, poster, banner (düz, 2D kompozisyonlar)
2. MARKALAMA/GIYDIRME: Ürün ambalajı, etiket, giydirme (ürün üzerine uygulanan tasarımlar)
3. 3D RENDER: Ürün görselleştirme, 3D model, render (sadece gerçek 3D modeller)
4. UI/UX: Web arayüzü, mobil uygulama, kullanıcı arayüzü
5. ILLÜSTRASYON: Çizim, illüstrasyon, sanatsal görsel
6. FOTOĞRAF: Fotoğraf, görsel düzenleme
7. MIMARI: Mimari tasarım, iç mekan, dış mekan

Sadece tür adını yaz: GRAFIK TASARIM, MARKALAMA/GIYDIRME, 3D RENDER, UI/UX, ILLÜSTRASYON, FOTOĞRAF, MIMARI
"""
    
    def _extract_design_type_from_response(self, response: str, default_type) -> DesignType:
        """
        Gemini yanıtından tasarım türünü çıkarır
        
        Args:
            response: Gemini yanıtı
            default_type: Varsayılan tür
            
        Returns:
            DesignType: Tespit edilen tasarım türü
        """
        response_lower = response.lower().strip()
        
        # Daha kesin eşleştirme
        if "3d render" in response_lower or "3d model" in response_lower:
            return DesignType.THREE_D_RENDER
        elif "grafik tasarım" in response_lower or "2d" in response_lower:
            return DesignType.GRAPHIC_DESIGN
        elif "markalama" in response_lower or "giydirme" in response_lower:
            return DesignType.BRANDING_APPLICATION
        elif "ui/ux" in response_lower or "arayüz" in response_lower:
            return DesignType.UI_UX
        elif "illüstrasyon" in response_lower or "çizim" in response_lower:
            return DesignType.ILLUSTRATION
        elif "fotoğraf" in response_lower:
            return DesignType.PHOTOGRAPHY
        elif "mimari" in response_lower:
            return DesignType.ARCHITECTURE
        else:
            # Varsayılan olarak grafik tasarım döndür
            return DesignType.GRAPHIC_DESIGN
    
    def _get_title_for_design_type(self, design_type: DesignType) -> str:
        """
        Tasarım türüne göre başlık oluşturur
        
        Args:
            design_type: Tasarım türü
            
        Returns:
            str: Başlık
        """
        titles = {
            DesignType.GRAPHIC_DESIGN: "🎨 Grafik Tasarım Analizi",
            DesignType.BRANDING_APPLICATION: "🏷️ Markalama/Giydirme Analizi",
            DesignType.THREE_D_RENDER: "🎯 3D Render Analizi",
            DesignType.UI_UX: "💻 UI/UX Tasarım Analizi",
            DesignType.ILLUSTRATION: "✏️ İllüstrasyon Analizi",
            DesignType.PHOTOGRAPHY: "📸 Fotoğraf Analizi",
            DesignType.ARCHITECTURE: "🏗️ Mimari Tasarım Analizi"
        }
        
        return titles.get(design_type, "🎨 Tasarım Analizi")
    
    def validate_file(self, file_path: str) -> bool:
        """
        Dosya formatını doğrular
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            bool: Geçerli mi?
        """
        if not os.path.exists(file_path):
            return False
        
        # Desteklenen formatlar
        supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp']
        file_ext = os.path.splitext(file_path)[1].lower()
        
        return file_ext in supported_extensions 