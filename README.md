CyberBully Detector

A simple Chinese cyberbullying text classifier based on TF–IDF features and a Multinomial Naïve Bayes model. The repo includes scripts for data preparation, model training/evaluation, and a small Tkinter GUI for interactive prediction.

Main files

* DataPrepare.py – Loads a CSV/Excel file, cleans and segments text (jieba), splits into train/test, and caches processed data.
* TrainModel.py – Trains a TF–IDF + Naïve Bayes classifier and saves the vectorizer/model.
* CyberBullyRecognizer.py – Loads the saved model and classifies new input text.
* App.py – Tkinter GUI: paste a sentence, click a button, and see the predicted category.
* TopMenu.py, StatBar.py – Menu bar and status bar for the GUI.

Installation

1. Go to the project directory:
   cd /path/to/CyberBullyDetector

2. (Optional) Create and activate a virtual environment:
   python -m venv .venv
   On Windows: .venv\Scripts\activate
   On macOS / Linux: source .venv/bin/activate

3. Install dependencies:
   pip install jieba pandas scikit-learn tqdm joblib

Basic usage

1. Prepare your dataset
   Create a CSV file (for example, CyberBully.csv) with two columns:

   * TEXT: Chinese sentences
   * label: 0 (normal) or 1 (cyberbullying)

2. Preprocess and split:
   python DataPrepare.py --csv CyberBully.csv --text-col TEXT --label-col label --test-size 0.1

3. Train the model:
   python TrainModel.py

4. (Optional) Evaluate on the test set:
   python TrainModel.py --evaluate

5. Launch the GUI:
   python App.py

Then paste text into the window and click the button to see the prediction.
