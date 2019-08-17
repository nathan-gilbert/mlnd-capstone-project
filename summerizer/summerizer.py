import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from summerizer.utils.scorer import Scorer

class Summerizer:
    def __init__(self):
        self.model = None
        self.training_dir = ""
        self.training_docs = []
        self.test_docs = []
        self.scorer = Scorer

    @staticmethod
    def _stem_tokens(tokens):
        stemmer = nltk.stem.porter.PorterStemmer()
        return [stemmer.stem(item) for item in tokens]

    def train(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def create_summary(self):
        raise NotImplementedError

    def _cosine_similarity(self, text1, text2):
        vectorizer = TfidfVectorizer(tokenizer=self._normalize, stop_words='english')
        tfidf = vectorizer.fit_transform([text1, text2])
        return (tfidf * tfidf.T).A[0, 1]

    def _normalize(self, text):
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        return self._stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
