# This module helps us turn chunks of text into numbers (embeddings) that the AI can understand.
# Think of it as translating words into a language the computer is really good at: math!
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

vectorizer = TfidfVectorizer(max_features=384)  # fixed dimensionality

def get_embeddings(text_chunks):
    """
    Converts a list of text chunks into fixed-size numerical vectors (embeddings).
    If there aren't enough features, we pad with zeros so every chunk is the same size.
    """
    vectors = vectorizer.fit_transform(text_chunks).toarray()
    # Padding in case fewer than 384 features are found
    if vectors.shape[1] < 384:
        padded = np.zeros((vectors.shape[0], 384))
        padded[:, :vectors.shape[1]] = vectors
        return padded
    return vectors
