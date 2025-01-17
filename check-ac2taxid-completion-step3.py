"""
This script is the third of three scripts that checks if all seqAcs in nt file have taxIds from nucl_gb.accession2taxid
file, and the ones do not have taxIds are checked in all other ac2taxid files.

Input
^^^^^
All inputs are currenlty hard-coded.
- `patList`: path for ../nucl_*.accession2taxid.DATE
- `ntFile`: path for new ntFile generated from check-ac2taxid-completion-step2.py ../logfile.step2.txt

Output
^^^^^^
All outputs are currently hard-coded.
- The `logfile.step3.txt` is generated.

Usage
^^^^^
- Currently no options available. 
"""
from optparse import OptionParser
import glob
import csv


__version__="1.0"
__status__ = "Dev"



###############################
def main():


	patList = "/data/projects/targetdbs/filtered-nt/downloads/ac2taxid.2017-05-30/*"
	fileList = glob.glob(patList)
	ntFile = "/data/projects/targetdbs/filtered-nt/downloads/logfile.step2.txt"
	passFile = ['nucl_wgs.accession2taxid', 'nucl_est.accession2taxid', 'nucl_gb.accession2taxid','nucl_gss.accession2taxid']


	seqAcDic = {}
	with open(ntFile, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=':', quotechar='|')
		for row in csvreader:
			seqAc = row[1].strip()
			seqAcDic[seqAc] = 1
	
	FW = open("/data/projects/targetdbs/filtered-nt/downloads/logfile.step3.txt", "w")
	ac2taxid = {}
	for fileName in fileList:
		i = 0
		if fileName.split('/')[-1] not in passFile:
			with open(fileName, 'rb') as csvfile:
					csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
					for row in csvreader:
							seqAc = row[0].strip()
					if seqAc in seqAcDic:
						seqAcDic[seqAc] = 2
					if seqAc+seqAc[-1] in seqAcDic and fileName.find("pdb.accession2taxid") >= 0:
						seqAcDic[seqAc+seqAc[-1]] = 2
					if i%10000000 == 0:
						print("Data reading ", fileName, i)
					i += 1

	for key,val in seqAcDic.items():
		if val == 1:
			FW.write("No taxid found for: %s\n" % (key))

	FW.close()

if __name__ == '__main__':
        main()

