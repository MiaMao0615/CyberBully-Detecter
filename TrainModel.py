# TrainModel.py
import os, pickle, argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, classification_report

def _load_stopwords(path):
    if path and os.path.exists(path):
        return [w.strip() for w in open(path, encoding='utf-8', errors='ignore') if w.strip()]
    return None

def train(max_features=50000, alpha=0.01, stopwords_path='data/stopwords.txt', ngram_max=1):
    tr = pickle.load(open('temp/处理训练集.pkl', 'rb'))
    X, y = tr['text'], tr['label']     # ← 改键名
    stopwords = _load_stopwords(stopwords_path)
    vectorizer = TfidfVectorizer(stop_words=stopwords, max_features=max_features,
                                 ngram_range=(1, ngram_max))
    Xv = vectorizer.fit_transform(X)
    print('特征维度:', len(vectorizer.get_feature_names_out()))
    print('示例特征:', vectorizer.get_feature_names_out()[:10])
    clf = MultinomialNB(alpha=alpha).fit(Xv, y)
    pred_tr = clf.predict(Xv)
    print('训练集准确率:', accuracy_score(y, pred_tr))
    print('训练集F1(加权):', f1_score(y, pred_tr, average='weighted'))
    os.makedirs('model', exist_ok=True)
    pickle.dump(vectorizer, open('model/extractor.pkl', 'wb'))
    pickle.dump(clf, open('model/estimator.pkl', 'wb'))
    print("模型已保存到 model/extractor.pkl 与 model/estimator.pkl")

def evaluate():
    vec = pickle.load(open('model/extractor.pkl', 'rb'))
    clf = pickle.load(open('model/estimator.pkl', 'rb'))
    te = pickle.load(open('temp/处理测试集.pkl', 'rb'))
    X, y = te['text'], te['label']     # ← 改键名
    pred = clf.predict(vec.transform(X))
    print('测试集准确率:', accuracy_score(y, pred))
    print('测试集F1(加权):', f1_score(y, pred, average='weighted'))
    print('分类报告:\n', classification_report(y, pred, digits=4))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='网络暴力识别：TF-IDF + 朴素贝叶斯 训练/评估')
    ap.add_argument('--evaluate', action='store_true', help='只做评估')
    ap.add_argument('--max-features', type=int, default=50000)
    ap.add_argument('--alpha', type=float, default=0.01)
    ap.add_argument('--stopwords', type=str, default='data/stopwords.txt')
    ap.add_argument('--ngram-max', type=int, default=1, help='使用 1 或 2：是否启用二元词组')
    args = ap.parse_args()
    if args.evaluate:
        evaluate()
    else:
        train(max_features=args.max_features, alpha=args.alpha,
              stopwords_path=args.stopwords, ngram_max=args.ngram_max)
