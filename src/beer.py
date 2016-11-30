"""
:author: Aidan Sawyer
:date: 2016-11-22
:name: Data Object
:description: data object for a single entry
"""

# imports
import re
from locations import get_state, get_region
from styles import get_style12, get_style05

# data
lsBeers = []


# class definition
class Beer:
    def __init__(self, name, brewery, location, style, size, abv, ibu):
        self.name = cleanAlphaNumeric(name).rstrip()
        self.brewery = cleanAlphaNumeric(brewery)
        self.location_state = get_state(location)
        self.location_region = get_region(get_state(location))
        self.style = cleanAlphaNumeric(style)
        self.style12 = get_style12(style)
        self.style05 = get_style05(get_style12(style))
        self.size = clean_size(size)
        self.abv = cleanABV(abv)
        self.ibu = None if ibu == "N/A" else int(ibu)
        self.abv_norm = None

    def getData(self):
        return [self.name, self.brewery, self.location_state, self.location_region,
                self.style, self.style12, self.style05, self.size, self.abv, self.ibu]
                #,self.abv_norm]


# - helpers - #

def getHeader():
    """return the list of attributes for a given 'Beer'"""
    return ["Beer", "Brewery", "State", "Region", "Style_RAW", "Style_12", "Style_05",
            "Size", "ABV", "IBU"] #, "ABV_Norm"]


def clean_size(size):
    """clean 'size' attribute by removing 'oz.' and other bare text"""
    if "16" in size:
        return "16"
    elif "12" in size:
        return "12"
    else:
        return None


def cleanABV(abv):
    """take an unformatted string and convert it to a digit"""
    txt_clean = re.sub("[^0-9]", "", abv)
    return float(txt_clean)/10.0 if txt_clean != "" else None


def cleanAlphaNumeric(str):
    """remove non-alphanumeric characters to sanitize export file"""
    txt_clean = re.sub(r'[^a-zA-Z0-9\s]', '', str)
    return txt_clean if txt_clean != "" else None
