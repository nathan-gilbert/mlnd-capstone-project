import json


class Annotation:
    # pylint: disable=too-many-arguments
    def __init__(self, i, text, label, start, end):
        self.__id = int(i)
        self.__start = int(start)
        self.__end = int(end)
        self.__text = str(text)
        self.__label = str(label)

    def __len__(self):
        return len(self.__text)

    def __str__(self):
        return self.to_json()

    def __lt__(self, other):
        return self.__start < other.get_start()

    def __le__(self, other):
        return self.__start <= other.get_start()

    def __gt__(self, other):
        return self.__start > other.get_start()

    def __ge__(self, other):
        return self.__start >= other.get_start()

    def __eq__(self, other):
        if self.__start == other.get_start() and self.__end == other.get_end() \
            and self.__text == other.get_text() \
            and self.__label == other.get_label():
            return True
        return False

    def __ne__(self, other):
        if self.__start != other.get_start() or self.__end != other.get_end() \
            or self.__text != other.get_text() \
            or self.__label != other.get_label():
            return True
        return False

    def get_id(self):
        return self.__id

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end

    def get_text(self):
        return self.__text

    def get_span(self):
        return self.__start, self.__end

    def get_label(self):
        return self.__label

    def contains(self, other):
        return (self.__start <= other.get_start()) and (self.__end >= other.get_end())

    def clean_text(self):
        return "%s" % self.__text.replace("\n", " ")

    def clean_text_and_span(self):
        txt = self.__text.replace("\n", " ")
        return "%s (%d,%d)" % (txt, self.__start, self.__end)

    def to_dict(self):
        a_dict = {
            "id": self.__id,
            "start": self.__start,
            "end": self.__end,
            "text": self.__text,
            "label": self.__label
        }
        return a_dict

    def to_json(self):
        return json.dumps(self.to_dict())
