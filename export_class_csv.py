import os
import pandas as pd

# 1. 讀取分群結果資料集
input_file = 'data/clustered_students.csv'

if not os.path.exists(input_file):
  print(f'錯誤：找不到檔案 {input_file}，請先執行 python train_kmeans.py')
else:
  df = pd.read_csv(input_file)

  # 2. 辨識班級欄位或從學生 ID 提取班級 (例如從 "505_S01" 提取 "505")
  if '班級' in df.columns:
    df['class_tag'] = df['班級'].astype(str)
  elif 'class' in df.columns:
    df['class_tag'] = df['class'].astype(str)
  else:
    # 預設以第一個欄位（學生 ID）抓取前三位班級數字
    first_col = df.columns[0]
    df['class_tag'] = df[first_col].astype(str).str.extract(r'(\d{3})')[0]

  # 3. 按班級拆分並匯出成 CSV (使用 utf-8-sig 確保 Excel 打開中文不卡亂碼)
  classes = sorted(df['class_tag'].dropna().unique())

  print('--- 開始匯出各班級 CSV 名單 ---')
  for c in classes:
    class_df = df[df['class_tag'] == c].drop(columns=['class_tag'])
    output_path = f'data/clustered_students_{c}.csv'
    class_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'✅ 已匯出 {c} 班名單（共 {len(class_df)} 人）：{output_path}')

  print('--- 匯出完成！---')