import yaml


def read_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f_config:
        config_data = yaml.load(f_config.read(), Loader=yaml.FullLoader)
    return config_data
