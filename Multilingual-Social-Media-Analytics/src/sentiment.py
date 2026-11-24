from preprocessing import normalize_text,tokenize
LEXICON={"positive":{"amazing","superb","great","happy","smooth","fast","good","mast","zabardast","nice","paisa","vasool","शानदार","अच्छा","अच्छी","बेहतरीन","तेज","साफ"},"negative":{"poor","disappointed","drains","drain","heats","hang","freezes","bad","bakwas","खराब","नहीं","गर्म","अटक","बेकार"}}
NEGATIONS={"not","no","nahi","nai","नहीं","मत"}
def lexicon_sentiment(text):
    tokens=tokenize(text); score=0
    for i,t in enumerate(tokens):
        if t in LEXICON["positive"]: score += -1 if any(x in NEGATIONS for x in tokens[max(0,i-2):i]) else 1
        elif t in LEXICON["negative"]: score += 1 if any(x in NEGATIONS for x in tokens[max(0,i-2):i]) else -1
    return "positive" if score>0 else "negative" if score<0 else "neutral"
def theme_tags(text):
    t=normalize_text(text).lower()
    groups={"Battery":["battery","बैटरी","backup","drain"],"Camera":["camera","कैमरा","photo","फोटो"],"Performance":["performance","smooth","fast","तेज","hang","अटक"],"Display":["display","screen","डिस्प्ले","स्क्रीन"],"Price & value":["price","कीमत","पैसा","worth","value"],"Availability & support":["launch","launched","available","service","सर्विस","लॉन्च"]}
    return [k for k,v in groups.items() if any(x in t for x in v)] or ["Other"]
