from config import DOMAIN_TO_SENSE, TEST_LABELS, CLASS_TO_SENSE

import os
import json

def base_test_sem_links(labels_file, predictions_file):
    with open(os.path.join(TEST_LABELS, labels_file)) as file:
        labels = json.loads(file.read())
    
    with open(predictions_file) as file:
        predictions = json.loads(file.read())
    
    for sem_link_word, expected_sem_link_senses in labels.items():
        assert predictions[sem_link_word] in expected_sem_link_senses, f"Expected {sem_link_word} to have sense in {expected_sem_link_senses} but was {predictions[sem_link_word]}"


def test_domains():
    base_test_sem_links("domain_labels.json", DOMAIN_TO_SENSE)


def test_classes():
    base_test_sem_links("class_labels.json", CLASS_TO_SENSE)