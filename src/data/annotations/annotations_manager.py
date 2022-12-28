import json


class AnnotationsManager:
    def __init__(
        self,
        annotations_path: str
    ) -> None:
        self.annotations_path = annotations_path

        with open(self.annotations_path, mode='r', encoding='utf-8') as file:
            self.annotations = json.loads(file.read())

    def get_annotations(self):
        return self.annotations
