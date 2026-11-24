# Multilingual Social Media Analytics

A reproducible NLP prototype exploring how people discuss a fictional smartphone launch in English, Devanagari Hindi and Romanised Hinglish. The workflow focuses on everyday social-post details such as mixed scripts, spelling variation, emojis and hashtags.

## Included
- 3,000 deterministic synthetic posts and a 200-row evaluation starter sample
- Unicode NFKC normalisation, emoji mapping, hashtag retention and Latin/Devanagari tokenisation
- Script- and vocabulary-based language baseline
- Custom Hinglish-aware lexicon sentiment baseline
- Theme tags for battery, camera, performance, display, price/value and support

## Dataset note
All posts are **synthetic**. Labels are generated from templates, not manually annotated. Review and correct the 200-row evaluation file before presenting results as human-labelled model performance. Template-based scores are only a pipeline check and must not be described as real-world accuracy.

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/run_analysis.py
```

## Reproducibility
Fixed seed: 42. The dataset and evaluation sample are deterministic.

## Limitations
Short posts, sarcasm, regional slang and transliteration make language detection difficult. Emoji meanings depend on context. The balanced synthetic dataset does not represent Indian social media. Never use these labels to make decisions about individual users.

## Next steps
Human-review the evaluation sample, compare two independent annotators, then evaluate a multilingual transformer (such as XLM-R) on the same fixed split. Report macro F1 and per-language error rates.
