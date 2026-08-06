# 第 4 週產出：Python 資料處理與預處理紀錄

## 一、 資料讀取與清理範疇
* **專題名稱：** 基於 PaGamO 閱讀素養歷程數據之學生學習型態分群與落後風險預警機制建置
* **執行環境：** VS Code (Python 3.14 / Pandas / OpenPyXL)
* **資料來源：** 整合後之跨學年去識別化作答紀錄 Excel 檔案（共 4 份涵蓋完整學年歷程之資料集）。

---

## 二、 資料清理與轉化技術 (Data Cleaning & Pipeline)

1. **自動化路徑與檔案合併 (Automation)：**
   - 使用 `glob` 與 `pandas` 批量讀取 `data/` 目錄下之所有 Excel 檔。
   - 解析檔名動態生成 `學期` 與 `班級` 結構化標籤。

2. **資料型態轉換 (Data Type Conversion)：**
   - 針對原始作答時間字串 `HH:MM:SS` (如 `00:01:47`)，撰寫自訂函數轉換為純數值 `平均作答時間_秒` (如 `107` 秒)，以利後續集群分析與特徵工程之定量計算。

3. **主資料集整合 (Master Dataset Formulation)：**
   - 重構欄位順序，將核心識別變項與歷程指標 (`學生ID`、`班級`、`學期`、`平均正確率`、`平均作答時間_秒`、`完成率`、`完成任務數`) 置於前排。
   - 順利合併並輸出為 `data/master_pagamo_dataset.csv` (UTF-8 with BOM 格式)。

---

## 三、 產出成果驗證
- **執行腳本：** `merge_data.py`
- **產出檔案：** `data/master_pagamo_dataset.csv` (116 筆學生學年歷程紀錄)
- **狀態：** 已順利通過自動化腳本驗證並推送至 GitHub 遠端倉庫。
