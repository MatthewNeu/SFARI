#!/usr/bin/python

import sys, re
from sys import argv
import os


################################
# Matthew Neu
# Aug 9 2016
# This script removes all commented lines from the bottom of a VCF file,
# then creates a new file with "footerless" appended to name.
#
# to run: remove_footer.py <filename.vcf>
################################

input_filtered_var_file = sys.argv[1]
dirname = os.path.dirname(input_filtered_var_file)
original_file = os.path.split(input_filtered_var_file)[1].split(".")[0]

try:
    input_file = open(input_filtered_var_file, "r")
except IOError:
    print "unable to open" , input_filtered_var_file
    sys.exit()

with input_file:
    line_list = input_file.readlines()

    pop_line = line_list.pop()

    while pop_line.startswith("#"):
        pop_line = line_list.pop()
        continue

outfile_name = os.path.join(dirname, original_file + "_footerless.vcf")

try:
    out_file = open(outfile_name, "w")
except IOError:
    print "unable to open" , outfile_name
    sys.exit()

with out_file:
    out_file.writelines(line_list)
