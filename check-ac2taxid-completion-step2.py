"""
This script is the second of three scripts that checks if all seqAcs in nt file have taxIds from nucl_gb.accession2taxid
file, and the ones do not have taxIds are checked in all other ac2taxid files.

Input
^^^^^
All inputs are currenlty hard-coded.
- `patList`: path for ../nucl_*.accession2taxid.DATE
- `ntFile`: path for new ntFile generated from check-ac2taxid-completion-step1.py ../logfile.step1.txt

Output
^^^^^^
All outputs are currently hard-coded.
- The `logfile.step2.txt` is generated.

Usage
^^^^^
- Currently no options available. 
"""
from optparse import OptionParser
from Bio import SeqIO
import glob
import csv


__version__="1.0"
__status__ = "Dev"



###############################
def main():


	patList = "/data/projects/targetdbs/filtered-nt/downloads/nucl_*.accession2taxid.2017-05-21"
    
	fileList = glob.glob(patList)
	
	ntFile = "/data/projects/targetdbs/filtered-nt/generated/logfile.step1.txt"


	seqAcDic = {}
	with open(ntFile, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=':', quotechar='|')
		for row in csvreader:
			seqAc = row[1].strip()
			seqAcDic[seqAc] = 1
	
	FW = open("/data/projects/targetdbs/filtered-nt/generated/logfile.step2.txt", "w")
	ac2taxid = {}
	for fileName in fileList:
		if fileName.find("nucl_gb.accession2taxid") == -1:
			i = 0
			with open(fileName, 'rb') as csvfile:
				csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
				for row in csvreader:
					seqAc = row[0].strip()
					if seqAc in seqAcDic:
						seqAcDic[seqAc] = 2
					if i%10000000 == 0:
						print("Data reading ", fileName, i)
					i += 1

	for key,val in seqAcDic.items():
		if val == 1:
			FW.write("No taxid found for: %s\n" % (key))

	FW.close()

if __name__ == '__main__':
        main()

