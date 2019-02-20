#! /usr/bin/env python
# Script for symlinking original PNG files and combining them using pattern
# files

import csv
import os.path
import sys

BASE_DIRECTORY = "/nfs/bioimage/drop/idr0054-segura-tonsilhyperion/S-BSST221/"
EXPERIMENT_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(
        sys.argv[0]))), 'experimentA')
PATTERNS_DIRECTORY = os.path.join(EXPERIMENT_DIRECTORY, 'patterns')
ASSAYS_FILE = os.path.join(
    EXPERIMENT_DIRECTORY, 'idr0054-experimentA-assays.txt')
UOD_METADATA_DIRECTORY = os.path.join(
    "/uod/idr/metadata/idr0054-segura-tonsilhyperion", "experimentA",
    "patterns")

images = {}
with open(ASSAYS_FILE, 'r') as f:
    f_csv = csv.reader(f, delimiter='\t')
    headers = next(f_csv)
    for row in f_csv:
        if row[0] not in images.keys():
            images[row[0]] = {'files': [], 'channels': []}
        images[row[0]]['files'].append(row[16])
        images[row[0]]['channels'].append(row[20])

for name in images:
    image_folder = os.path.join(PATTERNS_DIRECTORY, name)
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)

    pattern = "C_<"
    files = images[name]['files']
    for i in range(len(files)):
        src = os.path.join(BASE_DIRECTORY, files[i])
        dest = os.path.join(image_folder, "C_%s.png" % i)
        if not os.path.islink(dest):
            os.symlink(src, dest)
    pattern_filename = "C_<" + ",".join(map(str, range(len(files)))) + ">.png"
    pattern_fullpath = os.path.join(
        UOD_METADATA_DIRECTORY, name, pattern_filename)

    with open(image_folder + ".pattern", "w") as f:
        f.write(pattern_fullpath)
