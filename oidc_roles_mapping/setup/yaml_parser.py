import yaml
import os.path

def parse(config_file_path):
    with open(config_file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content
