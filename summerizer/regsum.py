import uuid
import operator
import os
import sys

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, '.')
sys.path.insert(0, '..')
from summerizer.summerizer import Summerizer
from summerizer.annotations.annotation_set import AnnotationSet
from data_utils.data_organizer import get_subfolders


class RegSum(Summerizer):
    def __init__(self):
        super().__init__()
        self.__summary = []
        self.feature_vectors = None
        self.words2uuids = {}
        self.model = LogisticRegression()

    def train(self):
        self.__generate_features()
        self.__get_labels()

        # create the Logistic Regression model
        self.feature_vectors = pd.DataFrame(self.feature_vectors)
        X = pd.DataFrame(self.feature_vectors.iloc[:, :-1])
        y = pd.DataFrame(self.feature_vectors.iloc[:, -1])
        self.model.fit(X, y)

    def predict(self):
        pass

    def create_summary(self, src_docs):
        raise NotImplementedError

    def __generate_features(self):
        # map column name to index
        self.feature_vectors = []

        # iterate over sentences and build feature vectors
        print("Training on documents: ")
        all_training_doc_sets = self._text_sents_tokens()

        global_counts = {}
        top_1000_counts = []
        for doc_set in all_training_doc_sets.values():
            doc_set.create_word_probabilities()

            # create global word counts for top_k & LLR
            for word, count in doc_set.word_counts.items():
                # don't count stop words obvs
                if self._is_stop_word(word):
                    continue
                global_counts[word] = global_counts.get(word, 0) + count

            # get the top 1000 words in the training set
            top_1000_counts = sorted(global_counts.items(),
                                     key=operator.itemgetter(1),
                                     reverse=True)[:1000]

        self.__unsupervised_features(all_training_doc_sets, top_1000_counts)
        # self.__word_location_features(all_training_doc_sets)
        # self.__word_type_features(all_training_doc_sets)
        # convert to Pandas Dataframe

    def __unsupervised_features(self, all_doc_sets, top_k_counts):
        # FreqSum - take the top K (non stop word) words from training data
        for doc_set in all_doc_sets:
            print(f"Document: {doc_set}...")
            # iterating over all documents in data
            for doc in all_doc_sets[doc_set]:
                sentences = doc.annotations["sentences"]
                s = 1
                # iterating over all sentences in data
                for sentence in sentences:
                    print(f"\tSentence {s}/{len(sentences)}...")
                    word_list = self._remove_stop_words(self._normalize(sentence.text))
                    # iterating over words in sentences in documents of the data
                    word_id = 0
                    word_key = f"{doc_set}:{s}:{word_id}"
                    for word in word_list:
                        feature_vector = {}
                        row_uuid = uuid.uuid4()
                        # Where the mapping from a particular word in the data to uuid is set
                        self.words2uuids[word_key] = row_uuid
                        feature_vector["uuid"] = row_uuid
                        feature_vector["word"] = word
                        feature_vector["word_key"] = word_key
                        for top_k in top_k_counts:
                            if top_k in word_list:
                                feature_vector[top_k] = 1
                            else:
                                feature_vector[top_k] = 0
                        word_id += 1
                        self.feature_vectors.append(feature_vector)
                    s += 1
                # FutureWork: LLR -  current document terms vs entire training corpus
                # TextRank
                # sentences = doc.annotations["sentences"]
                # ranked_sentences = self.__get_text_rank(sentences)[:3]

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
        for doc in self.training_docs:
            doc_path = self.training_dir + os.path.sep + doc
            input_docs = get_subfolders(doc_path)
            for in_doc in input_docs:
                if in_doc != 'keys':
                    continue
                keys = AnnotationSet("answer_keys")
                key_file = f"{doc_path}{os.path.sep}keys{os.path.sep}annotations{os.path.sep}answer_keys"
                keys.read_annotation_file(key_file)
                key_text = keys.get(0).text.replace("\n", " ").lower()
                key_cleaned = self._remove_stop_words(key_text.split())

                for vec in self.feature_vectors:
                    if vec['word'] in key_cleaned:
                        vec['target'] = 1
                    else:
                        vec['target'] = 0

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
    rs.training_dir = "/Users/nathan/Documents/Data/summarization/duc2003"
    rs.training_docs = ["0", "1", "10", "11", "12", "13", "14", "15", "16",
                             "17", "18", "19", "2", "20", "21", "22", "23", "24",
                             "25", "26", "27", "28", "29", "3", "30", "31", "32",
                             "33", "34", "35", "36", "37", "38", "39", "4", "40",
                             "41", "42", "43", "44", "45", "46", "47", "48", "49",
                             "5", "50", "51", "52", "53", "54", "55", "56", "57",
                             "58", "59", "6", "7", "8", "9"]
    rs.train()
