import os
import operator
from summerizer.annotations.document import Document
from summerizer.annotations.document_set import DocumentSet
from data_utils.data_organizer import get_subfolders
from summerizer.summerizer import Summerizer
from sklearn.linear_model import LogisticRegression


class RegSum(Summerizer):
    def __init__(self):
        super().__init__()
        self.__summary = []
        self.training_vector = None
        self.model = LogisticRegression()

    def train(self):
        self.__generate_features()
        # todo train the model

    def predict(self):
        pass

    def create_summary(self, src_docs):
        raise NotImplementedError

    def __generate_features(self):
        # iterate over sentences and build feature vectors
        print("Training on documents: ")
        all_training_doc_sets = {}

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
            all_training_doc_sets[doc] = doc_set

        global_counts = {}
        top_1000_counts = []
        for doc_set in all_training_doc_sets.values():
            doc_set.create_word_probabilities()
            # create global word counts for LLR
            for word, count in doc_set.word_counts.items():
                global_counts = global_counts.get(word, 0) + count

            # get the top 1000 words in the training set
            top_1000_counts = sorted(global_counts.items(),
                                     key=operator.itemgetter(1),
                                     reverse=True)[:1000]
        self.__unsupervised_features(all_training_doc_sets, global_counts, top_1000_counts)
        self.__word_location_features(all_training_doc_sets)
        self.__word_type_features(all_training_doc_sets)

    def __unsupervised_features(self, all_docs_sets, global_counts, top_1000_counts):
        # FreqSum - take the top K words from training data
        # LLR - input document vs entire corpus
        # TextRank
        pass

    def __word_location_features(self, all_docs):
        # 6 types
        # earliest first location
        # latest last location
        # average location
        # average first location
        pass

    def __word_type_features(self, all_docs):
        # part of speech tags
        # named entity
        # unigrams from training documents
        pass
