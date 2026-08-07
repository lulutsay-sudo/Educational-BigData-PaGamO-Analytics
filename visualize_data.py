import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

print("開始執行繪圖程式...")

# 1. 設定中文字型與基礎樣式
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]  # Windows 環境
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", font="Microsoft JhengHei")

# 2. 建立圖表儲存目錄
os.makedirs("figures/class_reports", exist_ok=True)

# 3. 讀取完成分群的學生資料檔
df = pd.read_csv("data/clustered_students.csv")

# 自動找尋對應的欄位名稱（避免欄位名不合報錯）
cols = df.columns.tolist()

# 找聚類/分群欄位
cluster_col = next(
    (c for c in ["聚類標籤", "Cluster", "cluster", "群組", "聚類"] if c in cols), None
)
# 找預警欄位
risk_col = next(
    (
        c
        for c in ["落後預警標籤", "Risk_Level", "risk", "預警標籤", "預警"]
        if c in cols
    ),
    None,
)
# 找班級欄位
class_col = next(
    (c for c in ["班級", "Class", "class", "班級名稱"] if c in cols), None
)

print(
    f"偵測到的欄位 -> 班級: {class_col}, 分群: {cluster_col}, 預警: {risk_col}"
)

# =========================================================
# 方向一：全年級整體分析（4 個班級跨班比較）
# =========================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(
    data=df, x=class_col, y="平均正確率", palette="Set3", ax=axes[0]
)
axes[0].set_title("各班平均正確率分佈比較")
axes[0].set_ylim(0, 1)

sns.boxplot(data=df, x=class_col, y="完成率", palette="Set3", ax=axes[1])
axes[1].set_title("各班任務完成率分佈比較")
axes[1].set_ylim(0, 1)

plt.tight_layout()
plt.savefig("figures/fig1_overall_class_comparison.png", dpi=300)
plt.close()

# 1-2. 各班級在 K-means 學習型態（聚類）的人數分佈
plt.figure(figsize=(10, 6))
sns.countplot(
    data=df, x=class_col, hue=cluster_col if cluster_col else None, palette="viridis"
)
plt.title("各班級學生學習型態人數結構")
plt.xlabel("班級")
plt.ylabel("學生人數")
if cluster_col:
    plt.legend(title="學習型態", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig("figures/fig2_overall_cluster_by_class.png", dpi=300)
plt.close()


# =========================================================
# 方向二：單一班級微觀分析（自動產出 4 個班級獨立診斷圖）
# =========================================================

classes = df[class_col].unique()

for c in sorted(classes):
    class_df = df[df[class_col] == c]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # 左圖：班級學生學習行為散佈圖
    sns.scatterplot(
        data=class_df,
        x="平均作答時間_秒",
        y="平均正確率",
        hue=cluster_col if cluster_col else None,
        style=risk_col if risk_col else None,
        s=120,
        palette="tab10",
        ax=axes[0],
    )
    axes[0].set_title(f"{c} 班學生學習行為與落後預警散佈圖")
    axes[0].set_xlabel("平均作答時間（秒）")
    axes[0].set_ylabel("平均正確率")
    axes[0].axhline(
        y=0.6, color="r", linestyle="--", alpha=0.5, label="預警線 (60%)"
    )

    # 右圖：該班級核心特徵相關係數熱圖
    feature_cols = [
        col
        for col in ["平均正確率", "完成率", "平均作答時間_秒", "完成任務數"]
        if col in class_df.columns
    ]
    corr = class_df[feature_cols].corr()
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="coolwarm", ax=axes[1], cbar=False
    )
    axes[1].set_title(f"{c} 班學習特徵相關性")

    plt.suptitle(f"— {c} 班導師專用學習行為診斷圖表 —", fontsize=16, y=1.02)
    plt.tight_layout()

    plt.savefig(f"figures/class_reports/class_{c}_report.png", dpi=300)
    plt.close()

print("全體比較與各班級獨立圖表已全部繪製完成！")