import logging
from typing import Any
from geopy.geocoders import Nominatim
from geopy import distance
from scipy.spatial.distance import pdist, squareform
import time


# [Getting coordinates from address]
def coords_by_address(address: str):
    app = Nominatim(user_agent="tsp-api")
    time.sleep(1)
    try:
        location = app.geocode(address)
        lon = float(location.longitude)
        lat = float(location.latitude)
        return [lat, lon]

    except:
        return coords_by_address(address)


# [Getting distance between two coordinates]
def dist_between_coords(coords1, coords2):
    miles = distance.geodesic(coords1, coords2).miles
    return miles


# [Getting distances between all coordinates]
def distance_matrix(coords: list) -> list[float]:
    dist_array = pdist(coords)
    dist_matrix = squareform(dist_array)
    # print(dist_matrix)
    return list(dist_matrix.tolist())


# [Finding optimal path]
def tsp_path(coords: list) -> tuple:
    if len(coords) == 0:
        return [], 0
    
    if len(coords) == 1:
        return [0, 0], 0
    
    dist_matrix: list = distance_matrix(coords)
    num_nodes: int = len(coords)
    
    # Initialize the memorization table
    memo_table: dict = {}
    
    # Helper function for dynamic programming
    def dp_tsp(node: int, visited: int) -> tuple:
        # Base case: If all nodes have been visited, return the distance to node 0
        if visited == (1 << num_nodes) - 1:
            return dist_matrix[node][0], [0]
        
        # Memorization: Check if already computed
        if (node, visited) in memo_table:
            return memo_table[(node, visited)]
        
        shortest_path: list = []
        min_dist = float('inf')
        
        # Try all possible next nodes to visit
        for next_node in range(num_nodes):
            if (visited >> next_node) & 1 == 0:  # If next_node not visited yet
                new_visited: int = visited | (1 << next_node)  # Mark next_node as visited
                total_dist, path = dp_tsp(next_node, new_visited)
                total_dist += dist_matrix[node][next_node]
                
                # Update if total distance is shorter
                if total_dist < min_dist:
                    min_dist = total_dist
                    shortest_path = [next_node] + path
        
        # Memorize the result
        memo_table[(node, visited)] = (min_dist, shortest_path)
        return min_dist, shortest_path
    
    # Start the dynamic programming from node 0
    min_dist, path = dp_tsp(0, 1)
    
    # Add the starting point to complete the path
    shortest_path = [0] + path
    
    return shortest_path, min_dist

