# - states and regions - #

# northeast
northeast = "Northeast"
ls_new_england = ["CT", "ME", "NH", "RI", "VT"]
ls_midatlantic = ["NJ", "NY", "PA"]
ls_northeast = ls_new_england + ls_midatlantic

# midwest
midwest = "Midwest"
ls_midwest_eastnorth = ["IL", "IN", "MI", "OH", "WI"]
ls_midwest_westnorth = ["IA", "KS", "MN", "MS", "NE", "ND", "SD"]
ls_midwest = ls_midwest_eastnorth + ls_midwest_westnorth

# south
south = "South"
ls_south_atlantic   = ["DE", "FL", "GA", "MD", "NC", "SC", "VA", "DC", "WV"]
ls_south_east       = ["AL", "KY", "MS", "TN"]
ls_south_west       = ["AR", "LA", "OK", "TX"]
ls_south = ls_south_atlantic + ls_south_east + ls_south_west

# west
west = "West"
ls_west_mountain = ["AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY"]
ls_west_pacific  = ["AK", "CA", "HI", "OR", "WA"]
ls_west = ls_west_mountain + ls_west_pacific

# all
ls_all_states = ls_northeast + ls_midwest + ls_south + ls_west


# - functions - #

def get_state(citystate):
    """return two character state code from 'city, NY' string"""
    stateCode =  citystate.split(", ", 1)[1]
    return None if stateCode not in ls_all_states else stateCode


def get_region(state):
    """return a curated 'region' code given state ISO"""
    if state in ls_northeast:
        return northeast
    elif state in ls_midwest:
        return midwest
    elif state in ls_south:
        return south
    elif state in ls_west:
        return west
    else:
        return None
