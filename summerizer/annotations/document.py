import os

from summerizer.annotations.annotation_set import AnnotationSet


# pylint: disable=too-few-public-methods
class Document:
    def __init__(self, pd, fn, annotations):
        self.annotations = {}
        self.attributes = {}
        self._parent_directory = pd
        self._filename = fn
        self._file_full_path = f"{self._parent_directory}{os.path.sep}{self._filename}{os.path.sep}"
        self._ann_dir = "annotations"

        self.__initialize_document(annotations)

    def __initialize_document(self, annotations):
        for ann_type in annotations:
            ann_set = AnnotationSet(ann_type)
            ann_full_path = self._file_full_path + self._ann_dir + os.path.sep + ann_type
            ann_set.read_annotation_file(ann_full_path)
            self.annotations[ann_type] = ann_set
