import os
import pandas as pd
import numpy as np

print("=== 開始執行第 8 週：學習成效與學習風險分析 (做法 B：三級分級版) ===")

# 1. 讀取資料
data_path = "data/clustered_students.csv"
if not os.path.exists(data_path):
    print(f"找不到資料檔案：{data_path}，請確認檔名與路徑。")
    exit()

df = pd.read_csv(data_path)

# 自動識別關鍵欄位名稱
cols = df.columns.tolist()
class_col = next((c for c in ["班級", "Class", "class"] if c in cols), "班級")
student_col = next((c for c in ["學生姓名", "帳號", "Student_ID", "姓名", "student_id"] if c in cols), cols[0])
accuracy_col = next((c for c in ["平均正確率", "正確率", "accuracy"] if c in cols), "平均正確率")
completion_col = next((c for c in ["完成率", "completion_rate"] if c in cols), "完成率")
time_col = next((c for c in ["平均作答時間_秒", "作答時間", "duration"] if c in cols), "平均作答時間_秒")

# 2. 定義做法 B 的三級風險標籤 (目標變數)
conditions = [
    (df[accuracy_col] < 0.35) | (df[completion_col] < 0.5),                                  # 高風險：正確率 < 35% 或 完成率 < 50%
    (df[accuracy_col] >= 0.35) & (df[accuracy_col] < 0.50) & (df[completion_col] >= 0.5),   # 中風險：35% <= 正確率 < 50%
    (df[accuracy_col] >= 0.50) & (df[completion_col] >= 0.5)                                 # 低風險：正確率 >= 50%
]
choices = ["高風險(需優先抽問)", "中風險(觀望提醒)", "低風險(學習穩定)"]

df["早期預警風險"] = np.select(conditions, choices, default="中風險(觀望提醒)")

print("\n--------------------------------------------------")
print("【軌道一：全年級跨班整體學習成效與風險統計】")
print("--------------------------------------------------")

overall_summary = df.groupby(class_col).agg(
    學生人數=(student_col, "count"),
    平均正確率=(accuracy_col, "mean"),
    平均完成率=(completion_col, "mean"),
    高風險人數=("早期預警風險", lambda x: (x == "高風險(需優先抽問)").sum()),
    中風險人數=("早期預警風險", lambda x: (x == "中風險(觀望提醒)").sum()),
    低風險人數=("早期預警風險", lambda x: (x == "低風險(學習穩定)").sum())
).reset_index()

overall_summary["高風險比例(%)"] = (overall_summary["高風險人數"] / overall_summary["學生人數"] * 100).round(1)
overall_summary["平均正確率"] = (overall_summary["平均正確率"] * 100).round(1)
overall_summary["平均完成率"] = (overall_summary["平均完成率"] * 100).round(1)

print(overall_summary.to_string(index=False))

print("\n--------------------------------------------------")
print("【軌道二：各班導師專用微觀診斷與早期預警清單】")
print("--------------------------------------------------")

for c in sorted(df[class_col].unique()):
    class_df = df[df[class_col] == c]
    
    # 計算參與度與成效的相關性
    corr = class_df[completion_col].corr(class_df[accuracy_col])
    
    print(f"\n▶ [{c} 班診斷報告]")
    print(f"  • 班級人數：{len(class_df)} 人")
    print(f"  • 參與度與成效相關係數：{corr:.2f}")
    
    risk_students = class_df[class_df["早期預警風險"] == "高風險(需優先抽問)"]
    print(f"  • 需優先關注之高風險學生人數：{len(risk_students)} 人")
    
    if len(risk_students) > 0:
        print("  • 核心高風險學生名單與行為特徵：")
        for _, row in risk_students.iterrows():
            print(f"    - 學生: {row[student_col]} | 正確率: {row[accuracy_col]*100:.1f}% | 完成率: {row[completion_col]*100:.1f}% | 平均作答時間: {row[time_col]:.1f}秒")
    else:
        print("  • 該班學生整體表現穩定，無高風險預警學生。")

# 3. 覆蓋更新 csv 檔案
output_path = "data/learning_risk_analysis_result.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"\n分析完成！更新後的 CSV 數據已覆蓋儲存至：{output_path}")