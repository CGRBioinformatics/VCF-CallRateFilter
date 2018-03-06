import os,sys

'''
python vcf_callratecheck.py input.vcf cutoff
'''

ivcf=sys.argv[1]
ival=sys.argv[2]

opvtag="_CR"+str(ival)+".vcf"
opltag="_CR"+str(ival)+".log"

opvcf=ivcf.replace(".vcf",opvtag)
oplog=ivcf.replace(".vcf",opltag)

ovcf=open(str(opvcf),'w')
olog=open(str(oplog),'w')

#print(ivcf,ovcf)
for line in open(os.path.expanduser(ivcf),'r'):
	if "#" in line:
		ovcf.write(line)
		olog.write(line)
	else:
		totgt=0
		calls=0
		nocalls=0
		line=line.strip()
		arr=line.split("\t")
		for ni,i in enumerate(arr):
			if ni>8:
				totgt=totgt+1
				if str(i).split(":")[0]=="./.":
					nocalls=nocalls+1
				else:
					calls=calls+1
		if float(float(calls)/float(totgt)) >= float(float(ival)/float(100)):
			ovcf.write(line+"\n")
		else:
			olog.write(line+"\n")
