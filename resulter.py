import csv, sys, itertools

PHAS1202 = []
PHAS1224 = []
PHAS1228 = []
PHAS1240 = []
PHAS1241 = []
PHAS1245 = []
PHAS1246 = []
PHAS1247 = []

read = csv.DictReader(open('results.csv'))

data = list(read)

print(data)


cand = 0
while cand < len(data):
	mod = 1
	while mod < 9:
		module = 'module' + str(mod)
		mark = 'mark' + str(mod)
		if data[cand][module] == 'PHAS1202':
			PHAS1202.append(data[cand][mark])
		elif data[cand][module] == 'PHAS1224':
			PHAS1224.append(data[cand][mark])
		elif data[cand][module] == 'PHAS1228':
			PHAS1228.append(data[cand][mark])
		elif data[cand][module] == 'PHAS1240':
			PHAS1240.append(data[cand][mark])
		elif data[cand][module] == 'PHAS1241':
			PHAS1241.append(data[cand][mark])
		elif data[cand][module] == 'PHAS1245':
			PHAS1245.append(data[cand][mark])
		elif data[cand][module] == 'PHAS1246':
			PHAS1246.append(data[cand][mark])
		elif data[cand][module] == 'PHAS1247':
			PHAS1247.append(data[cand][mark])

		mod += 1

	cand += 1

zipped = itertools.zip_longest(PHAS1202, PHAS1224, PHAS1228, PHAS1240, PHAS1241, PHAS1245, PHAS1246, PHAS1247)

resultswrite = csv.writer(open('modules.csv', 'w'), quoting=csv.QUOTE_ALL, delimiter=",")
resultswrite.writerow(["PHAS1202", "PHAS1224", "PHAS1228", "PHAS1240", "PHAS1241", "PHAS1245", "PHAS1246", "PHAS1247"])
for row in zipped:
	resultswrite.writerow(row)




