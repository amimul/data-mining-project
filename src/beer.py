"""
:author: Aidan Sawyer
:date: 2016-11-22
:name: Data Object
:description: data object for a single entry
"""

# imports
from locations import get_state, get_region
from styles import get_style12, get_style05


# class definition
class Beer:
    def __init__(self, bid, name, brewery, location, style, size, abv, ibu):
        self.id = bid
        self.name = name.rstrip()
        self.brewery = brewery.rstrip()
        self.location_state = get_state(location)
        self.location_region = get_region(self.state)
        self.style12 = get_style12(style)
        self.style05 = get_style05(self.style12)
        self.size = clean_size(size)
        self.abv = abv.replace("%", "")
        self.ibu = None if ibu == "N/A" else int(ibu)


# - helpers - #
def clean_size(size):
    """clean """
    if "16" in size:
        return "16"
    elif "12" in size:
        return "12"
    else:
        return None


def exportToCSV(lsBeers):
    """export data into a csv file"""
    pass
