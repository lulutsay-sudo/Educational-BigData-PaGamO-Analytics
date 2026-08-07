import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. 讀取特徵檔
df = pd.read_csv('data/initial_feature_table.csv')

# 2. 自動過濾特徵與數值型目標變數
X = df.drop(columns=['student_id', 'is_risk'], errors='ignore').select_dtypes(include=['number']).fillna(0)
y = df['is_risk'] if 'is_risk' in df.columns else df.iloc[:, -1]

# 3. 切分 80/20 訓練與測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 使用線性迴歸模型
model = LinearRegression()
model.fit(X_train, y_train)

# 5. 印出 Baseline 評估結果
y_pred = model.predict(X_test)
print("=== Baseline 全班混合模型績效結果 ===")
print(f"均方誤差 (MSE): {mean_squared_error(y_test, y_pred):.4f}")
print(f"R2 決定係數: {r2_score(y_test, y_pred):.4f}")

# 6. 匯出預測結果
output_df = df.loc[X_test.index].copy()
output_df['actual'] = y_test
output_df['predicted'] = y_pred
output_df.to_csv('data/baseline_predictions.csv', index=False)
print("詳細預測結果已存至 data/baseline_predictions.csv！")