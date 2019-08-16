from nltk.tokenize import sent_tokenize


class SentenceSplitter:
    @staticmethod
    def split(self, in_text):
        return sent_tokenize(in_text)
