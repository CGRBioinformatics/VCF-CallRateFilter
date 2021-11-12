import os,sys

'''
python vcf_callratecheck.py input.vcf cutoff [--by-sample]
'''

bySample = False
argCount = 0         # Counts the number of required arguments that have been parsed
for ar in sys.argv:
	if argCount == 0:
		argCount += 1
	elif ar == "--by-sample":
		bySample = True
	elif argCount == 1:
		argCount += 1
		ivcf = ar
	elif argCount == 2:
		argCount += 1
		ival = ar

opvtag="_CR"+str(ival)+".vcf"
opltag="_CR"+str(ival)+".log"

opvcf=ivcf.replace(".vcf",opvtag)
oplog=ivcf.replace(".vcf",opltag)

ovcf=open(str(opvcf),'w')
olog=open(str(oplog),'w')

#print(ivcf,ovcf)
if not bySample:
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
else:
	for line in open(os.path.expanduser(ivcf), 'r'):
		if "##" in line:
			continue
		elif '#' in line:
			arr = line.split("\t")
			firstSampleIndex = 0       # This gets the index of the first sample, since the FORMAT and INFO headers can sometimes be missing
			while firstSampleIndex < 7 or arr[firstSampleIndex] == "FORMAT" or arr[firstSampleIndex] == "INFO":
				firstSampleIndex += 1
			numSamples = len(arr) - firstSampleIndex
			nocalls = [0] * numSamples
			totalVariants = 0
		else:
			arr = line.strip().split("\t")
			ind = 0
			for s in arr[firstSampleIndex:]:
				if s.split(":")[0] == "./.":
					nocalls[ind] += 1
				ind += 1
			totalVariants += 1
	keepIndices = []
	removedPatients = 0
	for i in range(firstSampleIndex, numSamples + firstSampleIndex):
		if float(float(totalVariants - nocalls[i - firstSampleIndex]) / float(totalVariants)) >= float(float(ival) / float(100)):
			keepIndices.append(i)
		else:
			removedPatients += 1
	for line in open(os.path.expanduser(ivcf), 'r'):
		if "##" in line:
			ovcf.write(line)
			olog.write(line)
		else:
			arr = line.strip().split("\t")
			i = 0
			for s in arr:
				if i == 0:
					ovcf.write(s)
					olog.write(s)
				elif i < firstSampleIndex:
					ovcf.write("\t" + s)
					olog.write("\t" + s)
				elif i in keepIndices:
					ovcf.write("\t" + s)
				else:
					olog.write("\t" + s)
				i += 1
			ovcf.write("\n")
			olog.write("\n")
	print(str(removedPatients) + " out of the " + str(numSamples) + " samples were filtered for having a call rate of lower than " + str(ival) + "%")
