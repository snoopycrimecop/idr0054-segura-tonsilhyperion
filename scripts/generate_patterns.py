#! /usr/bin/env python
# Script for symlinking original PNG files and combining them using pattern
# files

import os.path
import sys

BASE_DIRECTORY = "/nfs/bioimage/drop/idr0054-segura-tonsilhyperion/S-BSST221/"
METADATA_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(
        sys.argv[0]))), 'experimentA', 'patterns')
IMAGES = {'Donor1': 'd1 normalized_'}
CHANNELS = [
    'CD206', 'IL-21', 'CD185(CXCR5)', 'CD45', 'empty', 'CXCL13',
    'CD1c-biotin-NA', 'CD303(BDCA2)', 'CD11b', 'CD45RA', 'Bcl-6',
    'E-Cadherin', 'CD141', 'CD123', 'CD68', 'HLA-DR', 'CD279(PD-1)', 'aSMA',
    'CD370', 'CD11c', 'CD19', 'ICOS', 'DNA1', 'CD56(NCAM)', 'DNA2', 'CD3',
    'CD14']


for name, prefix in IMAGES.iteritems():
    image_folder = os.path.join(METADATA_DIRECTORY, name)
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)

    pattern = "%s/C_<" % name
    for c in range(len(CHANNELS)):
        src = os.path.join(BASE_DIRECTORY, "%s%s.png" % (prefix, CHANNELS[c]))
        dest = os.path.join(image_folder, "C_%s.png" % c)
        if not os.path.islink(dest):
            os.symlink(src, dest)

        if c == 0:
            pattern += "%s" % c
        else:
            pattern += ",%s" % c
    pattern += ">.png"

    with open(image_folder + ".pattern", "w") as f:
        f.write(pattern)
