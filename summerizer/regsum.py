import operator

from sklearn.linear_model import LogisticRegression

from summerizer.summerizer import Summerizer


class RegSum(Summerizer):
    def __init__(self):
        super().__init__()
        self.__summary = []
        self.feature_vector = None
        self.feature_vector_columns = None
        self.model = LogisticRegression()

    def train(self):
        self.__generate_features()
        labels = self.__get_labels()
        self.model.fit(self.feature_vector, labels)

    def predict(self):
        pass

    def create_summary(self, src_docs):
        raise NotImplementedError

    def __generate_features(self):
        # iterate over sentences and build feature vectors
        print("Training on documents: ")
        all_training_doc_sets = self._text_sents_tokens()

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
        # self.__word_location_features(all_training_doc_sets)
        # self.__word_type_features(all_training_doc_sets)

    def __unsupervised_features(self, all_docs_sets, global_counts, top_k_counts):
        # FreqSum - take the top K words from training data
        for doc_set in all_docs_sets:
            for doc in doc_set:
                sentences = doc.annotations["sentences"]
                for sentence in sentences:
                    word_list = self._remove_stop_words(self._normalize(sentence.text))
                    for top_k in top_k_counts:
                        self.feature_vector_columns.append(top_k)
                        if top_k in word_list:
                            self.feature_vector.append(doc_set.word_counts.get(top_k, 0.0))
                        else:
                            self.feature_vector.append(0.0)

        # LLR - input document vs entire corpus

        # TextRank

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

    def __get_labels(self):
        pass
