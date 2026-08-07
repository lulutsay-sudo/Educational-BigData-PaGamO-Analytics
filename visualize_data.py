import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定中文字型與樣式
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font='Microsoft JhengHei')

# 自動定位當前檔案所在目錄，確保 figures 資料夾建在正確位置
base_dir = os.path.dirname(os.path.abspath(__file__))
figures_dir = os.path.join(base_dir, 'figures')
data_path = os.path.join(base_dir, 'data', 'clustered_students.csv')

os.makedirs(figures_dir, exist_ok=True)

# 讀取聚類好的資料
df = pd.read_csv(data_path)

# --- 圖表 1：不同學習型態群體的平均正確率分佈 (箱型圖) ---
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Cluster', y='平均正確率', palette='Set2')
plt.title('圖一：不同學習型態群體的平均正確率分佈', fontsize=14)
plt.xlabel('學生分群 (Cluster)', fontsize=12)
plt.ylabel('平均正確率', fontsize=12)
plt.savefig(os.path.join(figures_dir, 'fig1_accuracy_boxplot.png'), dpi=300, bbox_inches='tight')
plt.close()

# --- 圖表 2：不同群體的平均班級完成率 (條形圖) ---
plt.figure(figsize=(8, 5))
cluster_completion = df.groupby('Cluster')['完成率'].mean().reset_index()
sns.barplot(data=cluster_completion, x='Cluster', y='完成率', palette='Blues_d')
plt.title('圖二：不同學習型態群體的平均任務完成率', fontsize=14)
plt.xlabel('學生分群 (Cluster)', fontsize=12)
plt.ylabel('平均完成率', fontsize=12)
plt.savefig(os.path.join(figures_dir, 'fig2_class_completion_barplot.png'), dpi=300, bbox_inches='tight')
plt.close()

# --- 圖表 3：學習特徵相關性分析 (熱圖 Heatmap) ---
plt.figure(figsize=(8, 6))
numeric_cols = ['平均正確率', '平均作答時間_秒', '完成率', '完成任務數']
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('圖三：學習行為特徵相關係數熱圖', fontsize=14)
plt.savefig(os.path.join(figures_dir, 'fig3_feature_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ 3 張核心視覺化圖表已成功繪製並儲存至 figures/ 資料夾！")