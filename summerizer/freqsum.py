import os

from data_utils.data_organizer import get_subfolders
from summerizer.annotations.document import Document
from summerizer.annotations.document_set import DocumentSet
from summerizer.summerizer import Summerizer


class FreqSum(Summerizer):
    def __init__(self):
        super().__init__()
        # List of sentences containing the summary
        self.__summary = []

    def train(self):
        all_training_doc_sets = []
        for doc in self.training_docs:
            # contains one set of documents from DUC
            doc_set = DocumentSet(doc)
            doc_path = self.training_dir + os.path.sep + doc
            input_docs = get_subfolders(doc_path)
            for in_doc in input_docs:
                if in_doc == 'keys':
                    # skip the keys for now...
                    continue
                processed_doc = Document(doc_path, in_doc, ["tokens"])
                doc_set.add(processed_doc)
            all_training_doc_sets.append(doc_set)

    def predict(self):
        pass
