import os
import re
import pandas as pd

def clean_student_data(file_path, output_dir="cleaned_data"):
    # 1. 解析學期與班級（排除學年 114，精準抓取 3 位數班級號碼）
    semester = "114-1" if "114-1" in file_path else "114-2"
    class_nums = [n for n in re.findall(r'\d{3}', file_path) if n != '114']
    class_num = class_nums[0] if class_nums else "000"
    
    df = pd.read_excel(file_path)
    
    # 2. 個資去識別化（座號改為 S01 格式，刪除姓名欄）
    seat_col = [c for c in df.columns if '座號' in c][0]
    df['學生ID'] = df[seat_col].apply(lambda x: f"{class_num}_S{int(x):02d}")
    df_cleaned = df.drop(columns=['姓名', seat_col], errors='ignore')
    
    # 調整欄位順序（將學生ID置於第一欄）
    cols = ['學生ID'] + [c for c in df_cleaned.columns if c != '學生ID']
    df_cleaned = df_cleaned[cols]
    
    # 3. 處理未作答與轉為數值
    metadata_cols = ['學生ID', '平均正確率', '平均作答時間', '完成率', '完成任務數']
    task_cols = [c for c in df_cleaned.columns if c not in metadata_cols]
    
    df_cleaned[task_cols] = df_cleaned[task_cols].replace('未作答', 0)
    for col in task_cols:
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce').fillna(0)
        
    # 4. 新增作答秒數欄位
    def parse_seconds(t):
        if pd.isna(t) or t == '未作答': return 0
        p = str(t).split(':')
        return int(p[0])*3600 + int(p[1])*60 + int(p[2]) if len(p) == 3 else (int(p[0])*60 + int(p[1]) if len(p) == 2 else t)

    df_cleaned['平均作答時間_秒'] = df_cleaned['平均作答時間'].apply(parse_seconds)
    
    # 5. 輸出新 Excel 檔（使用原始檔名加上 cleaned_ 前綴，確保不覆蓋）
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(file_path)
    output_path = os.path.join(output_dir, f"cleaned_{base_name}")
    df_cleaned.to_excel(output_path, index=False)
    print(f"已成功清理並匯出: {output_path}")

if __name__ == "__main__":
    # 自動搜尋資料夾內所有原始 Excel 檔
    raw_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('cleaned_')]
    for file in raw_files:
        clean_student_data(file)