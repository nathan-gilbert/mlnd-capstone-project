from rouge import Rouge


# pylint: disable=too-few-public-methods
class Scorer:
    def __init__(self):
        self.rouge = Rouge()
        self.__last_score = None

    def rouge_score(self, hypothesis, key):
        scores = self.rouge.get_scores(hypothesis, key)
        self.__last_score = scores
        print(scores)

    def get_last_score(self):
        return self.__last_score
