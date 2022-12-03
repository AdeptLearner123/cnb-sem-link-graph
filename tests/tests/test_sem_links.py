from config import DOMAIN_TO_SENSE, TEST_LABELS, CLASS_TO_SENSE

import os
import json

def test_sem_links(labels_file, predictions_file):
    with open(os.path.join(TEST_LABELS, labels_file)) as file:
        labels = json.loads(file.read())
    
    with open(predictions_file) as file:
        predictions = json.loads(file.read())
    
    for sem_link_word, sem_link_sense in labels.items():
        assert predictions[sem_link_word] == sem_link_sense, f"Expected {sem_link_word} to have sense {sem_link_sense} but was {predictions[sem_link_word]}"


def test_domains():
    test_sem_links("domain_labels.json", DOMAIN_TO_SENSE)


#def test_classes():
#    test_sem_links("class_labels".json, CLASS_TO_SENSE)