import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 確保 figures 資料夾存在
os.makedirs('figures', exist_ok=True)

# 2. 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font='Microsoft JhengHei')

# 3. 自動尋找 CSV 檔案位置（優先找 data/ 資料夾，找不到就找當前目錄）
csv_path = 'data/learning_risk_analysis_result.csv'
if not os.path.exists(csv_path):
    csv_path = 'learning_risk_analysis_result.csv'

if not os.path.exists(csv_path):
    print("【提示】找不到 learning_risk_analysis_result.csv！請先執行 analyze_learning_risk.py 產生該檔案。")
else:
    df = pd.read_csv(csv_path)

    # ==========================================
    # 繪製圖表：各班級三級學習風險學生比例分佈圖 (100% 堆疊長條圖)
    # ==========================================
    df_risk_counts = pd.crosstab(df['班級'], df['早期預警風險'], normalize='index') * 100
    cols_order = ['低風險(學習穩定)', '中風險(觀望提醒)', '高風險(需優先抽問)']
    df_risk_counts = df_risk_counts[cols_order]

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ['#2ECC71', '#F39C12', '#E74C3C']
    df_risk_counts.plot(kind='bar', stacked=True, color=colors, ax=ax, width=0.55)

    plt.title('各班級三級學習風險學生比例分佈圖 (100% 堆疊長條圖)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('班級', fontsize=12)
    plt.ylabel('百分比 (%)', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='風險分級', bbox_to_anchor=(1.05, 1), loc='upper left')

    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        if height > 5:
            x, y = p.get_xy() 
            ax.text(x + width/2, y + height/2, f'{height:.1f}%', ha='center', va='center', color='white', fontweight='bold', fontsize=10)

    plt.tight_layout()

    # 儲存圖片
    output_img = 'figures/chart2_risk_distribution.png'
    plt.savefig(output_img, dpi=300)
    plt.close()

    print(f"成功了！圖片已成功產出並存入 {output_img}！")