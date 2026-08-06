import pandas as pd
import numpy as np

# 1. 讀取 Master Dataset
df = pd.read_csv('data/master_pagamo_dataset.csv')

# 2. 進行特徵工程 (Feature Engineering)
# 計算總作答秒數與估算投入度
df['總作答時間_秒'] = df['平均作答時間_秒'] * df['完成任務數']
df['每任務平均投入效率'] = np.where(df['完成任務數'] > 0, df['平均正確率'] / (df['平均作答時間_秒'] + 1), 0)

# 3. 定義特徵變項群組
core_features = [
    '學生ID', '班級', '學期', 
    '平均正確率', '平均作答時間_秒', '完成率', '完成任務數',
    '總作答時間_秒', '每任務平均投入效率'
]

# 4. 產出初步特徵表
feature_df = df[core_features]
feature_df.to_csv('data/initial_feature_table.csv', index=False, encoding='utf-8-sig')

print("✅ 初步特徵表已成功產出：data/initial_feature_table.csv")
print(f"📊 特徵表維度：{feature_df.shape[0]} 列 x {feature_df.shape[1]} 欄")