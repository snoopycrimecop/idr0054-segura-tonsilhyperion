#! /usr/bin/env python
# Script for symlinking original PNG files and combining them using pattern
# files

import os.path
import sys

BASE_DIRECTORY = "/nfs/bioimage/drop/idr0054-segura-tonsilhyperion/S-BSST221/"
METADATA_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(
        sys.argv[0]))), 'experimentA', 'patterns')
UOD_METADATA_DIRECTORY = os.path.join(
    "/uod/idr/metadata/idr0054-segura-tonsilhyperion", "experimentA",
    "patterns")
IMAGES = [
    {'name': 'Donor1',
     'prefix': 'd1 normalized_',
     'channels': [
        'CD206', 'IL-21', 'CD185(CXCR5)', 'CD45', 'empty', 'CXCL13',
        'CD1c-biotin-NA', 'CD303(BDCA2)', 'CD11b', 'CD45RA', 'Bcl-6',
        'E-Cadherin', 'CD141', 'CD123', 'CD68', 'HLA-DR', 'CD279(PD-1)',
        'aSMA', 'CD370', 'CD11c', 'CD19', 'ICOS', 'DNA1', 'CD56(NCAM)',
        'DNA2', 'CD3', 'CD14']},
    {'name': 'Donor2',
     'prefix': 'd2 normalized_',
     'channels': [
        'CD206', 'IL-21', 'CD185(CXCR5)', 'CD45', 'empty', 'CXCL13',
        'CD1c-biotin-NA', 'CD303(BDCA2)', 'CD11b', 'CD45RA', 'Bcl-6',
        'E-Cadherin', 'CD141', 'CD123', 'CD68', 'HLA-DR', 'CD279(PD-1)',
        'aSMA', 'CD370', 'CD11c', 'CD19', 'ICOS', 'DNA1', 'CD56(NCAM)',
        'DNA2', 'CD3', 'CD14']},
    {'name': 'DonorA',
     'prefix': 'normalized_',
     'channels': [
        'CD206', 'IL-21', 'CXCR5', 'CD45', 'IL3R', 'CXCL13',
        'CD1c', 'avanti', 'FoxP3', 'CD45RA', 'Bcl6',
        'E-Cadherin', 'CD44', 'Histon3', 'CTLA4', 'Collagen14', 'PD-1',
        'AlphaSMA', 'CD8a', 'CD11c', 'CD19', 'Rutenium Red', 'DNA1', 'Bcl2',
        'DNA3', 'CD3', 'CD14', 'KI67']}]

for image in IMAGES:
    image_folder = os.path.join(METADATA_DIRECTORY, image['name'])
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)

    pattern = "C_<"
    for c in range(len(image['channel'])):
        src = os.path.join(BASE_DIRECTORY, "%s%s.png" % (
            image['prefix'], image['channels'][c]))
        dest = os.path.join(image_folder, "C_%s.png" % c)
        if not os.path.islink(dest):
            os.symlink(src, dest)

        if c == 0:
            pattern += "%s" % c
        else:
            pattern += ",%s" % c
    pattern += ">.png"
    abspath_pattern = os.path.join(
        UOD_METADATA_DIRECTORY, image['name'], pattern)

    with open(image_folder + ".pattern", "w") as f:
        f.write(abspath_pattern)
