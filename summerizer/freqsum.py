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
        print("Training on documents: ")
        all_training_doc_sets = []
        for doc in self.training_docs:
            # contains one set of documents from DUC
            print(f"{self.training_dir}{os.path.sep}{doc}")
            doc_set = DocumentSet(doc)
            doc_path = self.training_dir + os.path.sep + doc
            input_docs = get_subfolders(doc_path)
            for in_doc in input_docs:
                if in_doc == 'keys':
                    # skip the keys for now...
                    continue
                processed_doc = Document(doc_path, in_doc, ["full_text", "sentences", "tokens"])
                doc_set.add(processed_doc)
            all_training_doc_sets.append(doc_set)

        for ds in all_training_doc_sets:
            ds.create_word_probabilities()

        self.model = all_training_doc_sets

    def predict(self):
        # Generate the summaries
        for ds in self.model:
            doc_summary = self.create_summary()
            score = self.scorer(doc_summary, "key")
            print(score)

    def create_summary(self):
        raise NotImplementedError


