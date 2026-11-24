from pathlib import Path
import sys
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score
)

# Define ROOT before using it
ROOT = Path(__file__).resolve().parent.parent

# Create outputs folder
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import project modules
sys.path.insert(0, str(Path(__file__).resolve().parent))

from preprocessing import detect_language, normalize_text
from sentiment import lexicon_sentiment, theme_tags

# -----------------------------------
# 1. Load the main dataset
# -----------------------------------

DATA_FILE = ROOT / "data" / "social_posts_synthetic.csv"

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully!")
print("Total posts:", len(df))


# -----------------------------------
# 2. Text preprocessing
# -----------------------------------

df["clean_text"] = df["text"].fillna("").map(normalize_text)

df["language_pred"] = df["text"].fillna("").map(detect_language)

df["sentiment_lexicon"] = (
    df["text"].fillna("").map(lexicon_sentiment)
)

df["themes"] = (
    df["text"].fillna("").map(lambda x: ", ".join(theme_tags(x)))
)

print("Text preprocessing completed!")


# -----------------------------------
# 3. Evaluate predictions
# -----------------------------------

EVAL_FILE = ROOT / "data" / "evaluation_sample_200.csv"

ev = pd.read_csv(EVAL_FILE)

ev["language_pred"] = (
    ev["text"].fillna("").map(detect_language)
)

ev["sentiment_pred"] = (
    ev["text"].fillna("").map(lexicon_sentiment)
)

print("\n========== EVALUATION RESULTS ==========")

print(
    "Language accuracy:",
    round(accuracy_score(ev["language_gold"], ev["language_pred"]), 3)
)

print(
    "Sentiment macro F1:",
    round(
        f1_score(
            ev["sentiment_gold"],
            ev["sentiment_pred"],
            average="macro",
            zero_division=0
        ),
        3
    )
)

print("\nLanguage Classification Report:")
print(
    classification_report(
        ev["language_gold"],
        ev["language_pred"],
        zero_division=0
    )
)

print("\nSentiment Classification Report:")
print(
    classification_report(
        ev["sentiment_gold"],
        ev["sentiment_pred"],
        zero_division=0
    )
)


# -----------------------------------
# 4. Language-wise post counts
# -----------------------------------

language_table = (
    df.groupby("language_gold")
    .agg(posts=("post_id", "count"))
    .reset_index()
)

language_table.to_csv(
    OUTPUT_DIR / "language_wise_post_counts.csv",
    index=False
)


# -----------------------------------
# 5. Theme analysis
# -----------------------------------

theme_rows = []

for _, row in df.iterrows():

    themes = theme_tags(row["text"])

    for theme in themes:

        theme_rows.append({
            "language": row["language_gold"],
            "sentiment": row["sentiment_gold"],
            "theme": theme
        })

theme_df = pd.DataFrame(
    theme_rows,
    columns=["language", "sentiment", "theme"]
)

if not theme_df.empty:

    theme_summary = (
        theme_df.groupby(
            ["language", "sentiment", "theme"]
        )
        .size()
        .reset_index(name="posts")
    )

else:

    theme_summary = pd.DataFrame(
        columns=["language", "sentiment", "theme", "posts"]
    )

theme_summary.to_csv(
    OUTPUT_DIR / "theme_summary.csv",
    index=False
)


# -----------------------------------
# 6. Save annotated dataset
# -----------------------------------

df[
    [
        "post_id",
        "language_gold",
        "sentiment_gold",
        "clean_text",
        "language_pred",
        "sentiment_lexicon",
        "themes"
    ]
].to_csv(
    OUTPUT_DIR / "annotated_posts.csv",
    index=False
)


# -----------------------------------
# 7. Completion message
# -----------------------------------

print("\n===================================")
print("PROJECT ANALYSIS COMPLETED!")
print("===================================")

print("Generated files:")

for file in OUTPUT_DIR.iterdir():
    print("-", file.name)

print("\nAll output files saved in the outputs folder.")
