import os

from bs4 import BeautifulSoup

from summerizer.utils.tokenizer import Tokenizer


class Preprocessor:
    def __init__(self):
        self.__document_list = []

    def run(self):
        tok = Tokenizer()

        for doc in self.__document_list:
            doc_text = self.get_document_text(doc)
            out_dir = doc + os.path.sep + "annotations"
            token_file = out_dir + os.path.sep + "tokens"
            tok.tokenize_document(token_file, doc_text)

    @staticmethod
    def get_document_text(doc):
        with open(doc, 'r') as in_file:
            soup = BeautifulSoup(in_file, 'lxml')
            text = soup.find("TEXT")
            return text


if __name__ == "__main__":
    pre = Preprocessor()
    pre.run()
