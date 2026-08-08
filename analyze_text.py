import os
import pandas as pd

# 1. 建立 4 個班級 (505, 506, 507, 510) 每班 29 人的學生學習反思文本數據
classes = ['505', '506', '507', '510']
sample_reflections = [
    '這篇閱讀文章非常有意思，我覺得做答題目很有挑戰性，收穫很多！',
    '題目太難了，看不太懂文章意思，時間不夠用，有點挫折。',
    '今天完成任務獲得很多代幣，解題過程很順利，很有成就感。',
    '閱讀介面字太小，而且討論區大家都回答很快，壓力好大。',
    '文章內容很實用，對我寫作文有幫助，希望能多做這種題目。',
    '只是為了拿獎勵隨便亂猜，根本不想讀那麼長的文字。',
    '分析圖表滿有趣的，跟同學討論之後終於搞懂正確答案。',
    '系統卡住很不順，題目敘述好複雜，完全不想繼續寫。',
    '提問很引人深思，雖然寫錯幾題，但看解說就懂了。',
    '無聊，不喜歡這個閱讀平台，希望功課可以少一點。',
]

records = []
for c in classes:
  for i in range(1, 30):  # 修改為 1~29，產生每班 29 位學生 (S01~S29)
    student_id = f'{c}_S{i:02d}'
    text = sample_reflections[(i - 1) % len(sample_reflections)]
    records.append({'student_id': student_id, 'class': c, 'reflection': text})

df = pd.DataFrame(records)

# 2. 簡易教育關鍵字特徵與正負向情緒標記
positive_keywords = ['成就感', '收穫', '順利', '有趣', '實用', '幫助', '深思', '挑戰性']
negative_keywords = ['難', '挫折', '壓力', '亂猜', '卡住', '複雜', '無聊', '不喜歡']


def analyze_sentiment(text):
  pos_score = sum(1 for kw in positive_keywords if kw in text)
  neg_score = sum(1 for kw in negative_keywords if kw in text)
  if pos_score > neg_score:
    return '正面 (Positive)'
  elif neg_score > pos_score:
    return '負面 (Negative)'
  else:
    return '中立/平淡 (Neutral)'


df['sentiment'] = df['reflection'].apply(analyze_sentiment)

# 3. 匯出完整 4 個班級 (116 筆) 的文本分析結果
os.makedirs('data', exist_ok=True)
output_path = 'data/text_analysis_result.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print('--- 第 13 週文本分析執行完成 ---')
print(
    f'✅ 已完成 4 個班級 ({", ".join(classes)}) 每班 29 人，共 {len(df)} 筆學生反思分析'
)
print('\n各班級資料筆數：')
print(df['class'].value_counts().sort_index())
print('\n正負向情緒分布統計：')
print(df['sentiment'].value_counts())
print(f'\n✅ 結果已更新並儲存至：{output_path}')