"""
:author: Aidan Sawyer
:date: 2016-11-28
:name: Main
:description: ingest, parse, edit, export csv
"""

# import csv, sys, and beer libraries
import csv, sys
from beer import Beer, getHeader

# list of beers
lsBeers = []

# index for each attribute value
NAME     = 1
BREWERY  = 2
LOCATION = 3
STYLE    = 4
SIZE     = 5
ABV      = 6
IBU      = 7


# - import/export - #

def main():
    fileInput = "input.csv"
    fileOutput = "data_beer.csv"

    # set input/output files
    lsArgs = sys.argv
    if len(lsArgs) < 1:
        print("Please provide input and output file names")
    elif len(lsArgs) == 1:
        fileInput = lsArgs[1]
    else:
        fileInput = lsArgs[1]
        fileOutput = lsArgs[2]

    #print(lsArgs)
    #print("input: " + fileInput)
    #print("output: " + fileOutput)

    # run ingest/output with those files
    ingest(fileInput)
    export(fileOutput)


def ingest(filename):
    """create a list of beers from data from a csv"""
    with open(filename) as csv_in:
        beer_data_in = csv.reader(csv_in, delimiter=',')
        isHeader = True
        for row in beer_data_in:
            if not isHeader:
                lsBeers.append( Beer(row[NAME], row[BREWERY], row[LOCATION], row[STYLE], row[SIZE], row[ABV], row[IBU]) )
            else:
                isHeader = False
    pass


def export(filename):
    """write data from the `lsBeers` list"""
    with open(filename, "w") as csv_out:
        beer_data_out = csv.writer(csv_out)

        beer_data_out.writerow(getHeader())

        num_total = 0
        num_left = 0
        for beer in lsBeers:
            num_total += 1
            beerData = beer.getData()

            # only include beers with all information
            if None not in beerData:
                beer_data_out.writerow(beer.getData())
                num_left += 1

        discard = num_total - num_left
        print("total: " + str(num_total) + " | left: " + str(num_left))
        print("discarded: " + str(discard) + " | " + str((discard*1.0)/num_total) + "%")

if __name__ == "__main__":
    main()
