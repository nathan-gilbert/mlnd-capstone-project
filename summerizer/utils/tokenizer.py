import os

from nltk.tokenize import TreebankWordTokenizer as twt


class Tokenizer:
    def __init__(self):
        self.tokenizer = twt()

    def tokenize(self, text):
        return self.tokenizer.tokenize(text)

    def get_token_spans(self, text):
        return self.tokenizer.span_tokenize(text)

    def tokenize_document(self, out_dir, doc_text):
        tokens = self.tokenize(doc_text)
        spans = self.get_token_spans(doc_text)

        with open(out_dir + os.path.sep + "tokens", 'w') as tokens_file:
            for token, span in zip(tokens, spans):
                tokens_file.write(f"{token}\t{span}\n")
