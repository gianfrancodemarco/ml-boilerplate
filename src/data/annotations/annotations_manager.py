import json

class AnnotationsManager:
    def __init__(
        self,
        annotations_path: str    
    ) -> None:
        self.annotations_path = annotations_path
    
        with open(self.annotations_path, 'r') as f:
             self.annotations = json.loads(f.read())

    def get_annotations(self):
        return self.annotations