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
SIZEC = 27

# Read image names and channels from annotation CSV file
images = {}
annotation_file = os.path.join(
    EXPERIMENT_DIRECTORY, 'idr0054-experimentA-annotation.csv')
with open(annotation_file, 'r') as f:
    f_csv = csv.reader(f, delimiter=',')
    headers = next(f_csv)  # First row is header
    for row in f_csv:
        name = row[0]
        channels = [x.strip() for x in row[-1].split(',')]
        assert len(channels) == SIZEC, 'Found %s channels' % len(channels)
        files = ['' for i in range(SIZEC)]
        images[name] = {'files': files, 'channels': channels}

# Read mapping between channels and files on disk from assays file
assays_file = os.path.join(
    EXPERIMENT_DIRECTORY, 'idr0054-experimentA-assays.txt')
MAPPING = {
    'Donor1': 'Tonsil 1',
    'Donor2': 'Tonsil 2',
    'DonorA': 'Tonsil 3'}
with open(assays_file, 'r') as f:
    f_csv = csv.reader(f, delimiter='\t')
    headers = next(f_csv)  # First row is header
    for row in f_csv:
        image = images[MAPPING[row[0]]]
        channel_index = image['channels'].index(row[20].rstrip())
        image['files'][channel_index] = row[16]

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

    # Check rendering file
    rendering_file = os.path.join(
        EXPERIMENT_DIRECTORY, 'rendering_settings', name + '.yml')
    with open(rendering_file, 'r') as f:
        d = yaml.load(f)
        assert d['version'] == 2
        assert d['greyscale'] is False
        assert d['channels'].keys() == [i + 1 for i in range(SIZEC)]
        for i in range(SIZEC):
            assert d['channels'][i + 1]['label'] == channels[i]
            assert d['channels'][i + 1]['active'] is (i < 7)

with open(os.path.join(
        EXPERIMENT_DIRECTORY, "idr0054-experimentA-filePaths.tsv"), 'w') as f:
    for name in sorted(images):
        pattern_file = os.path.join(IDR_PATTERNS_DIRECTORY, name + ".pattern")
        index = name[5]
        if index == "A":
            index = 3

        f.write("Dataset:name:Tonsil\t%s\tTonsil %s\n" % (pattern_file, index))
