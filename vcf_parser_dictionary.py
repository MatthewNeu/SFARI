import sys, re
from sys import argv

input_VCF_filename = sys.argv[1]
output_filename = input_VCF_filename + "_p"

if sys.argv[1] == "-h":
    print "Usage: <script> <input VCF> [-he het calls only] [-ho homozygous calls only] [-nr no repeats] [-r repeats only] [-nm no multiallelic calls] [-ma multiallelic calls only] [-ns no segdups] [-sd segdups only] [-ac1 only AC=1] [-na1 is not AC=1]"
    sys.exit()

output_filename = input_VCF_filename + "_p"

if "-he" in sys.argv:
    print "Considering het calls only."
    output_filename = output_filename + "_het_only"

if "-ho" in sys.argv:
    print "Considering Homozygous calls only."
    output_filename = output_filename + "_hom_only"

if "-he" or "-ho" not in sys.argv:
    print "Considering calls of all zygosity."

if "-nr" in sys.argv:
    print "Considering variants only in non-repetitive regions."
    output_filename = output_filename + "_no_repeats"

if "-r" in sys.argv:
    print "Considering variants only in repetitive regions"
    output_filename = output_filename + "_only_repeats"

if "-nr" or "-r" not in sys.argv:
    print "Considering variants in both repetitive and non-repetitive regions."

if "-nm" in sys.argv:
    print "Excluding multi-allelic calls."
    output_filename = output_filename + "_no_MA"

if "-ma" in sys.argv:
    print "Considering only multi-allelic calls."
    output_filename = output_filename + "_only_MA"

if "-nm" or "-ma" not in sys.argv:
    print "Considering all alleles."

if "-ns" in sys.argv:
    print "Excluding Segdups."
    output_filename = output_filename + "_no_sd"

if "-sd" in sys.argv:
    print "Considering only Segdups."
    output_filename = output_filename + "_only_sd"

if "-ac1" in sys.argv:
    print "Considering only calls of AC=1."
    output_filename = output_filename + "_only_AC_1"

if "-na1" in sys.argv:
    print "Excluding all calls of AC=1."
    output_filename = output_filename + "_not_AC_1"

if "-ac1" or "na1" not in sys.argv:
    print "Considering calls of all AC."

with open(input_VCF_filename, "r") as input_VCF, open(output_filename, "w") as output:
    records_found = []
    for count, line in enumerate(input_VCF):

        # print "reading line" , count

        if line.startswith('#CHROM'):
            keys = line.split("\t")
        if line.startswith("#"):
            continue

        split_line = line.split("\t")
        info_column = split_line[7]
        VCF_dict = dict(zip(keys, split_line))
        info_dict = {}

        for variable in VCF_dict['INFO'].split(';'):
            try:
                data = variable.split('=')
                info_dict[data[0]] = data[1]
            except:
                continue

        VCF_dict['INFO_DATA'] = info_dict
        # print VCF_dict['INFO_DATA'].keys()

        record_match = True

        all_conditions_tested = False
        while record_match and not all_conditions_tested:

            if 'MinorAlleleFreq' in VCF_dict['INFO_DATA'].keys():
                print "MAF found, line num", count
            else:
                VCF_dict['INFO_DATA']['MinorAlleleFreq'] = 0

            if "-r" in sys.argv:
                if 'Repeats' in VCF_dict['INFO_DATA'].keys():
                    print "repeats found, line num", count
                else:
                    record_match = False
                    break

            if "-nr" in sys.argv:
                if 'Repeats' not in VCF_dict['INFO_DATA'].keys():
                    print "repeats not found, line num", count
                else:
                    record_match = False
                    break

            if "-sd" in sys.argv:
                if 'Segdup' in VCF_dict['INFO_DATA'].keys():
                    print "Segdup found, line num", count
                else:
                    record_match = False
                    break

            if "-ns" in sys.argv:
                if 'Segdup' not in VCF_dict['INFO_DATA'].keys():
                    print "Segdup not found, line num", count
                else:
                    record_match = False
                    break

            if "-he" in sys.argv:
                genotype_column = split_line[9]
                het = re.search('^0/1', genotype_column)
                if het:
                    print "het found, line num", count
                else:
                    record_match = False
                    break

            if "-ho" in sys.argv:
                genotype_column = split_line[9]
                hom_ones = re.search('^1/1', genotype_column)
                hom_zeros = re.search('^0/0', genotype_column)
                if hom_ones or hom_zeros:
                    print "hom found, line num", count
                else:
                    record_match = False
                    break

            if "-nm" in sys.argv:
                if "," not in VCF_dict['ALT']:
                    print "not MA, line num", count
                else:
                    record_match = False
                    break

            if "-ma" in sys.argv:
                if "," in VCF_dict['ALT']:
                    print "MA, line num", count
                else:
                    record_match = False
                    break

            if "-ac1" in sys.argv:
                if 'AC' in VCF_dict['INFO_DATA'].keys():
                    if int(VCF_dict['INFO_DATA']['AC']) == 1:
                        print "AC=1, line num", count
                    else:
                        record_match = False
                        break

            if "-na1" in sys.argv:
                if 'AC' in VCF_dict['INFO_DATA'].keys():
                    if int(VCF_dict['INFO_DATA']['AC']) != 1:
                        print "AC is not 1, line num", count
                    else:
                        record_match = False
                        break

            all_conditions_tested = True

            if record_match:
                records_found.append(VCF_dict)
                # print "number of records" , len(records_found)
    for VCF_record in records_found:
        maf_value = 0
        print VCF_record['INFO_DATA']['MinorAlleleFreq']
        if VCF_record['INFO_DATA']['MinorAlleleFreq'] != 0:
            maf_value = VCF_record['INFO_DATA']['MinorAlleleFreq'].split(",")[7]
            output.write("%s\t%s\n" % (VCF_record['INFO_DATA']['CADDscaledScore'], maf_value))
        # print VCF_record['INFO_DATA']['CADDscaledScore'], "\t", maf_value
        else:
            output.write("%s\t%s\n" % (VCF_record['INFO_DATA']['CADDscaledScore'], maf_value))