import operator
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

    @staticmethod
    def cf_sum(word_counts, word_list):
        """

        :param word_counts:
        :param word_list:
        :return: cf_sum
        """
        total_words = sum(word_counts.values())
        cf_sum = 0.0
        for word in word_list:
            cf_sum += word_counts.get(word, 0.0) / total_words
        return cf_sum

    def train(self):
        """

        :return:
        """
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

        for doc_set in all_training_doc_sets.values():
            doc_set.create_word_probabilities()

        print("Created FreqSum model over training docs...")
        self.model = all_training_doc_sets

    def predict(self):
        """

        :return: summaries - a dict of summaries for test docs
        """
        print("Testing on documents: ")
        summaries = {}
        for doc in self.test_docs:
            print(f"{self.test_dir}{os.path.sep}{doc}")
            input_doc_set = self.model[doc]
            test_doc_path = f"{self.test_dir}{os.path.sep}{doc}"
            summaries[test_doc_path] = self.create_summary(input_doc_set)
        return summaries

    def create_summary(self, src_docs):
        """

        :param src_docs:
        :return:
        """
        summary = []
        # iterate sentences, calculate CF_Sum, add to summary list if cosine
        # similarity is <= .5
        word_counts = src_docs.word_counts
        cf_sums = {}
        for doc in src_docs:
            sentence_set = doc.annotations["sentences"]
            for sentence in sentence_set:
                # normalize, tokenize & strip stop words
                word_list = self._remove_stop_words(self._normalize(sentence.text))

                # calculate CF_sum
                sentence_cf_sum = self.cf_sum(word_counts, word_list)
                cf_sums[sentence.text] = sentence_cf_sum

        # sort the sum values and create the summary list
        sorted_cf_sums = sorted(cf_sums.items(), key=operator.itemgetter(1), reverse=True)
        for text, cf_sum in sorted_cf_sums:
            if self._cosine_sim_check(text, summary) and self._size_check(text, summary):
                summary.append(text)
        return summary
