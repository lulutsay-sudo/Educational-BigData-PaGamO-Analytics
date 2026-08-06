import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 設定中文字型與負號顯示
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 讀取第 5 週產出的特徵表
df = pd.read_csv('data/initial_feature_table.csv')

# 2. 選取用於分群的核心特徵變項
features = ['平均正確率', '平均作答時間_秒', '完成率', '完成任務數']
X = df[features].fillna(0)

# 3. 特徵標準化 (Z-score Standardization)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. 執行 K-Means 分群 (預設分為 3 群)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# 定義群體標籤對應 (根據數據特徵賦予教育意涵)
cluster_names = {
    0: '群組 0 (學習型態 A)',
    1: '群組 1 (學習型態 B)',
    2: '群組 2 (學習型態 C)'
}
df['學習型態標籤'] = df['Cluster'].map(cluster_names)

# 5. 儲存帶有分群結果的資料表
df.to_csv('data/clustered_students.csv', index=False, encoding='utf-8-sig')

# 6. 繪製並儲存視覺化圖表
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df, 
    x='平均作答時間_秒', 
    y='平均正確率', 
    hue='Cluster', 
    style='Cluster',
    palette='Set1', 
    s=100
)
plt.title('學生學習型態分群散佈圖 (K-Means Clustering)', fontsize=14)
plt.xlabel('平均作答時間 (秒)', fontsize=12)
plt.ylabel('平均正確率', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# 確保 figures 資料夾存在並儲存圖片
import os
os.makedirs('figures', exist_ok=True)
plt.savefig('figures/kmeans_clusters_scatterplot.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ K-Means 模型訓練完成！")
print("📊 分群結果已存至：data/clustered_students.csv")
print("🖼️ 視覺化圖表已存至：figures/kmeans_clusters_scatterplot.png")