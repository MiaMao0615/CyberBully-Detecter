# keep_label_text.py
import os, sys
import pandas as pd

in_path  = sys.argv[1] if len(sys.argv) > 1 else "train.csv"
out_path = sys.argv[2] if len(sys.argv) > 2 else "CyberBully.csv"
label_col = "label"
text_col  = "TEXT"

ext = os.path.splitext(in_path)[1].lower()
if ext in (".xlsx", ".xls"):
    df = pd.read_excel(in_path)
else:
    df = pd.read_csv(in_path)

# 只保留 label / TEXT 两列
df = df[[label_col, text_col]].copy()

# 只保留 0/1 两类
df = df[df[label_col].isin([0, 1])].copy()

# 清理空文本
df[text_col] = df[text_col].astype(str).str.strip()
df = df[df[text_col] != ""].copy()

# 打乱
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

df.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"saved: {out_path}, rows={len(df)}")
print("label counts:\n", df[label_col].value_counts())
