from config import DICTIONARY, SYNONYM_SENSES

import json
from collections import defaultdict

def get_word_to_senses(dictionary):
    word_to_senses = defaultdict(lambda: [])
    for sense_id, entry in dictionary.items():
        word_to_senses[entry["word"]].append(sense_id)
    return word_to_senses


def get_synonym_sense(sense_id, synonym_word, word_to_senses, dictionary):
    word = dictionary[sense_id]["word"]
    synonym_senses = word_to_senses[synonym_word]

    for synonym_sense in synonym_senses:
        synonym_sem_links = dictionary[synonym_sense]["semLinks"]

        if "synonyms" in synonym_sem_links:
            if word in synonym_sem_links["synonyms"]:
                return synonym_sense
    return None


def main():
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())
    
    word_to_senses = get_word_to_senses(dictionary)

    synonym_senses = defaultdict(lambda: [])
    for sense_id, entry in dictionary.items():
        sem_links = entry["semLinks"]
        
        if "synonyms" in sem_links:
            for synonym_word in sem_links["synonyms"]:
                synonym_sense = get_synonym_sense(sense_id, synonym_word, word_to_senses, dictionary)
                if synonym_sense is not None:
                    synonym_senses[sense_id].append(synonym_sense)
    
    with open(SYNONYM_SENSES, "w+") as file:
        file.write(json.dumps(synonym_senses, indent=4))
            


if __name__ == "__main__":
    main()