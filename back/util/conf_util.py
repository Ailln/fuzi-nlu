from ruamel.yaml import YAML

yaml = YAML()


def read_config(config_path=None):
    if config_path is None:
        config_path = "./config/guotie.yaml"

    with open(config_path, "r", encoding="utf-8") as f_config:
        config_data = yaml.load(f_config.read())
    return config_data
