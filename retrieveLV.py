import json
import sys

if len(sys.argv) < 3:
	print('Usage:')
	print(' python %s <Input file> <Output file>' % sys.argv[0])
	exit()

inputFileName = sys.argv[1];
outputFileName = sys.argv[2];

with open(inputFileName, 'r') as inputFile:
	json_decode = json.load(inputFile)

	data = []
	for item in json_decode:

		if item.get('city') == 'Las Vegas' and item.get('categories') and 'Restaurants' in item.get('categories'):
			data.append(item)

	with open(outputFileName, 'w') as outputFile:
		json.dump(data, outputFile)

# just for check
with open(inputFileName, 'r') as inputFile:
	json_decode = json.load(inputFile)
	i = 0
	for item in json_decode:
		i += 1
	print('items in input file:')
	print(i)

with open(outputFileName, 'r') as inputFile:
	json_decode = json.load(inputFile)
	i = 0
	for item in json_decode:
		i += 1
	print('items in output file:')
	print(i)