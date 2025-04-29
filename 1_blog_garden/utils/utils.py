# -*- coding = utf-8 -*-
# @Time : 2025/4/29 22:47
# @Author : 鬼鬼
# @File : utils.py
# @Software: PyCharm

import yaml
import os


def get_cfgs(cfgs_path):
    with open(cfgs_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def flag_file_exist(file):
    if os.path.exists(file):
        return True
    return False


def main():
    pass


if __name__ == "__main__":
    main()
