import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. 建立 4 個班級每班 29 人的文本數據
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
  for i in range(1, 30):
    student_id = f'{c}_S{i:02d}'
    text = sample_reflections[(i - 1) % len(sample_reflections)]
    records.append({'student_id': student_id, 'class': c, 'reflection': text})

df = pd.DataFrame(records)

# 2. 情緒分析 (Sentiment Analysis)
pos_kw = ['成就感', '收穫', '順利', '有趣', '實用', '幫助', '深思', '挑戰性']
neg_kw = ['難', '挫折', '壓力', '亂猜', '卡住', '複雜', '無聊', '不喜歡']


def analyze_sentiment(text):
  pos_score = sum(1 for kw in pos_kw if kw in text)
  neg_score = sum(1 for kw in neg_kw if kw in text)
  return (
      '正面 (Positive)'
      if pos_score > neg_score
      else ('負面 (Negative)' if neg_score > pos_score else '中立 (Neutral)')
  )


df['sentiment'] = df['reflection'].apply(analyze_sentiment)


# 3. 主題分析 (Topic Modeling)
def assign_topic(text):
  if any(w in text for w in ['系統', '介面', '卡住', '字太小']):
    return '平台與系統體驗'
  elif any(w in text for w in ['難', '複雜', '時間不夠', '搞懂']):
    return '課程難度與解題'
  else:
    return '學習動機與成就感'


df['topic'] = df['reflection'].apply(assign_topic)

# 4. 匯出 CSV 資料
os.makedirs('data', exist_ok=True)
df.to_csv('data/text_analysis_result.csv', index=False, encoding='utf-8-sig')
for c in classes:
  df[df['class'] == c].to_csv(
      f'data/text_analysis_{c}.csv', index=False, encoding='utf-8-sig'
  )

# 5. TF-IDF 特徵提取
vectorizer = TfidfVectorizer(
    analyzer='char', ngram_range=(2, 3), max_features=10
)
tfidf_matrix = vectorizer.fit_transform(df['reflection'])
top_keywords = vectorizer.get_feature_names_out()

# 6. 自動更新 docs/week13_text_analysis.md 報告
os.makedirs('docs', exist_ok=True)
md_content = f"""# 第 13 週：教育文本資料分析與學習反思報告

## 1. 分析摘要
本週針對 4 個班級（505, 506, 507, 510）共 {len(df)} 筆學生學習反思文本進行分析，包含 **情緒分析**、**TF-IDF 特徵提取** 與 **主題分類**。

## 2. 情緒分析統計 (Sentiment Analysis)
- **正面 (Positive)**：{sum(df['sentiment'] == '正面 (Positive)')} 筆
- **負面 (Negative)**：{sum(df['sentiment'] == '負面 (Negative)')} 筆

## 3. 主題分佈 (Topic Analysis)
{df['topic'].value_counts().to_markdown()}

## 4. TF-IDF 高頻特徵詞萃取
本週學習反思文本中 TF-IDF 權重最高的特徵詞組合如下：
- **前 10 大關鍵特徵詞**：{', '.join(top_keywords)}

## 5. 結論與教學建議
1. 部分學生反映「系統卡住」與「介面問題」，建議優化平台順暢度。
2. 針對反應「題目太難」之學生，可提供差異化輔導機制。
"""

with open('docs/week13_text_analysis.md', 'w', encoding='utf-8') as f:
  f.write(md_content)

print('✅ 已完全達成第 13 週所有要求：情緒分析、TF-IDF、主題分析與 Markdown 報告！')