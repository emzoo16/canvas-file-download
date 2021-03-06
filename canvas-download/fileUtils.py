import os
import yaml
from values import *


def load_ignorelist(path):
    regex_list = []

    if os.path.isfile(path):
        with open(path) as f:
            regex_list = f.readlines()

    regex_list = [line.strip() for line in regex_list]
    return regex_list


def load_config(file):
    user_config = []
    if not os.path.exists(file):
        print("Please run init first")
        exit()

    with open(file) as config:
        user_config = yaml.load(config, Loader=yaml.FullLoader)

    return user_config


def save_to_config(config_object, file):
    file = open(config_path, "w")
    yaml.dump(config_object, file)
    file.close()


def make_directories_if_not_exist(folder_list, directory):
    for folder in folder_list:
        if not os.path.exists(directory + "/" + folder):
            os.mkdir(directory + "/" + folder)
