from geopy.geocoders import Nominatim
from geopy import distance
import time
from sys import maxsize
import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import permutations


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
    return dist_matrix


def TSP(coords, start):
    distances = distances_from_coords(coords)
    print(distances)
    # store all vertex apart from source vertex
    vertex = [i for i in range(len(distances))]
    # store minimum cost Hamiltonian Cycle
    min_path = maxsize
    next_permutation = permutations(vertex)
    path = []
    for i in next_permutation:
        visited = []
        # store current path cost
        current_cost = 0
        # compute current path cost
        k = start
        for j in i:
            visited.append(j)
            current_cost += distances[k][j]
            k = j
        current_cost += distances[k][start]
        # update minimum
        min_path = min(min_path, current_cost)
        if min_path < current_cost and visited[k - 1] not in path:
            path.append(visited[k - 1])

        # if not next_permutation(vertex):
        #     break
    print(visited)
    print(path)
    return min_path


def next_perm(lst):
    n = len(lst)
    i = n - 2

    while i >= 0 and lst[i] > lst[i + 1]:
        i -= 1
    if i == -1:
        return False
    j = i + 1

    while j < n and lst[j] > lst[i]:
        j += 1
    j -= 1
    lst[i], lst[j] = lst[j], lst[i]
    left = i + 1
    right = n - 1

    while left < right:
        lst[left], lst[right] = lst[right], lst[left]
        left += 1
        right -= 1
    return True


# MAX = 999999
# def TSP(mask, pos, graph, dp, n, visited):
#     if mask == visited:
#         return graph[pos][0]
#     if dp[mask][pos] != -1:
#         return dp[mask][pos]

#     ans = MAX
#     for city in range(0, n):
#         if ((mask & (1 << city)) == 0):
#             new = graph[pos][city] + \
#                 TSP(mask | (1 << city), city, graph, dp, n, visited)
#             ans = min(ans, new)

#     dp[mask][pos] = ans
#     print(visited)
#     return dp[mask][pos]
