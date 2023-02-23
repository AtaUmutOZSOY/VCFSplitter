import os
import re

class VCFChromSplitter:
    def __init__(self, input_vcf_path,output_path):
        self.input_vcf_path = input_vcf_path
        self.output_path = output_path
        self.chrom_files = {}

        with open(self.input_vcf_path, 'r') as vcf:
            for line in vcf:
                if line.startswith('#'):
                    # Write header lines to all chromosome files
                    for chrom_file in self.chrom_files.values():
                        chrom_file.write(line)
                else:
                    # Extract the chromosome from the line
                    chrom_match = re.search(r'^(\w+)\t', line)
                    chrom = chrom_match.group(1)

                    # If this is the first variant for this chromosome, create a new file
                    if chrom not in self.chrom_files:
                        output_vcf_path = os.path.splitext(output_path)[0] + os.path.basename(input_vcf_path)+ f'.{chrom}.vcf'
                        self.chrom_files[chrom] = open(output_vcf_path, 'w')

                    # Write the variant to the appropriate chromosome file
                    self.chrom_files[chrom].write(line)

        # Close all chromosome files
        for chrom_file in self.chrom_files.values():
            chrom_file.close()
