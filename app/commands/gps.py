from geopy.geocoders import Nominatim
from geopy import distance
import time
from sys import maxsize
import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import permutations
from typing import DefaultDict


# [Getting coordinates from address]


def get_coords_by_address(address: str):
    app = Nominatim(user_agent="pizza-drone")
    time.sleep(1)
    try:
        location = app.geocode(address)
        lon = float(location.longitude)
        lat = float(location.latitude)
        return [lat, lon]

    except:
        return get_coords_by_address(address)

# [Getting distance between two coordinates]


def get_distance_by_coords(coords1, coords2):
    miles = distance.geodesic(coords1, coords2).miles
    return miles

# [Getting distances between all coordinates]


def distances_from_coords(coords):
    coords_array = np.array(coords)
    dist_array = pdist(coords_array)
    dist_matrix = squareform(dist_array)
    # print(dist_matrix)
    return list(dist_matrix)


INT_MAX = 2147483647

# Greedy algo


def tsp(tsp):
    # distances = distances_from_coords(coords)
    # print(distances)
    path_cost = 0
    counter = 0
    j = 0
    i = 0
    minimum = INT_MAX
    visitedRouteList = DefaultDict(int)
    """ Starting from the 0th indexed
    address i.e., the first address """
    visitedRouteList[0] = 1
    route = [0] * len(tsp)
    """ Traverse the adjacenct
    matrix tsp[][] """
    while i < len(tsp) and j < len(tsp[i]):
        # Corner of the Matrix
        if counter >= len(tsp[i]) - 1:
            break
        """ If this path is unvisited
        and if the cost is less than minimum
        update the cost """
        if j != i and (visitedRouteList[j] == 0):
            if tsp[i][j] < minimum:
                minimum = tsp[i][j]
                route[counter] = j + 1

        j += 1
        # Check all paths from the ith indexed city
        if j == len(tsp[i]):
            path_cost += minimum
            minimum = INT_MAX
            visitedRouteList[route[counter] - 1] = 1
            j = 0
            i = route[counter] - 1
            counter += 1
    """ Update the ending address in array
    from last visited address """
    i = route[counter - 1] - 1
    for j in range(len(tsp)):
        if (i != j) and tsp[i][j] < minimum:
            minimum = tsp[i][j]
            route[counter] = j + 1

    path_cost += minimum
    print(path_cost)
    return route


def getNearestCity(distanceMatrix, cityId):
    i = 0
    for distanceList in distanceMatrix:
        if i == cityId:
            smallestDistance = min(idx for idx in distanceList if idx > 0)
            if smallestDistance > 9999 * 3:
                return -1, -1
            else:
                return smallestDistance, distanceList.index(smallestDistance)
        i += 1


def addCity(pathArray, citiesToVisit, distanceMatrix, city_id):
    pathArray.append(city_id)
    prev_city_id = pathArray[len(pathArray) - 2]
    for city in citiesToVisit:
        if city[0] == prev_city_id:
            citiesToVisit.remove(city)

    for distanceList in distanceMatrix:
        distanceList[prev_city_id] = 99999


def chooseCity(pathArray, distanceMatrix):
    if len(pathArray) == 0:  # If path empty, return starting node
        return 0, 0, 0

    bestDistance, idOfBestCity = getNearestCity(
        distanceMatrix, pathArray[(len(pathArray) - 1)])

    if idOfBestCity == -1:
        return -1, -1, -1  # Indicates we are done visiting cities

    return 0, idOfBestCity, bestDistance


def findBestPath(distanceMatrix, cities_to_add):
    # startingCity, endingCity = getNeighborCities(distanceMatrix)
    pathArray = []  # array to hold the paths that we will use
    flag = 0  # Holds flag as to weather we are done adding cities
    totalDistance = 0  # Holds the total distance (in theory)
    # Add cities until we have added them all.
    while flag != -1:
        flag, city_id, distance = chooseCity(
            pathArray, distanceMatrix)
        if flag == 0:
            addCity(pathArray, cities_to_add, distanceMatrix, city_id)
            totalDistance += distance

    return totalDistance, pathArray  # Return the final path to main


print(findBestPath([
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
], [[34.165041450000004, -119.22636029264734], [34.2772814, -119.23266763266079], [34.17504966518035, -119.17763448936975], [34.21978605061019, -119.06729615645638], [34.249636759454894, -119.19504682936139]]))
