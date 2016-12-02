"""
:author: Aidan Sawyer
:date: 2016-11-28
:name: Main
:description: ingest, parse, edit, export csv
"""

# import csv, sys, and beer libraries
import csv, sys

import styles
from beer import Beer, getHeader

# list of beers
lsBeers = []

# metrics used in filters and normalizations
max_ibu = 99999  # practically infinite
max_abv = 0
num_ipa = 0
lsIPA  = styles.ipa_ls
num_pale = 0
lsPale  = styles.pale_ls

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
    global lsPale, lsIPA, num_ipa, num_pale

    with open(filename, "w") as csv_out:
        beer_data_out = csv.writer(csv_out)
        beer_data_out.writerow(getHeader())

        num_total = 0
        num_left = 0
        toNormalize = []
        for beer in lsBeers:
            num_total += 1

            # only include beers with all information
            if matchFilters(beer):
                pass
            else:

                # update beer statistics
                global max_abv, max_ibu
                if beer.abv is not None:
                    max_abv = beer.abv if beer.abv > max_abv else max_abv
                if beer.ibu is not None:
                    max_ibu = beer.ibu if beer.ibu > max_ibu else max_ibu

                # update count of pale and ipa beers
                if beer.style12 == styles.pale:
                    num_pale += 1

                if beer.style12 == styles.ipa:
                    num_ipa += 1

                #print("num pale: " + str(num_pale) + " | num ipa: " + str(num_ipa))

                # add known beer to list to normalize and write out
                toNormalize.append(beer)
                num_left += 1

        # export the selected, normalized, known beers
        for beer in toNormalize:
            normalizeMetrics(beer)
            beer_data_out.writerow(beer.getData())

        discard = num_total - num_left
        print("total: " + str(num_total) + " | left: " + str(num_left))
        print("discarded: " + str(discard) + " | " + str((discard*100.0)/num_total) + "%")


# - beer filters - #

def matchFilters(beer):
    """dynamic function meant to handle which filters are currently being used"""
    lsFilters = [matchFilterEmptyValues(beer), matchFilterNotPaleOrStrong(beer)]
    return True in lsFilters


def matchFilterStylesMetrics(beer):
    """filter out values with 'None' in the style12,05, abv, or ibu fields"""
    return beer.style12 is None or beer.style05 is None or beer.abv is None or beer.ibu is None


def matchFilterEmptyValues(beer):
    """filter out any value with an empty field"""
    return None in beer.getData()


def matchFilterBeerIPACap(beer):
    """ensure the number of IPAs added to the data set is under 100"""
    global num_ipa, lsIPA
    return (beer.style12 in lsIPA) and num_ipa >=100


def matchFilterBeerPaleCap(beer):
    """ensure the number of Pale Ales added to the data set is under 100"""
    global num_pale, lsPale
    return (beer.style12 in lsPale) and num_pale >=100


def matchFilterStyleOther(beer):
    """catch beers in the 'other' category"""
    return beer.style12 is None or beer.style12 in styles.etc_ls


def matchFilterStyleAleOther(beer):
    """catch beers in the 'ale - other' category"""
    return beer.style12 in styles.ale_ls


def matchFilterStyleSour(beer):
    """catch beers in the 'sour' category """
    return beer.style12 in styles.sour_ls


def matchFilterNotPaleOrStrong(beer):
    """catch beers not in the 'Ale', 'Strong' """
    return beer.style05 not in [styles.ALE, styles.STRONG]

# - helpers - #

def normalizeMetrics(beer):
    """normalize beer metrics to float [0,1]"""
    beer.abv_norm = (beer.abv * 1.0) / max_abv if beer.abv is not None else None
    # beer.ibu_norm = ((1+beer.ibu) * 1.0) / (1+max_ibu) if beer.ibu is not None else None


if __name__ == "__main__":
    main()
