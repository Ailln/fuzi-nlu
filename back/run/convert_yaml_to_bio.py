import re
import argparse

from ruamel.yaml import YAML

parse = argparse.ArgumentParser("convert yaml to bio")
parse.add_argument("--yaml", required=True, help="yaml path")
parse.add_argument("--bio", required=True, help="bio path")
args = parse.parse_args()

yaml = YAML()


def yaml_to_bio():
    with open(args.yaml, "r") as f_yaml:
        nlu_data = yaml.load(f_yaml)

    output_list = []
    for nlu in nlu_data["nlu"]:
        intent = nlu["intent"]
        for example in nlu["examples"].split("\n"):
            if example != "":
                example = example[2:]
                last = 0
                entity_list = []
                for res in re.finditer(r"\[.*?\]\(.*?\)", example):
                    span = res.span()
                    entity_item = res.group()
                    content = entity_item.split("](")[0][1:]
                    entity = entity_item.split("](")[1][:-1]
                    start = span[0] - last
                    end = start + len(content) - 1
                    example = example[:span[0] - last] + content + example[span[1] - last:]
                    last = len(entity) + 4
                    entity_list.append([start, end, entity])

                input_data = " ".join([char for char in example])
                target_list = ["O"]*len(example)
                for pos_entity in entity_list:
                    start, end, entity = pos_entity
                    for i in range(start, end+1, 1):
                        if i == start:
                            entity_label = f"B-{entity}"
                        else:
                            entity_label = f"I-{entity}"
                        target_list[i] = entity_label
                target_data = " ".join(target_list)
                output_list.append(f"{input_data}\t{target_data}\t{intent}")

    output = "\n".join(output_list)

    with open(args.bio, "w") as f_bio:
        f_bio.write(output)

    print("convert success!")


if __name__ == '__main__':
    yaml_to_bio()
