"""Baseline sentiment scoring, extractive summary and parameterised chatbot."""
import re

POSITIVE = {"good", "helpful", "clean", "excellent", "safe", "improve"}
NEGATIVE = {"bad", "dirty", "smoke", "pollution", "harmful", "unhealthy"}
NEGATORS = {"not", "never", "no"}

def sentiment(text):
    words = re.findall(r"[a-z']+", text.lower())
    score = 0
    for i, word in enumerate(words):
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if i > 0 and words[i-1] in NEGATORS:
            value = -value
        score += value
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"

def extractive_summary(text, k=2):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    if not sentences:
        return []
    stop = {"the", "a", "an", "is", "are", "and", "to", "of", "in", "for", "near"}
    tokens = [[w for w in re.findall(r"[a-z]+", s.lower()) if w not in stop] for s in sentences]
    freq = {}
    for sent in tokens:
        for w in sent:
            freq[w] = freq.get(w, 0) + 1
    scores = [sum(freq.get(w, 0) for w in sent) for sent in tokens]
    chosen = sorted(sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:k])
    return [sentences[i] for i in chosen]

def chatbot_average(conn, station, day):
    return conn.execute(
        "SELECT AVG(pm25) FROM readings WHERE station=? AND day=?", (station, day)
    ).fetchone()[0]

if __name__ == "__main__":
    sample = "The air is dirty near the factory. Residents request cleaner transport and better monitoring."
    print("Sentiment:", sentiment("The air is not clean"))
    print("Summary:", extractive_summary(sample, 2))
