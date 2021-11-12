# VCF - Call Rate Filter

The utility of this pythons script is to filter variants or samples out of a VCF based on the call rate of the genotypes.

Example: 
A VCF has 100 samples. There are 10000 variants in the VCF with genotypes for every sample.
The script counts the number of genotype calls and no calls present in the genotypes and then calculates call rate as follows

Call Rate = No. of called genotypes (0/0, 0/1, 0/2, 1/2, etc and not ./.) / Total number of genotyes (2 x number of samples)

Based on the user provided cutoff, a variant or sample will be filtered out if the call rate is less than the user input.

By default the program will filter variants, but if the --by-samples arguement is passed then the program will filter out samples.

Usage:

python vcf_callratecheck.py input.vcf cutoff [--by-samples]

Output:
The script creates a VCF file with variants that passed the thresold and a log file in the format of a VCF with variants that failed to pass the thresold.
