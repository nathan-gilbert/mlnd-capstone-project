import os
import string

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from summerizer.annotations.annotation_set import AnnotationSet
from summerizer.utils.scorer import Scorer


class Summerizer:
    def __init__(self):
        self.model = None
        self.training_dir = ""
        self.training_docs = []
        self.test_dir = ""
        self.test_docs = []
        self.scorer = Scorer()

    @staticmethod
    def _stem_tokens(tokens):
        stemmer = nltk.stem.porter.PorterStemmer()
        return [stemmer.stem(item) for item in tokens]

    @staticmethod
    def _normalize(text):
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))

    @staticmethod
    def _remove_stop_words(word_list):
        """
        :param word_list:
        :return: list of words with English stop words removed
        """
        return [word for word in word_list if word not in stopwords.words('english')]

    def train(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def create_summary(self, src_docs):
        raise NotImplementedError

    def score(self, summaries):
        sep = os.path.sep
        for test_doc_path, hypothesis in summaries.items():
            print(f"Scoring document {test_doc_path}")
            keys = AnnotationSet("answer_keys")
            key_file = f"{test_doc_path}{sep}keys{sep}annotations{sep}answer_keys"
            keys.read_annotation_file(key_file)
            hypothesis = '\n'.join(hypothesis)
            reference = keys.get(0).text
            scores = self.scorer.rouge_score(hypothesis, reference)
            print(scores)

    def _cosine_similarity(self, text1, text2):
        vectorizer = TfidfVectorizer(tokenizer=self._normalize_with_stem, stop_words='english')
        tfidf = vectorizer.fit_transform([text1, text2])
        return (tfidf * tfidf.T).A[0, 1]

    def _normalize_with_stem(self, text):
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        return self._stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
