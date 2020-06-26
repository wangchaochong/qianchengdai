import yaml


def red_config(file):
    with open(file, encoding="utf-8") as f:
        conf = yaml.safe_load(f)
    return conf

