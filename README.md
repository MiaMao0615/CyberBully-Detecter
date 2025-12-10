# CyberBully Detector

A simple tool to detect cyberbullying in Chinese text using TF-IDF and a Naive Bayes classifier. Includes scripts for processing data, training a model, and a GUI for testing.

## 📁 Main Files

| File | Purpose |
|------|---------|
| `DataPrepare.py` | Prepares your data: loads, cleans, splits it |
| `TrainModel.py` | Trains and saves the classification model |
| `CyberBullyRecognizer.py` | Loads the model and predicts on new text |
| `App.py` | Simple GUI to test the model |
| `TopMenu.py`, `StatBar.py` | GUI menu and status bar |

## ⚙️ Setup

1. Go to the project folder:
```bash
cd /path/to/CyberBullyDetector
```

2. (Optional) Create a virtual environment:
```bash
python -m venv .venv
```
- Windows: `.venv\Scripts\activate`
- Mac/Linux: `source .venv/bin/activate`

3. Install requirements:
```bash
pip install jieba pandas scikit-learn tqdm joblib
```

## 🚀 How to Use

### 1. Prepare Your Data
Create a CSV file (e.g., `data.csv`) with two columns:
- `TEXT` – Chinese sentences
- `label` – `0` for normal, `1` for cyberbullying

### 2. Prepare & Split Data
```bash
python DataPrepare.py --csv data.csv --text-col TEXT --label-col label --test-size 0.1
```

### 3. Train the Model
```bash
python TrainModel.py
```
To also test the model:
```bash
python TrainModel.py --evaluate
```

### 4. Launch the GUI
```bash
python App.py
```
Paste text and click the button to see the prediction.

---

**Note**: This is a basic classifier for demonstration. For real-world use, consider more advanced models and larger datasets.
