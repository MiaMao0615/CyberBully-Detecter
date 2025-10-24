# DataPrepare.py
import os, pickle, argparse, multiprocessing
from collections import Counter
from joblib import Parallel, delayed
from tqdm import tqdm
import pandas as pd
import jieba
jieba.setLogLevel(0)

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return " ".join(jieba.lcut(text))

def _process_chunk(texts, labels):
    out_x, out_y = [], []
    pbar = tqdm(total=len(labels), desc=f'进程 {os.getpid()}')
    for t, y in zip(texts, labels):
        t2 = clean_text(t)
        pbar.update()
        if t2:
            out_x.append(t2); out_y.append(y)
    pbar.close()
    return out_x, out_y

def process_parallel(texts, labels, workers=None):
    if workers is None:
        workers = max(1, multiprocessing.cpu_count() - 1)
    n = len(labels)
    if n == 0: return [], []
    step = max(1, n // workers)
    ranges = list(range(0, n, step)) + [n]
    tasks = []
    for i in range(len(ranges) - 1):
        s, e = ranges[i], ranges[i+1]
        tasks.append(delayed(_process_chunk)(texts[s:e], labels[s:e]))
    results = Parallel(n_jobs=workers)(tasks)
    X, Y = [], []
    for x, y in results:
        X.extend(x); Y.extend(y)
    return X, Y

def read_data_with_pandas(path, text_col='TEXT', label_col='label',
                          sample_size=None, test_size=0.2, random_state=22):
    if path.lower().endswith(('.xlsx', '.xls')):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    if sample_size and 0 < sample_size < len(df):
        df = df.sample(n=sample_size, random_state=random_state)
    texts  = df[text_col].astype(str).tolist()
    labels = df[label_col].tolist()

    from sklearn.model_selection import train_test_split
    X_tr, X_te, y_tr, y_te = train_test_split(
        texts, labels, test_size=test_size, random_state=random_state, stratify=labels
    )
    print("原始标签分布:", Counter(labels))
    print("训练集标签分布:", Counter(y_tr))
    print("测试集标签分布:", Counter(y_te))

    os.makedirs('temp', exist_ok=True)
    pickle.dump({'text': X_tr, 'label': y_tr}, open('temp/原始训练集.pkl', 'wb'))   # ← 改键名
    pickle.dump({'text': X_te, 'label': y_te}, open('temp/原始测试集.pkl', 'wb'))
    print("已写入 temp/原始训练集.pkl 与 temp/原始测试集.pkl")

def prepare_text_data(workers=None):
    tr = pickle.load(open('temp/原始训练集.pkl', 'rb'))
    te = pickle.load(open('temp/原始测试集.pkl', 'rb'))
    print("开始并行分词（训练集）...")
    Xtr, ytr = process_parallel(tr['text'], tr['label'], workers=workers)   # ← 改键名
    print("开始并行分词（测试集）...")
    Xte, yte = process_parallel(te['text'], te['label'], workers=workers)
    pickle.dump({'text': Xtr, 'label': ytr}, open('temp/处理训练集.pkl', 'wb'))     # ← 改键名
    pickle.dump({'text': Xte, 'label': yte}, open('temp/处理测试集.pkl', 'wb'))
    print("已写入 temp/处理训练集.pkl 与 temp/处理测试集.pkl")

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="数据读取+分词处理（网络暴力识别）")
    ap.add_argument('--csv', required=True, help='训练数据文件路径（CSV 或 Excel）')
    ap.add_argument('--text-col', default='TEXT', help='文本列名')
    ap.add_argument('--label-col', default='label', help='标签列名（0=正常，1=网络暴力）')
    ap.add_argument('--sample-size', type=int, default=None, help='抽样数量，减少训练规模')
    ap.add_argument('--test-size', type=float, default=0.2, help='测试集比例')
    ap.add_argument('--workers', type=int, default=None, help='分词并行进程数')
    args = ap.parse_args()
    read_data_with_pandas(args.csv, text_col=args.text_col, label_col=args.label_col,
                          sample_size=args.sample_size, test_size=args.test_size)
    prepare_text_data(workers=args.workers)
