from ruamel.yaml import YAML

yaml = YAML()


def get_yml_data(yml_path):
    with open(yml_path, "r") as f_nlu:
        return yaml.load(f_nlu)


def get_all_data():
    data_path = "./data/guotie/nlu.yml"
    datas = get_yml_data(data_path)
    data_list = []
    for item in datas["nlu"]:
        data_list += [line[2:] for line in item["examples"].splitlines()]
    return data_list
