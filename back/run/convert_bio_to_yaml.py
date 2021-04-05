import argparse
from collections import defaultdict

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

parse = argparse.ArgumentParser("convert bio to yaml")
parse.add_argument("--bio", required=True, help="bio path")
parse.add_argument("--yaml", required=True, help="yaml path")
args = parse.parse_args()

yaml = YAML()


def bio_to_yaml():
    nlu_dict = defaultdict(list)
    with open(args.bio, "r") as f_bio:
        for line in f_bio.readlines():
            example, target, intent = line.strip().split("\t")
            example_list = example.split(" ")
            target_list = target.split(" ")
            entity_list = []
            for i, t in enumerate(target_list):
                if "B" == t[0]:
                    entity = t.replace("B-", "")
                    pos_start = i
                    for j in range(i+1, len(target_list), 1):
                        if f"I-{entity}" == target_list[j]:
                            pos_end = j
                        else:
                            entity_list.append([pos_start, pos_end, entity])
                            example_list[pos_start] = "[" + example_list[pos_start]
                            example_list[pos_end] = f"{example_list[pos_end]}]({entity})"
                            break

            nlu_dict[intent].append("".join(example_list))

    save_dict = {
        "version": "2.0",
        "nlu": []
    }
    for intent, examples in nlu_dict.items():
        save_dict["nlu"].append({
            "intent": intent,
            "examples": LiteralScalarString("- " + "\n- ".join(examples) + "\n")
        })

    with open(args.yaml, "w") as f_yaml:
        yaml.dump(save_dict, f_yaml)

    print("convert success!")


if __name__ == '__main__':
    bio_to_yaml()
