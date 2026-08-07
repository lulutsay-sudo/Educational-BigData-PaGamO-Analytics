import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# 1. 讀取數據 (請依據你的資料路徑調整，如 data/feature_data.csv 或合適的預處理檔)
df = pd.read_csv('data/learning_risk_analysis_result.csv')
# 2. 特徵與標籤分離
if 'is_risk' in df.columns:
    y = df['is_risk'].astype(int)
    X = df.drop(columns=['student_id', 'is_risk'], errors='ignore').select_dtypes(include=['number'])
else:
    # 若無 is_risk 欄位，自動取最後一個數值欄位，高於中位數設為高風險 (1)
    target_col = df.select_dtypes(include=['number']).columns[-1]
    y = (df[target_col] > df[target_col].median()).astype(int)
    X = df.drop(columns=['student_id', target_col], errors='ignore').select_dtypes(include=['number'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. 初始化三種模型
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

results = []

# 4. 批次訓練與評估
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred
    
    results.append({
        'Model': name,
        'Accuracy': round(accuracy_score(y_test, y_pred), 4),
        'Precision': round(precision_score(y_test, y_pred, zero_division=0), 4),
        'Recall': round(recall_score(y_test, y_pred, zero_division=0), 4),
        'F1-Score': round(f1_score(y_test, y_pred, zero_division=0), 4),
        'ROC-AUC': round(roc_auc_score(y_test, y_prob), 4) if len(np.unique(y_test)) > 1 else 'N/A'
    })

# 5. 印出模型評估對照表 (對應第 11 週作業需求)
eval_df = pd.DataFrame(results)
print("=== 第 11 週 模型評估對照表 ===")
print(eval_df.to_string(index=False))

# 6. 提取 Random Forest 特徵重要性 (Feature Importance)
rf_model = models['Random Forest']
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\n=== Top 5 關鍵特徵重要性 (Random Forest) ===")
print(importance_df.head(5).to_string(index=False))

# 7. 匯出預測結果供錯誤分析使用
output_df = X_test.copy()
output_df['actual_is_risk'] = y_test
output_df['rf_pred'] = models['Random Forest'].predict(X_test)
output_df.to_csv('data/advanced_model_predictions.csv', index=False)
print("\n評估結果與預測檔已成功儲存至 data/advanced_model_predictions.csv！")