from api import db


def new_workout(coord: list, dist: float, dur: float, elev: float):
    workout = {
        "coordinates": coord,
        "distance": dist,
        "duration": dur,
        "elev": elev
    }
