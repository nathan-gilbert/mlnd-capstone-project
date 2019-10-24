import operator

import networkx as nx
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

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
        # labels = self.__get_labels()
        # self.model.fit(self.feature_vector, labels)

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
            # for word, count in doc_set.word_counts.items():
            #    global_counts = global_counts.get(word, 0) + count

            # get the top 1000 words in the training set
            top_1000_counts = sorted(global_counts.items(),
                                     key=operator.itemgetter(1),
                                     reverse=True)[:1000]

        self.__unsupervised_features(all_training_doc_sets, top_1000_counts)
        # self.__word_location_features(all_training_doc_sets)
        # self.__word_type_features(all_training_doc_sets)

    def __unsupervised_features(self, all_docs_sets, top_k_counts):
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

                # FutureWork: LLR -  current document terms vs entire training corpus

                # TextRank
                sentences = doc.annotations["sentences"]
                ranked_sentences = self.__get_text_rank(sentences)[:3]


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

    # pylint: disable=too-many-locals
    def __get_text_rank(self, sentences):
        """
        Generate a ranked list of sentences from the document that are ranked
        by the PageRank algorithm.
        :return: ranked_sentences
        """
        # Extract word vectors
        word_embeddings = {}
        with open('glove.6B.100d.txt', encoding='utf-8') as in_file:
            for line in in_file:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                word_embeddings[word] = coefs

        clean_sentences = [self._remove_stop_words(r.split()) for r in sentences]
        sentence_vectors = []
        for i in clean_sentences:
            if len(i) != 0:
                s_v = sum(
                    [word_embeddings.get(w, np.zeros((100,))) for w in i.split()]
                ) / (len(i.split()) + 0.001)
            else:
                s_v = np.zeros((100,))
            sentence_vectors.append(s_v)

        # similarity matrix
        sim_mat = np.zeros([len(sentences), len(sentences)])
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    sim_mat[i][j] = \
                        cosine_similarity(
                            sentence_vectors[i].reshape(1, 100), sentence_vectors[j].reshape(1, 100)
                        )[0, 0]

        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank(nx_graph)
        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        return ranked_sentences


if __name__ == "__main__":
    rs = RegSum()
    rs.train()
