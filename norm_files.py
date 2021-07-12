#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil

from bib_recognition.files_tools import read_json_file, save_json_file, creat_folder_if_not_exist

DATASET_PATH = os.path.join("bib_dataset_draft", "bib")
IMAGE_SHAPE = 224
NORM_PATH = "norm"
NORM_PATH_IMAGES = os.path.join(NORM_PATH, "images")
creat_folder_if_not_exist(NORM_PATH_IMAGES)

data = read_json_file(os.path.join("bib_dataset_draft", "via_region_data.json"))

norm_json = {}

for pict in data.values():
    if isinstance(pict.get("regions"), list) and len(pict.get("regions")) > 0:
        filename = pict.get("filename")
        shutil.copy(os.path.join(DATASET_PATH, filename), os.path.join(NORM_PATH_IMAGES, filename))
        for region in pict.get("regions"):
            shape_attributes = region.get("shape_attributes")
            norm_json.setdefault(filename, []).append({
                "ymin": shape_attributes.get("y"),
                "xmin": shape_attributes.get("x"),
                "ymax": shape_attributes.get("height") + shape_attributes.get("y"),
                "xmax": shape_attributes.get("width") + shape_attributes.get("x"),
            })

save_json_file(norm_json, os.path.join(NORM_PATH, "bounding_boxes.json"), indent=2)
