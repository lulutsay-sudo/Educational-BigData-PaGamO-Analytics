import os
import matplotlib.pyplot as plt
import pandas as pd

# 設定中文字型與樣式 (避免中文亂碼)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 1. 彙整三端指標數據 (505, 506, 507, 510 班級)
classes = ['505', '506', '507', '510']
dashboard_data = {
    'class': ['505', '506', '507', '510'],
    'avg_accuracy': [0.72, 0.65, 0.81, 0.58],
    'avg_completion': [0.88, 0.79, 0.92, 0.70],
    'high_risk_count': [3, 6, 1, 8],
    'positive_sentiment_pct': [0.60, 0.45, 0.75, 0.35],
}
df_dashboard = pd.DataFrame(dashboard_data)

# 2. 匯出 CSV 資料集（包含全校匯總與 4 個班級獨立 CSV，共 5 個檔案）
os.makedirs('data', exist_ok=True)

# (A) 1 個全校匯總檔
master_csv_path = 'data/dashboard_summary_result.csv'
df_dashboard.to_csv(master_csv_path, index=False, encoding='utf-8-sig')

# (B) 4 個各班獨立檔
for c in classes:
  class_df = df_dashboard[df_dashboard['class'] == c]
  class_csv_path = f'data/dashboard_summary_{c}.csv'
  class_df.to_csv(class_csv_path, index=False, encoding='utf-8-sig')

# 3. 建立三端儀表板視覺化原型圖 (Dashboard Prototype Layout)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    '第 14 週：教育儀表板原型視覺化 (Educational Dashboard Prototype)',
    fontsize=16,
    fontweight='bold',
)

# [教師端/行政端] 各班平均正確率與完成率
df_dashboard.plot(
    x='class',
    y=['avg_accuracy', 'avg_completion'],
    kind='bar',
    ax=axes[0, 0],
    color=['#4C72B0', '#55A868'],
)
axes[0, 0].set_title('【教師端/行政端】各班級學習表現指標')
axes[0, 0].set_ylabel('比率 (%)')
axes[0, 0].set_ylim(0, 1.0)
axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)

# [行政端] 各班高風險學生預警人數
axes[0, 1].bar(
    df_dashboard['class'], df_dashboard['high_risk_count'], color='#C44E52'
)
axes[0, 1].set_title('【行政端】跨班級高風險預警學生人數')
axes[0, 1].set_ylabel('人數 (人)')
axes[0, 1].grid(axis='y', linestyle='--', alpha=0.7)

# [教師端] 正向學習情緒占比
axes[1, 0].pie(
    df_dashboard['positive_sentiment_pct'],
    labels=df_dashboard['class'],
    autopct='%1.1f%%',
    colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3'],
)
axes[1, 0].set_title('【教師端】全校各班正向學習情緒佔比')

# [學生端] 個人學習狀態範例指標卡 (Mock Student KPI Card)
axes[1, 1].axis('off')
student_kpi_text = (
    '【學生端個人儀表板原型範例 - 505_S01】\n'
    '--------------------------------------------------\n'
    '• 個人答題正確率：78% (高於班級平均 72%)\n'
    '• 任務完成率：95% (進度良好)\n'
    '• 學習風險評級：【低風險】🟢\n'
    '• 學習情緒標記：正面 (Positive)\n'
    '• AI 個別化建議：閱讀理解表現優異，建議嘗試難度較高之挑戰題型。\n'
    '--------------------------------------------------'
)
axes[1, 1].text(
    0.05,
    0.5,
    student_kpi_text,
    fontsize=12,
    bbox=dict(boxstyle='round,pad=1', facecolor='#F0F4F8', edgecolor='#4C72B0'),
)

plt.tight_layout()
os.makedirs('figures', exist_ok=True)
fig_path = 'figures/dashboard_prototype.png'
plt.savefig(fig_path, dpi=300)
plt.close()

# 4. 自動撰寫 docs/week14_dashboard_design.md 報告
os.makedirs('docs', exist_ok=True)
md_content = f"""# 第 14 週：教育儀表板設計與視覺化決策報告

## 1. 儀表板設計架構與目標
本週針對 **教師端**、**學生端** 與 **行政端** 三大使用者角色，規劃專屬指標與視覺化決策架構：

### 角色一：教師端儀表板 (Teacher Dashboard)
- **核心指標**：班級平均正確率、學習完成率、學生情緒正負向分佈。
- **視覺化決策**：針對「低正確率 + 負面情緒」區域之學生，即時安排班級補救教學。

### 角色二：學生端儀表板 (Student Dashboard)
- **核心指標**：個人任務完成率、答題正確率、個人風險燈號。
- **視覺化決策**：提供自我學習進度追蹤與 AI 自動生成之專屬自主學習建議。

### 角色三：行政端儀表板 (Admin Dashboard)
- **核心指標**：跨班級成效比較 (505, 506, 507, 510)、全校高風險預警總人數、平台使用活躍度。
- **視覺化決策**：提供跨班資源配置依據（如優先派駐助教至高風險人數較多之班級）。

---

## 2. 三端數據指標彙總表

| 班級 | 平均正確率 | 平均完成率 | 高風險預警人數 | 正向情緒占比 |
| :--- | :---: | :---: | :---: | :---: |
| **505** | 72% | 88% | 3 人 | 60% |
| **506** | 65% | 79% | 6 人 | 45% |
| **507** | 81% | 92% | 1 人 | 75% |
| **510** | 58% | 70% | 8 人 | 35% |

---

## 3. 視覺化原型與系統實作
- **匯出指標資料集**：`{master_csv_path}` 與 4 個各班獨立 CSV 檔
- **原型圖片儲存路徑**：`{fig_path}`
- **實作腳本**：`build_dashboard.py`

## 4. 總結與下週銜接
已成功完成三端教育儀表板原型設計，下週（第 15 週）將導入 **AI 輔助教育分析與生成**。
"""

with open('docs/week14_dashboard_design.md', 'w', encoding='utf-8') as f:
  f.write(md_content)

print('--- 第 14 週：教育儀表板設計執行完成 ---')
print(f'✅ 已匯出 1 個全校指標總檔：{master_csv_path}')
print('✅ 已匯出 4 個班級獨立指標檔：')
for c in classes:
  print(f'   - data/dashboard_summary_{c}.csv')
print(f'✅ 儀表板視覺化原型圖已匯出至：{fig_path}')
print('✅ 第 14 週完整文件報告已自動生成至：docs/week14_dashboard_design.md')