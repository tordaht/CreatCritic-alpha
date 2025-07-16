"""
CreaCritic Web Arayüzü
Seri No: CR-023-v1.1
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import sys

# Proje kök dizinini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gemini_processor import GeminiProcessor
from src.mathematical_model import OzanMathematicalModel
from config.settings import UPLOAD_FOLDER, MAX_CONTENT_LENGTH

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Global değişkenler
gemini_processor = None
math_model = None
analysis_history = []

def initialize_processors():
    global gemini_processor, math_model
    try:
        gemini_processor = GeminiProcessor()
        math_model = OzanMathematicalModel()
        return True
    except Exception as e:
        print(f"Processor başlatma hatası: {e}")
        return False

# Uygulama başlatılırken processor'ları başlat
with app.app_context():
    if not initialize_processors():
        print("HATA: Processor'lar başlatılamadı!")
        exit(1)

@app.route('/')
def index():
    return render_template('index.html', 
                         serial_no="CR-023-v1.1",
                         version="1.1.1")

@app.route('/analyze', methods=['POST'])
def analyze_design():
    """Tasarım analizi endpoint'i - HTML template döner"""
    try:
        if 'file' not in request.files:
            return render_template('result.html', error="Dosya seçilmedi")
        
        file = request.files['file']
        if file.filename is None or file.filename == '':
            return render_template('result.html', error="Dosya seçilmedi")
        
        filename = secure_filename(file.filename)
        if not filename:
            return render_template('result.html', error="Geçersiz dosya adı")
        
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in allowed_extensions:
            return render_template('result.html', error=f"Desteklenmeyen dosya formatı: {file_ext}")
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        brief_info = request.form.get('brief_info', '').strip()
        design_statement = request.form.get('design_statement', '').strip()
        gemini_api_key = request.form.get('gemini_api_key', '').strip()
        additional_context = ""
        
        if not gemini_api_key:
            return render_template('result.html', error="Gemini API Key gereklidir")
        
        if brief_info:
            additional_context += f"Brief Bilgisi: {brief_info}\n"
        if design_statement:
            additional_context += f"Tasarım Savunması: {design_statement}\n"
        
        if gemini_processor is None or math_model is None:
            return render_template('result.html', error="Sistem başlatılamadı")
        
        if additional_context:
            critique = gemini_processor.process_design_file_with_context(file_path, filename, additional_context, gemini_api_key)
        else:
            critique = gemini_processor.process_design_file(file_path, filename, gemini_api_key)
        
        has_brief = bool(brief_info)
        has_design_statement = bool(design_statement)
        
        category_scores = math_model.analyze_ozan_response_categories(critique, has_brief)
        dynamic_weights = math_model.calculate_dynamic_weights(has_brief, has_design_statement)
        ozan_response_weights = math_model.calculate_ozan_response_weights(has_brief, has_design_statement)
        factors = math_model.analyze_critique_pattern(critique)
        utility_score = math_model.calculate_utility_function(factors, has_brief, has_design_statement)
        
        # Onay kararı hesapla
        approval_decision = "ONAY" if utility_score >= 0.7 else "REVİZYON" if utility_score >= 0.5 else "RET"
        
        # Tasarım türünü çıkar
        design_type = "Grafik Tasarım"  # Varsayılan
        if "🎨 Grafik Tasarım" in critique:
            design_type = "Grafik Tasarım"
        elif "🏷️ Markalama" in critique:
            design_type = "Markalama/Giydirme"
        elif "🎯 3D Render" in critique:
            design_type = "3D Render"
        elif "💻 UI/UX" in critique:
            design_type = "UI/UX Tasarım"
        elif "✏️ İllüstrasyon" in critique:
            design_type = "İllüstrasyon"
        elif "📸 Fotoğraf" in critique:
            design_type = "Fotoğraf"
        elif "🏗️ Mimari" in critique:
            design_type = "Mimari Tasarım"
        
        result = {
            'filename': filename,
            'critique': critique,
            'category_scores': category_scores,
            'dynamic_weights': dynamic_weights,
            'ozan_response_weights': ozan_response_weights,
            'utility_score': utility_score,
            'approval_score': utility_score,
            'approval_decision': approval_decision,
            'has_brief': has_brief,
            'has_design_statement': has_design_statement,
            'design_type': design_type,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'serial_no': "CR-023-v1.1",
            'scores': factors  # Eski template için
        }
        
        analysis_history.append(result)
        
        # Dosyayı silme! Görsel arayüzde gösterilecek.
        # try:
        #     os.remove(file_path)
        # except:
        #     pass
        
        return render_template('result.html', result=result)
        
    except Exception as e:
        return render_template('result.html', error=f"Analiz hatası: {str(e)}")

@app.route('/analyze-json', methods=['POST'])
def analyze_design_json():
    """Tasarım analizi endpoint'i - JSON döner"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Dosya seçilmedi'}), 400
        
        file = request.files['file']
        if file.filename is None or file.filename == '':
            return jsonify({'error': 'Dosya seçilmedi'}), 400
        
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Geçersiz dosya adı'}), 400
        
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'error': f'Desteklenmeyen dosya formatı: {file_ext}'}), 400
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        brief_info = request.form.get('brief_info', '').strip()
        design_statement = request.form.get('design_statement', '').strip()
        gemini_api_key = request.form.get('gemini_api_key', '').strip()
        additional_context = ""
        
        if not gemini_api_key:
            return jsonify({'error': 'Gemini API Key gereklidir'}), 400
        
        if brief_info:
            additional_context += f"Brief Bilgisi: {brief_info}\n"
        if design_statement:
            additional_context += f"Tasarım Savunması: {design_statement}\n"
        
        if gemini_processor is None or math_model is None:
            return jsonify({'error': 'Sistem başlatılamadı'}), 500
        
        if additional_context:
            critique = gemini_processor.process_design_file_with_context(file_path, filename, additional_context, gemini_api_key)
        else:
            critique = gemini_processor.process_design_file(file_path, filename, gemini_api_key)
        
        has_brief = bool(brief_info)
        has_design_statement = bool(design_statement)
        
        category_scores = math_model.analyze_ozan_response_categories(critique, has_brief)
        dynamic_weights = math_model.calculate_dynamic_weights(has_brief, has_design_statement)
        ozan_response_weights = math_model.calculate_ozan_response_weights(has_brief, has_design_statement)
        factors = math_model.analyze_critique_pattern(critique)
        utility_score = math_model.calculate_utility_function(factors, has_brief, has_design_statement)
        
        analysis_result = {
            'filename': filename,
            'critique': critique,
            'category_scores': category_scores,
            'dynamic_weights': dynamic_weights,
            'ozan_response_weights': ozan_response_weights,
            'utility_score': utility_score,
            'has_brief': has_brief,
            'has_design_statement': has_design_statement,
            'timestamp': datetime.now().isoformat(),
            'serial_no': "CR-023-v1.1"
        }
        
        analysis_history.append(analysis_result)
        
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'critique': critique,
            'category_scores': category_scores,
            'dynamic_weights': dynamic_weights,
            'ozan_response_weights': ozan_response_weights,
            'utility_score': utility_score,
            'has_brief': has_brief,
            'has_design_statement': has_design_statement,
            'serial_no': "CR-023-v1.1"
        })
        
    except Exception as e:
        return jsonify({'error': f'Analiz hatası: {str(e)}'}), 500

@app.route('/history')
def history():
    """Geçmiş analizler sayfası"""
    return render_template('history.html', 
                         history=analysis_history,
                         serial_no="CR-023-v1.1")

@app.route('/settings')
def settings():
    """Ayarlar sayfası"""
    return render_template('settings.html', 
                         serial_no="CR-023-v1.1")

@app.route('/api/health')
def health_check():
    """Sistem sağlık kontrolü"""
    try:
        # Processor'ların çalışıp çalışmadığını kontrol et
        if gemini_processor is None or math_model is None:
            return jsonify({'status': 'error', 'message': 'Processor\'lar başlatılamadı'}), 500
        
        return jsonify({
            'status': 'healthy',
            'gemini_processor': True,
            'math_model': True,
            'serial_no': "CR-023-v1.1",
            'version': "1.1.1"
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/analysis_stats')
def analysis_stats():
    """Analiz istatistikleri"""
    try:
        if not analysis_history:
            return jsonify({'message': 'Henüz analiz yapılmamış'})
        
        total_analyses = len(analysis_history)
        avg_utility_score = sum(h['utility_score'] for h in analysis_history) / total_analyses
        
        # En çok kullanılan kategori
        category_counts = {}
        for analysis in analysis_history:
            for category, score in analysis['category_scores'].items():
                if score > 0.5:  # Yüksek skorlu kategoriler
                    category_counts[category] = category_counts.get(category, 0) + 1
        
        most_used_category = max(category_counts.items(), key=lambda x: x[1]) if category_counts else None
        
        return jsonify({
            'total_analyses': total_analyses,
            'avg_utility_score': round(avg_utility_score, 3),
            'most_used_category': most_used_category[0] if most_used_category else None,
            'serial_no': "CR-023-v1.1"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Upload klasörünü oluştur
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print("✅ CreaCritic Web Arayüzü başlatıldı")
    print(f"📊 Seri No: CR-023-v1.1")
    print(f"🌐 http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 