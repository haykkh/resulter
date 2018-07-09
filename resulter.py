import argparse, csv, itertools

parser = argparse.ArgumentParser(description='Find possible domains that use the tld in the name')
parser.add_argument('--input', '-i', default='input.csv', type=argparse.FileType('r'), help="file to import, defaults to input.csv")
parser.add_argument('--format', '-f', default=None, type=argparse.FileType('w'), help="reformats results by module and exports it to file specified")
parser.add_argument('--graph', '-g', default=None )

args = parser.parse_args()


badFormat = [row[1:] for row in csv.reader(args.input, delimiter=',')] # create a list from every row, drop first val (candidate number)

def goodFormater():
	''' 
	
	creates a csv where each modules results are grouped together, and returns this dictionary
	
	'''
	
	results = csv.writer(args.format,delimiter=',')
	
	devcom = 'PHAS' + badFormat[0][0]
	
	goodFormat = {devcom: []}
	
	length = int(len(badFormat[0])/2)

	for row in badFormat[1:]: #ignore first row cause it's just 'Mark' & 'ModuleN'
		goodFormat[devcom].append(int(row[0])) #add first val to devcom
	
		for i in range(length-1):
			goodFormat.setdefault(row[(2 * i) + 1], []) #if a key for that module doesn't exist, initialize with empt array
			goodFormat[row[(2*i)+1]].append(int(row[2*(i+1)])) #add value of module to module
	
	results.writerow(goodFormat.keys()) # write the keys (module names) as first row
	#zip module results together, fill modules with less people using empty values
	#add row by row
	results.writerows(itertools.zip_longest(*goodFormat.values(), fillvalue=''))

	return goodFormat

def grapher():
	import pandas as pd
	goodFormat = goodFormater()

	for module in goodFormat.items():
		res = pd.DataFrame(module[1])
		out = pd.cut(module[1], bins=[0, 40, 50, 60, 70, 80, 90, 100], include_lowest=True)
		
		# see https://stackoverflow.com/questions/43005462/pandas-bar-plot-with-binned-range to finish
		ax = out.value_counts().plot.bar(rot=0, color="b", figsize=(6,4))
		ax.set_xticklabels([c[1:-1].replace(","," to") for c in out.cat.categories])
		plt.show()





if args.format != None:
	goodFormater()

grapher()