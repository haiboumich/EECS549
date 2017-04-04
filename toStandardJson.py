# the original file got from Yelp is not a standard json file, need to be changed
# it just add comma at each line, still need manually change sth

import sys

if len(sys.argv) < 3:
	print('Usage:')
	print(' python %s <Input file> <Output file>' % sys.argv[0])
	exit()

inputFile = open(sys.argv[1], 'r')
outputFile = open(sys.argv[2], 'w')

for line in inputFile:
	line += ','
	print(line, file=outputFile)