"""
CreaCritic Web Arayüzü
Seri No: CR-023-v1.1
"""

import os
import json
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64

# Try to import Gemini API
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google.generativeai not available")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Simple configuration
SERIAL_NO = "CR-023-v1.1"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', serial_no=SERIAL_NO)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if not GEMINI_AVAILABLE:
            return jsonify({'error': 'Gemini API kütüphanesi yüklü değil'}), 500
            
        # Get form data
        file = request.files.get('file')
        brief_info = request.form.get('brief_info', '')
        design_statement = request.form.get('design_statement', '')
        gemini_api_key = request.form.get('gemini_api_key', '')
        
        if not file or not gemini_api_key:
            return jsonify({'error': 'Dosya ve API anahtarı gerekli'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Desteklenmeyen dosya formatı'}), 400
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Process image
        image = Image.open(file.stream)
        
        # Create prompt
        prompt = f"""
        CreaCritic tasarım analizi yap:
        
        Brief: {brief_info}
        Tasarımcı Açıklaması: {design_statement}
        
        Bu görseli analiz et ve detaylı eleştiri yap. Eleştiride şunlara odaklan:
        - Okunabilirlik ve netlik
        - Marka kimliği uygunluğu
        - Estetik değerler
        - Teknik kalite
        - Piyasa standartları
        - İyileştirme önerileri
        
        Detaylı ve yapıcı bir eleştiri sun.
        """
        
        # Generate response
        response = model.generate_content([prompt, image])
        
        return render_template('result.html', 
                            analysis=response.text,
                            filename=file.filename,
                            serial_no=SERIAL_NO)
    
    except Exception as e:
        print(f"Error in analyze: {str(e)}")
        return jsonify({'error': f'Hata: {str(e)}'}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'serial_no': SERIAL_NO})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True) 