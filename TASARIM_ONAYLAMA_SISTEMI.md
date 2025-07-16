# Tasarım Onaylama Sistemi - Matematiksel Model ve Yapı

**Seri No:** CR-015-v1.0  
**Versiyon:** 1.0.0  
**Tarih:** 2024-12-19

## 📋 Sistem Genel Bakış

CreaCritic projesine entegre edilecek tasarım onaylama sistemi, matematiksel modelleme ile otomatik onay kararları verir. Sistem, Ozan'ın tasarım eleştiri üslubunu tamamlayıcı olarak çalışır.

## 🧮 Matematiksel Model

### 1. Onay Kriterleri

Üç ana kriter tanımlanmıştır:

- **M (Piyasa Standartlarına Uygunluk):** $M \in [0,1]$
- **T (Takım Kalitesi):** $T \in [0,1]$  
- **E (Estetik ve İşlevsellik Dengesi):** $E \in [0,1]$

### 2. Ağırlıklandırma

```python
w_M = 0.4    # Piyasa standartları
w_T = 0.35   # Takım kalitesi  
w_E = 0.25   # Estetik ve işlevsellik
```

### 3. Onay Fonksiyonu

$$
A = w_M \cdot M + w_T \cdot T + w_E \cdot E
$$

**Örnek Hesaplama:**
- $M = 0.8, T = 0.9, E = 0.7$
- $A = 0.4 \times 0.8 + 0.35 \times 0.9 + 0.25 \times 0.7 = 0.815$

### 4. Onay Bölgesi

$$
\mathcal{A} = \{\mathbf{d} \in [0,1]^3 : A(\mathbf{d}) \ge \tau\}
$$

**Onay Eşiği:** $\tau = 0.75$

### 5. Discrete Onay Kararı

$$
\mathrm{approve}(\mathbf{d}) = \begin{cases}
1 & \text{eğer } A(\mathbf{d}) \ge \tau,\\
0 & \text{aksi halde.}
\end{cases}
$$

## 🔄 Genişletilmiş Model (5 Boyutlu)

### Ek Kriterler

- **R (Revizyon Notu):** $R \in [0,1]$ - Brief dışı öneriler
- **C (Canvas/Kompleksite):** $C \in [0,1]$ - Tasarım karmaşıklığı

### Genelleştirilmiş Fonksiyon

$$
A(\mathbf{x}) = \sum_{i=1}^5 w_i x_i, \quad \sum_i w_i = 1
$$

**Ağırlıklar:**
```python
w = (0.3, 0.25, 0.2, 0.15, 0.1)  # M, T, E, R, C
```

## 🌳 Karar Ağacı Yaklaşımı

```python
def approve_design(M, T, E):
    if M < 0.6:
        return "RET"  # Doğrudan ret
    elif T < 0.7:
        return "RET"  # Takım kalitesi yetersiz
    elif E < 0.65:
        return "REVIZYON"  # Revizyon talebi
    else:
        return "ONAY"  # Onayla
```

## 📊 Çizge Tabanlı Model

### Düğüm ve Kenar Yapısı

- **Düğümler ($v_i$):** Tasarım bileşenleri
- **Kenarlar ($w_{ij}$):** Bileşenler arası etkileşim

### Onay Skoru

$$
A = \mathbf{1}^T W \mathbf{x}
$$

Burada $W$ komşuluk matrisi, $\mathbf{x}$ kriter vektörü.

## 🏗️ Sistem Yapısı

### 1. Ana Bileşenler

```
src/
├── approval_system/
│   ├── __init__.py
│   ├── approval_calculator.py      # Onay hesaplayıcı
│   ├── decision_tree.py           # Karar ağacı
│   ├── graph_model.py             # Çizge modeli
│   └── approval_validator.py      # Onay doğrulayıcı
├── mathematical_model.py          # Mevcut model
└── ozan_style_engine.py          # Mevcut motor
```

### 2. Onay Hesaplayıcı Sınıfı

```python
class ApprovalCalculator:
    def __init__(self):
        self.weights = {
            'market_standards': 0.4,
            'team_quality': 0.35,
            'aesthetic_function': 0.25
        }
        self.threshold = 0.75
    
    def calculate_approval_score(self, M, T, E):
        """Onay skorunu hesaplar"""
        return (self.weights['market_standards'] * M +
                self.weights['team_quality'] * T +
                self.weights['aesthetic_function'] * E)
    
    def approve_design(self, M, T, E):
        """Onay kararı verir"""
        score = self.calculate_approval_score(M, T, E)
        return score >= self.threshold
```

### 3. Karar Ağacı Sınıfı

```python
class DecisionTree:
    def __init__(self):
        self.rules = [
            {'condition': lambda M, T, E: M < 0.6, 'action': 'RET'},
            {'condition': lambda M, T, E: T < 0.7, 'action': 'RET'},
            {'condition': lambda M, T, E: E < 0.65, 'action': 'REVIZYON'},
            {'condition': lambda M, T, E: True, 'action': 'ONAY'}
        ]
    
    def evaluate_design(self, M, T, E):
        """Karar ağacı ile değerlendirir"""
        for rule in self.rules:
            if rule['condition'](M, T, E):
                return rule['action']
```

### 4. Çizge Modeli Sınıfı

```python
class GraphModel:
    def __init__(self):
        self.adjacency_matrix = None
        self.criteria_vector = None
    
    def set_adjacency_matrix(self, matrix):
        """Komşuluk matrisini ayarlar"""
        self.adjacency_matrix = matrix
    
    def calculate_graph_score(self, criteria_vector):
        """Çizge tabanlı skor hesaplar"""
        if self.adjacency_matrix is None:
            return 0
        
        return np.dot(np.ones(len(criteria_vector)), 
                     np.dot(self.adjacency_matrix, criteria_vector))
```

## 🔧 Entegrasyon Planı

### 1. Mevcut Sisteme Entegrasyon

```python
# ozan_style_engine.py'ye eklenecek
from .approval_system.approval_calculator import ApprovalCalculator
from .approval_system.decision_tree import DecisionTree

class OzanStyleEngine:
    def __init__(self):
        # Mevcut kodlar...
        self.approval_calculator = ApprovalCalculator()
        self.decision_tree = DecisionTree()
    
    def generate_ozan_critique_with_approval(self, gemini_response, filename):
        """Eleştiri + onay kararı üretir"""
        # Mevcut eleştiri üretimi
        critique = self.generate_ozan_critique(gemini_response, filename)
        
        # Onay skorları hesapla (AI'dan gelen verilerle)
        M, T, E = self._extract_approval_scores(gemini_response)
        
        # Onay kararı
        approval_score = self.approval_calculator.calculate_approval_score(M, T, E)
        approval_decision = self.approval_calculator.approve_design(M, T, E)
        tree_decision = self.decision_tree.evaluate_design(M, T, E)
        
        # Sonuç formatı
        result = f"""
{critique}

📋 ONAY KARARI:
---------------
Onay Skoru: {approval_score:.3f}
Matematiksel Karar: {'ONAY' if approval_decision else 'RET'}
Karar Ağacı Sonucu: {tree_decision}
Kriterler: M={M:.2f}, T={T:.2f}, E={E:.2f}
"""
        return result
```

### 2. Yeni Dosya Yapısı

```
src/
├── approval_system/
│   ├── __init__.py
│   ├── approval_calculator.py
│   ├── decision_tree.py
│   ├── graph_model.py
│   └── approval_validator.py
├── mathematical_model.py
├── ozan_style_engine.py
├── gemini_processor.py
├── dropbox_watcher.py
├── slack_notifier.py
└── error_handler.py
```

## 📈 Performans Metrikleri

### 1. Onay Oranları

- **Yüksek Kalite:** $A \ge 0.85$ → %95 onay
- **Orta Kalite:** $0.75 \le A < 0.85$ → %70 onay  
- **Düşük Kalite:** $A < 0.75$ → %20 onay

### 2. Karar Tutarlılığı

- Matematiksel model ile karar ağacı uyumu: %90+
- Çizge modeli ile skor korelasyonu: 0.85+

## 🧪 Test Senaryoları

### 1. Birim Testleri

```python
def test_approval_calculator():
    calc = ApprovalCalculator()
    
    # Yüksek kalite tasarım
    assert calc.approve_design(0.9, 0.8, 0.85) == True
    
    # Düşük kalite tasarım
    assert calc.approve_design(0.5, 0.6, 0.4) == False

def test_decision_tree():
    tree = DecisionTree()
    
    # Piyasa standartları düşük
    assert tree.evaluate_design(0.5, 0.8, 0.7) == 'RET'
    
    # Takım kalitesi düşük
    assert tree.evaluate_design(0.8, 0.6, 0.7) == 'RET'
    
    # Estetik düşük
    assert tree.evaluate_design(0.8, 0.8, 0.6) == 'REVIZYON'
    
    # Tüm kriterler geçerli
    assert tree.evaluate_design(0.8, 0.8, 0.7) == 'ONAY'
```

### 2. Entegrasyon Testleri

```python
def test_full_approval_system():
    engine = OzanStyleEngine()
    
    # Test Gemini yanıtı
    test_response = '{"critiques": ["Test"], "scores": {"M": 0.8, "T": 0.9, "E": 0.7}}'
    
    result = engine.generate_ozan_critique_with_approval(test_response, "test.pdf")
    
    assert "ONAY KARARI" in result
    assert "Onay Skoru:" in result
```

## 🚀 Uygulama Adımları

### 1. Virtual Environment Kurulumu

```bash
# Virtual environment aktif
venv_creacritic\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt

# Yeni bağımlılıklar ekle
pip install numpy scipy networkx
```

### 2. Onay Sistemi Geliştirme

```bash
# Klasör yapısı oluştur
mkdir src\approval_system

# Dosyaları oluştur
# approval_calculator.py, decision_tree.py, vb.
```

### 3. Test ve Doğrulama

```bash
# Testleri çalıştır
python -m pytest tests/test_approval_system.py -v

# Sistem testi
python main.py --test-approval
```

## 📊 Sonuç Formatı

```
Ozan'ın tasarım_01.pdf için tasarım eleştirisi:

1. Kullan güçlü renk kontrastı
2. Değiştir tipografi hiyerarşisi
3. Artır görsel ağırlık dağılımı
4. Optimize et boşluk yönetimi
5. Test et responsive kırılma noktaları

📋 ONAY KARARI:
---------------
Onay Skoru: 0.815
Matematiksel Karar: ONAY
Karar Ağacı Sonucu: ONAY
Kriterler: M=0.80, T=0.90, E=0.70
```

---

**Seri No:** CR-015-v1.0  
**Versiyon:** 1.0.0  
**Durum:** Planlama Tamamlandı 