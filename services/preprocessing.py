import re
import nltk

nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words("english"))


def clean_text(text):
    
    "Clean the Text"

    # Convert to lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove stopwords
    words = text.split()

    words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return " ".join(words)