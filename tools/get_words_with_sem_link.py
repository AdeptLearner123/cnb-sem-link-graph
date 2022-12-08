from config import DICTIONARY

from argparse import ArgumentParser
import json

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("word", type=str)
    parser.add_argument("--domain", action="store_true")
    args = parser.parse_args()
    return args.word, args.domain


def main():
    word, is_domain = parse_args()

    with open(DICTIONARY, "r") as file:
        dictionary = json.loads(file.read())
    
    for sense_id, entry in dictionary.items():
        sem_links = entry["semLinks"]
        if "domains" in sem_links:
            if word in sem_links["domains"]:
                print(sense_id, entry["word"])