"""
:author: Aidan Sawyer
:date: 2016-11-22
:name: Data Object
:description: data object for a single entry
"""

# imports
from locations import get_state, get_region
from styles import get_style12, get_style05

# data
lsBeers = []


# class definition
class Beer:
    def __init__(self, name, brewery, location, style, size, abv, ibu):
        self.name = name.rstrip()
        self.brewery = brewery.rstrip()
        self.location_state = get_state(location)
        self.location_region = get_region(get_state(location))
        self.style12 = get_style12(style)
        self.style05 = get_style05(get_style12(style))
        self.size = clean_size(size)
        self.abv = abv.replace("%", "")
        self.ibu = None if ibu == "N/A" else int(ibu)

    def getData(self):
        return [self.name, self.brewery, self.location_state, self.location_region,
                self.style12, self.style05, self.size, self.abv, self.ibu]


# - helpers - #

def getHeader():
    """return the list of attributes for a given 'Beer'"""
    return ["Beer", "Brewery", "State", "Region", "Style_12", "Style_05",
            "Size", "ABV", "IBU"]


def clean_size(size):
    """clean 'size' attribute by removing 'oz.' and other bare text"""
    if "16" in size:
        return "16"
    elif "12" in size:
        return "12"
    else:
        return None
