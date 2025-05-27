import pandas as pd
import re
from collections import Counter

df = pd.read_csv('ufo-data/wiki_sightings.csv', dtype=str, low_memory=False)

# normalize col names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# join all description text
all_text = " ".join(df['description'].dropna().astype(str))

# get the words out
words = re.findall(r'\b\w+\b', all_text.lower())

filler_words = {'000', '100', '200', '39s', '39ve', 'about', 'across', 'after', 'all', 'las',
                '2010', '2011', '2012', '2013', '300', '4th', '500','you', 'yes', 'within',
                'always', 'amp', 'and', 'any', 'appear', 'appeared', 'are', 'who', 'where', '39t',
                'around', 'ave', 'away', 'back', 'before', 'but', 'can', 'wasn', 'until', 'non',
                'couldn', 'each', 'for', 'from', 'going', 'had', 'have', 'how', 'took', 'these',
                'into', 'just', 'like', 'looked', 'moved', 'near', 'new', 'not', 'thought',
                'note', 'noticed', 'observed', 'off', 'one', 'onto', 'our', 'could', 'said',
                'out', 'over', 'possibly', 'quot',' just', 'roughly', 'same', 'san', 'saw', 
                'say', 'see', 'seem', 'seeming', 'seemingly', 'seen', 'slight', 'taking', 'also',
                'than', 'that', 'the', 'then', 'there', 'they', 'this', 'though', 'them', 'ago',
                'through', 'too', 'two', 'very', 'was', 'way', 'evenly', 'almost', 'would',
                'went', 'were', 'what', 'when', 'which', 'while', 'with', 'except', 'did', 
                'didn', 'get', 'got', 'here', 'his', 'its', 'her', 'hers', 'much', 'their', 'later'}

# filter out short words and filler words
filtered = [w for w in words if len(w) > 2 and w not in filler_words]

# count occurrences and only keep those that appear more than x times
ctr = Counter(filtered)
popular = {word for word,count in ctr.items() if count > 3} # not that many items in this table

# printout sample just to see it
for word, count in ctr.most_common(200):
    print(f"{word}: {count}")

def extract_keywords(text):
    tokens = re.findall(r'\b\w+\b', str(text).lower())
    return [t for t in tokens if t in popular]

# extract keywords from each event
df['keywords'] = df['description'].apply(extract_keywords)

# make keyword list / save it
unique_keywords = sorted({kw for kws in df['keywords'] for kw in kws})
keywords_df = pd.DataFrame({
    'KeywordID': range(len(unique_keywords)),
    'Keyword': unique_keywords
})
keywords_df.to_csv('ufo-data/event_keywords.csv', index=False)

#map events to keywords
mapping = (
    df[['eventid','keywords']]
      .explode('keywords')
      .dropna(subset=['keywords'])
      .drop_duplicates()
      .rename(columns={'keywords':'keyword'})
)

# cast as strings
mapping['keyword']     = mapping['keyword'].astype(str)
keywords_df['Keyword'] = keywords_df['Keyword'].astype(str)

# merge cols
mapping = (
    mapping
      .merge(keywords_df, left_on='keyword', right_on='Keyword')
      [['eventid','KeywordID']]
)

mapping.to_csv('ufo-data/event_keyword_mapping.csv', index=False)

print("Saved:")
print("event_keywords.csv")
print("event_keyword_mapping.csv")