from ruamel.yaml import YAML

yaml = YAML()


def read_conf(conf_path=None):
    if conf_path is None:
        conf_path = "./conf/guotie.yaml"

    with open(conf_path, "r", encoding="utf-8") as f_conf:
        conf_data = yaml.load(f_conf.read())
    return conf_data
