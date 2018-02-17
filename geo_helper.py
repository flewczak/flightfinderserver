from geopy.distance import vincenty


# calculate distance between two coordinates of points
def calc_distance(latitude1, longitude1, latitude2, longitude2):
    newport_ri = (latitude1, longitude1)
    cleveland_oh = (latitude2, longitude2)
    out = vincenty(newport_ri, cleveland_oh)
    return out


class ShortestPaths:
    def __init__(self, weigh_list, airports_list, airline_list):
        self.weigh_list = weigh_list
        self.airports_list = airports_list
        self.airline_list = airline_list
