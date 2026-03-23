import math
def compute_city_distance(v1_long, v1_lat, v2_long, v2_lat):
    #  Convert degrees to radians
    lat_A = math.radians(lat_A)
    lon_A = math.radians(lon_A)
    lat_B = math.radians(lat_B)
    lon_B = math.radians(lon_B)

    # Differences
    delta_lat = lat_B - lat_A
    delta_lon = lon_B - lon_A

    # Haversine formula
    a = math.sin(delta_lat / 2)**2 + math.cos(lat_A) * math.cos(lat_B) * math.sin(delta_lon / 2)**2
    d = 2 * 6371 * math.asin(math.sqrt(a))  # R = 6371 km

    return d

def eval_dist(cities : list((float,float))):
    """
    points: list of (lat, lon) tuples in degrees
    returns: total distance (km) along the path
    """
    if len(cities) < 2:
        return 0.0

    total_dist = 0.0

    for i in range(len(cities) - 1):
        lat_A, lon_A = cities[i]
        lat_B, lon_B = cities[i + 1]
        total_dist += compute_city_distance(lat_A, lon_A, lat_B, lon_B)

    lat_A, lon_A = cities[0]
    lat_B, lon_B = cities[-1]
    total_dist += compute_city_distance(lat_A, lon_A, lat_B, lon_B)
    return total_dist
