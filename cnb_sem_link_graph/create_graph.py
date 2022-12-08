from config import CLASS_TO_SENSE, DOMAIN_TO_SENSE, SYNONYM_SENSES, DICTIONARY, EDGES

import json

def main():
    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())
    
    with open(DOMAIN_TO_SENSE, "r") as file:
        domain_to_sense = json.loads(file.read())
    
    with open(CLASS_TO_SENSE, "r") as file:
        class_to_sense = json.loads(file.read())

    with open(SYNONYM_SENSES, "r") as file:
        sense_synonyms = json.loads(file.read())

    edges = []

    for sense_id, entry in dictionary.items():
        sem_links = entry["semLinks"]
        if "domains" in sem_links:
            edges += [ (sense_id, domain_to_sense[domain], "DOMAIN") for domain in sem_links["domains"] if domain_to_sense[domain] is not None ]
        if "classes" in sem_links:
            edges += [ (sense_id, class_to_sense[domain], "CLASS") for domain in sem_links["classes"] if class_to_sense[domain] is not None ]

    for sense_id, synonym_senses in sense_synonyms.items():
        edges += [ (sense_id, synonym_sense, "SYNONYM") for synonym_sense in synonym_senses]

    lines = [ "\t".join(edge) for edge in edges ]
    
    with open(EDGES, "w+") as file:
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()