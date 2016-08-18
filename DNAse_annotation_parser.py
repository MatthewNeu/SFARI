import sys, re
from sys import argv

input_vcf_filename = sys.argv[1]

list_ENCFF530EKX_column = []

#print "The below data is for the file in the following path:", input_vcf_filename
with open(input_vcf_filename, "r") as input_vcf:
    total = 0
    for line in input_vcf:
        if line.startswith('#'):
            continue

        if line.startswith('CHROM'):
            continue

        split_line = line.strip().split("\t")

        ENCFF530EKX_column = split_line[13]
        ENCFF737WUQ_column = split_line[14]
        ENCFF804SPK_column = split_line[15]
        ENCFF876ORT_column = split_line[16]
        ENCFF985KHI_column = split_line[17]

        list_ENCFF530EKX_column.append(ENCFF530EKX_column)

        #print list_ENCFF530EKX_column
    #print list_ENCFF530EKX_column.count('1')

    total += list_ENCFF530EKX_column.count('1')
    print total

        #print ENCFF530EKX_column, ENCFF737WUQ_column, ENCFF804SPK_column, ENCFF876ORT_column, ENCFF985KHI_column

