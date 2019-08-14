from nltk.tokenize import TreebankWordTokenizer

from summerizer.annotations.annotation import Annotation
from summerizer.annotations.annotation_set import AnnotationSet


class Tokenizer:
    def __init__(self):
        self.tokenizer = TreebankWordTokenizer()

    def tokenize(self, text):
        return self.tokenizer.tokenize(text)

    def get_token_spans(self, text):
        return self.tokenizer.span_tokenize(text)

    def tokenize_document(self, out_dir, doc_text):
        token_set = AnnotationSet("tokens")
        tokens = self.tokenize(doc_text)
        spans = self.get_token_spans(doc_text)
        for token, span in zip(tokens, spans):
            token_set.add(Annotation(0, token, "token", span[0], span[1]))
        token_set.write_annotation_file(out_dir)
