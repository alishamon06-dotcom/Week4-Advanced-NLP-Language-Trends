from pathlib import Path
import sys
import pandas as pd
from sklearn.metrics import accuracy_score,f1_score,classification_report
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from preprocessing import normalize_text,detect_language
from sentiment import lexicon_sentiment,theme_tags
posts=pd.read_csv(ROOT/"data/social_posts_synthetic.csv")
eval_df=pd.read_csv(ROOT/"data/evaluation_sample_200.csv")
eval_df["language_pred"]=eval_df.text.map(detect_language)
eval_df["sentiment_pred"]=eval_df.text.map(lexicon_sentiment)
print("Language accuracy:",round(accuracy_score(eval_df.language_gold,eval_df.language_pred),3))
print("Sentiment macro F1:",round(f1_score(eval_df.sentiment_gold,eval_df.sentiment_pred,average="macro"),3))
print(classification_report(eval_df.sentiment_gold,eval_df.sentiment_pred,zero_division=0))
posts["themes"]=posts.text.map(lambda x:", ".join(theme_tags(x)))
posts.groupby("language_gold").size().rename("posts").reset_index().to_csv(ROOT/"outputs/language_wise_post_counts.csv",index=False)
rows=[]
for _,r in posts.iterrows():
 for theme in theme_tags(r.text): rows.append({"language":r.language_gold,"sentiment":r.sentiment_gold,"theme":theme})
pd.DataFrame(rows).groupby(["language","sentiment","theme"]).size().rename("posts").reset_index().to_csv(ROOT/"outputs/theme_summary.csv",index=False)
print("Saved language and theme summaries in outputs/.")
