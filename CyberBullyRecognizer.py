# CyberBullyRecognizer.py
import os, pickle
import jieba
jieba.setLogLevel(0)

class CyberBullyRecognizer:
    """
    网络暴力文本识别分类器：
    - 加载 TF-IDF 特征器与朴素贝叶斯模型（训练后会生成）
    - 预测时先进行结巴分词，再向量化并输出类别
    - 支持 0/1 标签映射为中文描述（0=正常言论，1=网络暴力言论）
    """
    def __init__(self, label_map=None):
        base_dir  = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(base_dir, 'model')
        self.extractor = pickle.load(open(os.path.join(model_dir, 'extractor.pkl'), 'rb'))
        self.estimator = pickle.load(open(os.path.join(model_dir, 'estimator.pkl'), 'rb'))
        self.label_map = label_map or {1: '网络暴力言论', 0: '正常言论'}

    def _clean(self, text: str) -> str:
        return ' '.join(jieba.lcut(text or ''))

    def predict(self, texts):
        texts = [self._clean(t) for t in texts]
        Xv = self.extractor.transform(texts)
        raw = self.estimator.predict(Xv)
        return [self.label_map.get(r, r) for r in raw]
