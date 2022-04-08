import re
import argparse

from ruamel.yaml import YAML

parse = argparse.ArgumentParser("generate domain from nlu")
parse.add_argument("--nlu", required=True, help="nlu path")
parse.add_argument("--domain", required=True, help="domain path")
args = parse.parse_args()

yaml = YAML()


def run():
    with open(args.nlu, "r") as f_nlu:
        nlu_data = yaml.load(f_nlu)

    intent_set = set()
    entity_set = set()

    for nlu_item in nlu_data["nlu"]:
        if "intent" in nlu_item:
            intent = nlu_item["intent"]
            intent_set.add(intent)

            for example in nlu_item["examples"].split("\n"):
                if example != "":
                    example = example[2:]
                    for res in re.finditer(r"\[.*?\]\(.*?\)", example):
                        entity_item = res.group()
                        entity = entity_item.split("](")[1][:-1]
                        entity_set.add(entity)

    domain_dict = {
        "version": "2.0",
        "intents": list(intent_set),
        "entities": list(entity_set)
    }

    with open(args.domain, "w") as f_domain:
        yaml.dump(domain_dict, f_domain)


if __name__ == '__main__':
    run()
