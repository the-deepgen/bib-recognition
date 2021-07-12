#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
All functions to read, write json files or csv files
"""

from __future__ import absolute_import

import io
import json
import os


def read_json_file(json_file_abs_path):
    """
    Read a json file in utf-8
    :param json_file_abs_path: (string) path to the json to read
    :return: (dic) dic of the json file
    """
    with io.open(json_file_abs_path, "r", encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data


def save_json_file(json_dic, file_name, indent=None):
    """
    Save dic to json file
    :param json_dic: (dict) dictionary need to be save
    :param file_name: (string) name of the file
    :param indent: (int) if not None add indent
    """
    with io.open(file_name, "w", encoding="utf-8") as f:
        if indent is None:
            json.dump(json_dic, f, ensure_ascii=False)
        else:
            json.dump(json_dic, f, indent=indent, ensure_ascii=False)


def save_file(text, file_name):
    """
    Save a file into utf-8 encoding
    :param text: (string) text to save
    :param file_name: (string) name of the file
    """
    with io.open(file_name, "w", encoding="utf-8") as f:
        f.write(text)


def creat_folder_if_not_exist(path):
    """
    Creat a folder if is not existe
    Note: if you have /folder1/folder2
    If folder1 not exist we will creat folder1 and folder2
    :param path: (string) path to creat
    """
    if not os.path.exists(path):
        os.makedirs(path)
