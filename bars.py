import sys
import json
import collections
import geopy.distance


def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as json_file:
        decoded_json = json.load(json_file)
    return decoded_json


def parse_json(decoded_json):
    seats_count_bar_dict = collections.defaultdict(list)
    for bar in decoded_json["features"]:
        seats_count = bar["properties"]["Attributes"]["SeatsCount"]
        bar_name = bar["properties"]["Attributes"]["Name"]
        seats_count_bar_dict[seats_count].append(bar_name)
    return  seats_count_bar_dict


def get_smallest_bar(seats_count_bar_dict):
    min_seats = min(seats_count_bar_dict)
    return min_seats, seats_count_bar_dict[min_seats]


def get_biggest_bar(seats_count_bar_dict):
    max_seats = max(seats_count_bar_dict)
    return max_seats, seats_count_bar_dict[max_seats]


def get_closest_bar(decoded_json, longitude, latitude):
    user_bar_coordinates = (longitude, latitude)
    min_dist = None
    for bar in decoded_json["features"]:
        bar_longitude = bar["geometry"]["coordinates"][0]
        bar_latitude = bar["geometry"]["coordinates"][1]
        bar_coordinates = (bar_longitude, bar_latitude)
        distance_between_2_bars = geopy.distance.vincenty(user_bar_coordinates, bar_coordinates).km
        if min_dist is None:
            min_dist = distance_between_2_bars
        elif distance_between_2_bars < min_dist :
                min_dist = distance_between_2_bars
                closest_bar_name = bar["properties"]["Attributes"]["Name"]
    return closest_bar_name, min_dist


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
        file_path = "bars.json"
    except IndexError:
        print("Arguments error")
    else:
        bar_data = load_data(file_path)
        small_bar = get_smallest_bar(parse_json(bar_data))
        big_bar = get_biggest_bar(parse_json(bar_data))
        print("Smallest bar: {}, Seats count: {} ".format(small_bar[0], (small_bar[1])))
        print("Biggest bar: {}, Seats count: {}".format(big_bar[0], big_bar[1]))
        longitude = float(input("Enter longitude:"))
        latitude = float(input("Enter latitude:"))
        closest_bar = get_closest_bar(bar_data, longitude, latitude)
        print("Closest bar: {}, distance: {:.3f} km".format(closest_bar[0], closest_bar[1]))