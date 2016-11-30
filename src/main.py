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
max_ibu = 99999  # practically infinite
max_abv = 0

# index for each attribute value
NAME     = 1
BREWERY  = 2
LOCATION = 3
STYLE    = 4
SIZE     = 5
ABV      = 6
IBU      = 7
ABV_NORM = 8
IBU_NORM = 9


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
                # create beer
                beer = Beer(row[NAME], row[BREWERY], row[LOCATION], row[STYLE], row[SIZE], row[ABV], row[IBU])

                # add beer to list of beers
                lsBeers.append(beer)
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
        toNormalize = []
        for beer in lsBeers:
            num_total += 1

            print(beer.getData())

            # only include beers with all information
            if None in beer.getData(): #beer.style12 is None or beer.style05 is None or beer.size is None or beer.abv is None or beer.ibu is None:
                pass
            else:

                # update beer statistics
                global max_abv, max_ibu
                if beer.abv is not None:
                    max_abv = beer.abv if beer.abv > max_abv else max_abv
                if beer.ibu is not None:
                    max_ibu = beer.ibu if beer.ibu > max_ibu else max_ibu

                toNormalize.append(beer)
                num_left += 1

        for beer in toNormalize:
            normalizeMetrics(beer)
            beer_data_out.writerow(beer.getData())

        discard = num_total - num_left
        print("total: " + str(num_total) + " | left: " + str(num_left))
        print("discarded: " + str(discard) + " | " + str((discard*1.0)/num_total) + "%")


# - helpers - #

def normalizeMetrics(beer):
    """normalize beer metrics to float [0,1]"""
    beer.abv_norm = (beer.abv * 1.0) / max_abv if beer.abv is not None else None
    #beer.ibu_norm = ((1+beer.ibu) * 1.0) / (1+max_ibu) if beer.ibu is not None else None


if __name__ == "__main__":
    main()
