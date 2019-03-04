#! /usr/bin/env python
# Script for symlinking original PNG files and combining them using pattern
# files

import csv
import os.path
import sys
import yaml

BASE_DIRECTORY = "/uod/idr/filesets/idr0054-segura-tonsilhyperion/S-BSST221/"
EXPERIMENT_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(
        sys.argv[0]))), 'experimentA')
LOCAL_PATTERNS_DIRECTORY = os.path.join(EXPERIMENT_DIRECTORY, 'patterns')
IDR_PATTERNS_DIRECTORY = os.path.join(
    "/uod/idr/metadata/idr0054-segura-tonsilhyperion", "experimentA",
    "patterns")

# Read list of constituent PNGs for the three images from submitted assays file
images = {}
assays_file = os.path.join(
    EXPERIMENT_DIRECTORY, 'idr0054-experimentA-assays.txt')
with open(assays_file, 'r') as f:
    f_csv = csv.reader(f, delimiter='\t')
    headers = next(f_csv)  # First row is header
    for row in f_csv:
        if row[0] not in images.keys():
            images[row[0]] = {'files': [], 'channels': []}
        images[row[0]]['files'].append(row[16])
        images[row[0]]['channels'].append(row[20].rstrip())


# Move active channels to the first positions
FIRST_CHANNELS = ["CD3-170Er", "CD19-169Tm", "CD324/E-Cadherin-158Gd"]
for name in images:
    for channel in reversed(FIRST_CHANNELS):
        index = images[name]['channels'].index(channel)
        images[name]['files'].insert(0, images[name]['files'].pop(index))
        images[name]['channels'].insert(0, images[name]['files'].pop(index))


for name in images:
    files = images[name]['files']
    channels = images[name]['channels']

    # Symlink original images under experimentA/patterns
    image_folder = os.path.join(LOCAL_PATTERNS_DIRECTORY, name)
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)

    # Generate pattern file
    pattern = "C_<"
    for i in range(len(files)):
        src = os.path.join(BASE_DIRECTORY, files[i])
        dest = os.path.join(image_folder, "%s_C%s.png" % (name, "%02d" % i))
        if not os.path.islink(dest):
            os.symlink(src, dest)
    pattern_filename = "%s_C<00-%s>.png" % (name, len(files) - 1)
    pattern_fullpath = os.path.join(
        IDR_PATTERNS_DIRECTORY, name, pattern_filename)
    with open(image_folder + ".pattern", "w") as f:
        f.write(pattern_fullpath + "\n")

    # Rendering files
    d = {'version': 2, 'channels': {}, 'greyscale': False}
    for i in range(len(files)):
        if (i % 3) == 0:
            color = "FF0000"
        elif (i % 3) == 1:
            color = "00FF00"
        else:
            color = "0000FF"
        active = (i < 3)
        d['channels'][i + 1] = {
            'label': channels[i],
            'color': color,
            'active': active}
    with open(os.path.join(EXPERIMENT_DIRECTORY, name + ".yml"), 'w') as f:
        yaml.dump(d, f, explicit_start=True, width=80, indent=4,
                  default_flow_style=False)

with open(os.path.join(
        EXPERIMENT_DIRECTORY, "idr0054-experimentA-filePaths.tsv"), 'w') as f:
    for name in sorted(images):
        pattern_file = os.path.join(IDR_PATTERNS_DIRECTORY, name + ".pattern")
        index = name[5]
        if index == "A":
            index = 3

        f.write("Dataset:name:Tonsil\t%s\tTonsil %s\n" % (pattern_file, index))
