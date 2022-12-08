import json
from tqdm import tqdm

from config import DOMAIN_TO_SENSE, CLASS_TO_SENSE, DICTIONARY


POS_ORDER = ["noun", "adjective", "verb", "proper"]

def get_sem_link_words(dictionary, sem_link_key):
    sem_link_words = set()
    for entry in dictionary.values():
        if sem_link_key in entry["semLinks"]:
            sem_link_words.update(entry["semLinks"][sem_link_key])
    return sem_link_words


def get_sense_possibilities(dictionary, sem_link_words):
    sem_link_senses = { word: [] for word in sem_link_words }

    for sense_id, entry in tqdm(dictionary.items()):
        if entry["pos"] not in POS_ORDER:
            continue
        
        word_forms = [ word_form.lower() for word_form in entry["wordForms"] ]
        
        for sem_link_word in sem_link_words:
            if sem_link_word.lower() in word_forms:
                sem_link_senses[sem_link_word].append(sense_id)
    
    return sem_link_senses


def select_sense(dictionary, sem_link_word, senses, sem_link_key):
    candidates = []
    
    for sense in senses:
        entry = dictionary[sense]
        sem_links = entry["semLinks"]
        direct_link = sem_link_key in sem_links and sem_link_word in sem_links[sem_link_key]
        candidates.append((sense, (not direct_link, POS_ORDER.index(entry["pos"]), -entry["knownness"])))
    
    candidates = sorted(candidates, key=lambda candidate: candidate[1])
    if len(candidates) > 0:
        sense, _ = candidates[0]
        return sense

    return None


def assign_senses(dictionary, sem_link_senses, sem_link_key):
    sem_link_to_sense = dict()
    for sem_link, senses in sem_link_senses.items():
        sem_link_to_sense[sem_link] = select_sense(dictionary, sem_link, senses, sem_link_key)
    return sem_link_to_sense


def disambiguate_sem_link(out_file, sem_link_key):
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())

    sem_link_words = get_sem_link_words(dictionary, sem_link_key)
    sem_link_senses = get_sense_possibilities(dictionary, sem_link_words)
    sem_link_word_to_sense = assign_senses(dictionary, sem_link_senses, sem_link_key)

    print("Unassigned sem links", list(sem_link_word_to_sense.values()).count(None), "/", len(sem_link_word_to_sense))

    with open(out_file, "w+") as file:
        file.write(json.dumps(sem_link_word_to_sense, sort_keys=True, indent=4))


def disambiguate_domains():
    disambiguate_sem_link(DOMAIN_TO_SENSE, "domains")


def disambiguate_classes():
    disambiguate_sem_link(CLASS_TO_SENSE, "classes")