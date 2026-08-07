import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. 讀取特徵檔
df = pd.read_csv('data/initial_feature_table.csv')

# 取得所有不重複的班級列表
classes = df['班級'].unique()
print(f"找到的班級列表：{classes}\n")

all_predictions = []

# 2. 針對每個班級分別進行訓練與評估
for c in classes:
    class_df = df[df['班級'] == c].copy()
    
    # 判斷資料量是否足夠（若人數太少則跳過）
    if len(class_df) < 5:
        print(f"⚠️ 班級 {c} 資料量不足 ({len(class_df)} 筆)，跳過訓練。")
        continue
    
    # 準備該班級的特徵 (X) 與目標 (y)
    X = class_df.drop(columns=['student_id', 'is_risk', '班級'], errors='ignore').select_dtypes(include=['number']).fillna(0)
    y = class_df['is_risk'] if 'is_risk' in class_df.columns else class_df.iloc[:, -1]
    
    # 切分 80/20 訓練與測試集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 訓練該班級專屬模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 評估與預測
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"=== 班級 {c} 獨立模型結果 ===")
    print(f"總筆數: {len(class_df)} | 測試集筆數: {len(X_test)}")
    print(f"均方誤差 (MSE): {mse:.4f}")
    print(f"R2 決定係數: {r2:.4f}\n")
    
    # 儲存該班級預測結果
    output_sub = class_df.loc[X_test.index].copy()
    output_sub['actual'] = y_test
    output_sub['predicted'] = y_pred
    all_predictions.append(output_sub)

# 3. 整合所有班級結果並匯出
if all_predictions:
    final_output = pd.concat(all_predictions, axis=0)
    final_output.to_csv('data/baseline_predictions_by_class.csv', index=False)
    print("各班獨立模型的詳細預測結果已存至 data/baseline_predictions_by_class.csv！")