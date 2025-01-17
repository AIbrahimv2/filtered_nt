"""

"""

from optparse import OptionParser
from Bio import SeqIO
import csv


__version__="1.0"
__status__ = "Dev"



###############################
def main():


	ntFile = "/data/projects/targetdbs/filtered-nt/downloads/nt.2017-05-21"
	ac2taxidFile = '/data/projects/targetdbs/filtered-nt/generated/logfile.ac2taxid.list.txt'
	ac2taxidFile2 = '/data/projects/targetdbs/filtered-nt/generated/logfile.step3.manually.added.txt'
	blackFile = '/data/projects/targetdbs/filtered-nt/generated/blacklist-taxId.1.and.2.unique.csv'
	fw = "/data/projects/targetdbs/filtered-nt/generated/filtered_nt_test.fasta"

	blackList = {}
	with open(blackFile, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csvreader:
			blackList[row[0]] = 1
	blackList['NA'] = 1
	print(len(blackList))

	ac2taxid = {}
	with open(ac2taxidFile, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csvreader:
			seqAc = row[0].strip().upper()
			taxId = row[1].strip().upper()
			if not taxId in blackList:
				ac2taxid[seqAc] = 1

	with open(ac2taxidFile2, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
		for row in csvreader:
			seqAc = row[0].strip().upper()
			taxId = row[1].strip().upper()
		if not taxId in blackList:
				ac2taxid[seqAc] = 1
	print(len(ac2taxid))

	i = 0
	for record in SeqIO.parse(ntFile, "fasta"):
		seqAc = record.id
		seqAc = seqAc.split('.')[0].upper()
		seqName = record.description
		seqName = ' '.join(seqName.split()[1::])
		if seqAc in ac2taxid:
			with open(fw, "w") as FW: 
				FW.write(">%s|%s\n%s\n" % (seqAc, seqName, record.seq))
		if i%10000000 == 0:
			print("Done loading ", i)
		i += 1


if __name__ == '__main__':
        main()

