from ruamel.yaml import YAML

yaml = YAML()


def read_yaml(yaml_path):
    with open(yaml_path, "r") as f_yaml:
        datas = yaml.load(f_yaml)
    return datas


def get_conf(conf_path=None):
    if conf_path is None:
        conf_path = "./conf/guotie.yaml"

    return read_yaml(conf_path)
