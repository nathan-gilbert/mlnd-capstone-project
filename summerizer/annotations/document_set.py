class DocumentSet:
    def __init__(self, n):
        self.documents = []
        # attributes collected from all documents in the set
        self.attributes = {}
        self._set_name = n

    def name(self):
        return self._set_name

    def add(self, doc):
        self.documents.append(doc)

    def __create_word_probabilities(self):
        # iterate the documents and count the number of non-stop words
        self.attributes["word_counts"] = None
        self.attributes["totals_non_stop_words"] = 0
