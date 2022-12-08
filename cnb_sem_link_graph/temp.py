from config import TEST_LABELS

import os
import json

def main():
    path = os.path.join(TEST_LABELS, "synonym_labels.json")
    with open(path, "r") as file:
        labels = json.loads(file.read())
    
    for key in labels:
        labels[key] = [ labels[key] ]
    
    with open(path, "w") as file:
        file.write(json.dumps(labels, indent=4))