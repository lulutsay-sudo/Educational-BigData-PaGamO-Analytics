import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# 1. 讀取數據 (讀取 1~9 週產出的風險分析檔)
df = pd.read_csv('data/learning_risk_analysis_result.csv')

# 2. 特徵與標籤分離 (對齊 1~9 週早期預警風險標準)
if '早期預警風險' in df.columns:
    # 將「高風險(需優先抽問)」設為 1 (高風險)，其他(中/低風險)設為 0
    y = (df['早期預警風險'] == '高風險(需優先抽問)').astype(int)
    X = df.drop(columns=['學生ID', '學期', '早期預警風險', 'is_risk', 'student_id'], errors='ignore').select_dtypes(include=['number'])
elif 'is_risk' in df.columns:
    y = df['is_risk'].astype(int)
    X = df.drop(columns=['學生ID', '學期', '早期預警風險', 'is_risk', 'student_id'], errors='ignore').select_dtypes(include=['number'])
else:
    raise ValueError("❌ 找不到『早期預警風險』或『is_risk』欄位，請先執行 analyze_learning_risk.py 產出風險標籤！")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. 初始化三種模型
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

results = []

# 4. 訓練與評估模型
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_proba)
    
    results.append({
        'Model': name,
        'Accuracy': round(acc, 4),
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'F1 Score': round(f1, 4),
        'AUC': round(auc, 4)
    })

# 5. 輸出模型比較結果
results_df = pd.DataFrame(results)
print("\n=== 模型訓練與對齊評估結果 ===")
print(results_df.to_string(index=False))