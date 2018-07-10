import argparse, csv, itertools, os, pandas as pd, matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Find possible domains that use the tld in the name')
parser.add_argument('--input', '-i', default='input.csv', type=argparse.FileType('r'), help="file to import, defaults to input.csv")
parser.add_argument('--format', '-f', type=argparse.FileType('w'), help="reformats results by module and exports it to file specified")
parser.add_argument('--plot', '-p', action='store_true', help="plot the module results (note if you don't specify --exportplots or --showplots nothing will happen with the plots)")
parser.add_argument('--exportplots', '-ep', help="export all plots to /path/you/want/")
parser.add_argument('--showplots', '-sp',action='store_true', help="show all plots")
parser.add_argument('--my', '-m', help="returns your weighted average for the year (need to specify your candidate number)")
parser.add_argument('--year', '-y', help="specify your year")
parser.add_argument('--rank', '-r', action='store_true', help="returns your rank in the year")
args = parser.parse_args()


badFormat = {row[0]:row[1:] for row in csv.reader(args.input, delimiter=',')} # create a list from every row
length = int(len(badFormat['Cand'])/2)


def goodFormater(outputPath):
    '''[summary]
    
    reformats the input results into a dictionary with module names as keys and their respective results as values

    outputs to csv if outputPath is specified
    
    Arguments:
        outputPath {str} -- the path to output to
    
    Returns:
        dictionary -- module : [results for module]
        saves to file if output path is specified

    '''
        
    devcom = 'PHAS' + badFormat['Cand'][0]
    
    goodFormat = {devcom: []}
    

    for row in list(badFormat.values())[1:]: #ignore first row cause it's just 'Mark' & 'ModuleN'
        goodFormat[devcom].append(int(row[0])) #add first val to devcom
    
        for i in range(length-1):
            goodFormat.setdefault(row[(2 * i) + 1], []) #if a key for that module doesn't exist, initialize with empt array
            goodFormat[row[(2*i)+1]].append(int(row[2*(i +1)])) #add value of module to module
    
    goodFormat.pop('0')

    goodFormat['Averages'] = everyonesAverage(args.year)
    if outputPath is not None: #if requested to reformat and save to file

        results = csv.writer(outputPath,delimiter=',')
        results.writerow(goodFormat.keys()) # write the keys (module names) as first row
        #zip module results together, fill modules with less people using empty values
        #add row by row
        results.writerows(itertools.zip_longest(*goodFormat.values(), fillvalue=''))

    return goodFormat

def plotter(path, show):
    '''makes some plots
        
    creates binned histograms of the results of each module
    (ie count of results in ranges [(0,40), (40, 50), (50,60), (60, 70), (70, 80), (80, 90), (90, 100)])

    Arguments:
        path {str} --  path to save plots to
        show {boolean} -- whether to show plots using python

    output:
        saves plots to files/shows plots depending on inputs
    '''

    goodFormat = goodFormater(args.format) #goodFormat the results first


    for module in goodFormat.items(): #for each module
        bins = [0,40,50,60,70,80,90,100] 
        out = pd.cut(module[1], bins=bins, include_lowest=True) # cut the data into bins
        ax = out.value_counts().plot.bar(rot=0, color="b", figsize=(10,6), alpha=0.5, title=module[0]) #plot counts of the cut data as a bar

        ax.set_xticklabels(['0 to 40', '40 to 50', '50 to 60', '60 to 70', '70 to 80', '80 to 90','90 to 100'])

        ax.set_ylabel("# of candidates")
        ax.set_xlabel("grade bins \n total candidates: {}".format(len(module[1])))


        if path is not None and show is not False:

            exportPath = path + '/' if path[-1] is not '/' else path
            
            if not os.path.isdir(exportPath): #if export path directory doesn't exist: create it
                os.makedirs(exportPath)
            
            plt.savefig(exportPath + module[0] + '.png')
            plt.show()

        elif path is not None:

            exportPath = path + '/' if path[-1] is not '/' else path

            if not os.path.isdir(exportPath): #if export path directory doesn't exist: create it
                os.makedirs(exportPath)
            
            plt.savefig(exportPath + module[0] + '.png')
            plt.close()

        elif show is not False:
            plt.show()


def myGrades(year, candidateNumber):
    '''returns final result of candidateNumber in year
    
    Arguments:
        year {str} -- the year candidateNumber is in
        candidateNumber {str} -- the candidateNumber of candidateNumber
    
    Returns:
        int -- a weighted average for a specific candidate number and year
    '''

    weights1 = [1,1,1,1,0.5,0.5,0.5,0.5]
    weights2 = [1,1,1,1,1,1,0.5,0.5]
    if year == '1':
        myFinalResult = sum([int(badFormat[candidateNumber][2*(i + 1)]) * weights1[i] for i in range(length-1)]) / 6
    elif year == '2' or year == '3':
        myFinalResult = sum([int(badFormat[candidateNumber][2*(i + 1)]) * weights2[i] for i in range(length-1)]) / 7
    elif year == '4':
        myFinalResult = sum([int(badFormat[candidateNumber][2*(i + 1)]) for i in range(length-1)]) / 8

    return myFinalResult


def myRank(year, candidateNumber):
    '''rank of candidateNumber in year
        
    Arguments:
        year {str} -- the year candidateNumber is in
        candidateNumber {str} -- the candidateNumber of candidateNumber

    Returns:
        int -- rank of candidateNumber in year
    '''
    return sorted(everyonesAverage(year), reverse=True).index(myGrades(year, candidateNumber)) + 1

def everyonesAverage(year):
    ''' creates list of weighted average results for everyone in year
    
    Arguments:
        year {str}

    returns:
        list -- weighted average results of everyone in year
    '''
    return [myGrades(year, cand) for cand in list(badFormat.keys())[1:]]


if args.plot is not None:
    plotter(args.exportplots, args.showplots)
elif args.format is not None:
    goodFormater(args.format)

if args.my is not None and args.year is not None:
    print('Your weighted average for the year is: {:.2f}%'.format(myGrades(args.year, args.my)))



if args.rank is not False:
    r = int(myRank(args.year, args.my))
    print('{}th of {} ({:.2f} percentile)'.format(r, 161, (r * 100) / 161))


if not len(sys.argv) > 1:
    #if no args get input from user
    pass

