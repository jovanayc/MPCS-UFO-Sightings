import re
from collections import Counter
import pandas as pd

df = pd.read_csv('ufo-data/combined_deduped.csv',low_memory=False)

# all the text in the comment fields in one big blob
all_text = " ".join(df['summary'].dropna().astype(str))

# get the words out
words = re.findall(r'\b\w+\b', all_text.lower())

# list of filler words (not exhaustive)
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
                'didn', 'get', 'got', 'here', 'his', 'its', 'her', 'hers', 'much', 'their'}

# filter out short words and filler words
filtered = [w for w in words if len(w) > 2 and w not in filler_words]

# count occurrences and only keep those that appear more than x times
ctr = Counter(filtered)
popular = {word for word,count in ctr.items() if count > 200}

# printout sample just to see it
for word, count in ctr.most_common(20):
    print(f"{word}: {count}")

# helper to only extract the keywords you want (popular keywords)
def extract_keywords(text):
    tokens = re.findall(r'\b\w+\b', str(text).lower())
    return [t for t in tokens if t in popular]

# keywords per sighting
df['keywords'] = df['summary'].apply(extract_keywords)

# not actually sure why I sorted these but it made it easier to inspect visually
unique_keywords = sorted({kw for kws in df['keywords'] for kw in kws})
keywords_df = pd.DataFrame({
    'keyword_id': range(len(unique_keywords)),
    'keyword': unique_keywords
})
keywords_df.to_csv('ufo-data/keywords.csv', index=False)

# now, build the sighting-id to keyword-id table for the M:N relationship
mapping = (
    df[['sighting_id','keywords']]
      .explode('keywords')
      .dropna(subset=['keywords'])
      .drop_duplicates()
      .rename(columns={'keywords':'keyword'})
      .merge(keywords_df, left_on='keyword', right_on='keyword')
      [['sighting_id','keyword_id']]
)
mapping.to_csv('ufo-data/sightid_keyid.csv', index=False)

# if we want to save the data with a list of keywords for some reason
# df.to_csv('ufo-data/with_keywords.csv', index=False)

print("Saved")