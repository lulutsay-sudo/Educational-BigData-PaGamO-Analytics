import os
import glob
import pandas as pd

# 1. 指定資料夾路徑與搜尋 Excel 檔案
data_folder = 'data'
file_pattern = os.path.join(data_folder, 'cleaned_*.xlsx')
file_list = glob.glob(file_pattern)

print(f"找到 {len(file_list)} 個資料檔案，準備開始合併...")

combined_data = []

for file in file_list:
    df = pd.read_excel(file)
    filename = os.path.basename(file)
    
    # 自動辨識學期，只保留學年度 114
    if '114' in filename:
        semester = '114'
    else:
        semester = '未知'
        
    # 自動辨識班級 (501, 504, 505, 506, 507, 510)
    class_code = '未知'
    for c in ['501', '504', '505', '506', '507', '510']:
        if c in filename:
            class_code = c
            break
            
    # 新增識別欄位
    df['學期'] = semester
    df['班級'] = class_code
    
    # 處理時間格式：將「平均作答時間」字串轉換為總秒數
    if '平均作答時間' in df.columns and '平均作答時間_秒' not in df.columns:
        def time_to_seconds(t_str):
            try:
                t_str = str(t_str).strip()
                parts = t_str.split(':')
                if len(parts) == 3:
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                elif len(parts) == 2:
                    return int(parts[0]) * 60 + int(parts[1])
                return float(t_str)
            except:
                return 0
        df['平均作答時間_秒'] = df['平均作答時間'].apply(time_to_seconds)
        
    combined_data.append(df)

# 2. 合併所有班級資料
master_df = pd.concat(combined_data, ignore_index=True)

# 調整欄位順序（把識別指標移到最前面）
first_cols = ['學生ID', '班級', '學期', '平均正確率', '平均作答時間_秒', '完成率', '完成任務數']
other_cols = [c for c in master_df.columns if c not in first_cols and c != '平均作答時間']
final_cols = [c for c in first_cols if c in master_df.columns] + other_cols

master_df = master_df[final_cols]

# 3. 輸出最終 Master 檔案至 data 資料夾
output_path = os.path.join(data_folder, 'master_pagamo_dataset.csv')
master_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"🎉 成功！Master Dataset 已順利產出，共 {len(master_df)} 筆學生紀錄。")
print(f"檔案已儲存於：{output_path}")