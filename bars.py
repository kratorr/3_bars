import sys
import json
from geopy.distance import vincenty


def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as json_file:
        decoded_json = json.load(json_file)
    return decoded_json


def get_smallest_bar(decoded_json):
    smallest_bar = min(decoded_json["features"],
                       key=lambda x: x["properties"]["Attributes"]
                        ["SeatsCount"])
    return smallest_bar


def get_biggest_bar(decoded_json):
    biggest_bar = max(decoded_json["features"],
                       key=lambda x: x["properties"]["Attributes"]
                       ["SeatsCount"])
    return biggest_bar


def get_closest_bar(decoded_json, user_coordinates):
    closest_bar = min(decoded_json["features"], key=lambda x:
    vincenty(user_coordinates, (x["geometry"]["coordinates"][0],
                               x["geometry"]["coordinates"][1])).km)
    return closest_bar


if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
    except IndexError:
        print("Arguments error")
    else:
        bar_data = load_data(file_path)
        small_bar = get_smallest_bar(bar_data)
        big_bar = get_biggest_bar(bar_data)
        print("Smallest bar: {}, Seats count:{}".format(
            small_bar["properties"]["Attributes"]["Name"],
            small_bar["properties"]["Attributes"]["SeatsCount"])
        )
        print("Biggest bar: {}, Seats count:{}".format(
            big_bar["properties"]["Attributes"]["Name"],
            big_bar["properties"]["Attributes"]["SeatsCount"])
        )
        try:
            longitude = float(input("Enter longitude:"))
            latitude = float(input("Enter latitude:"))
            user_coordinates = (longitude, latitude)
            closest_bar = get_closest_bar(bar_data, user_coordinates)
            print("Closest bar: {}".format(
                closest_bar["properties"]["Attributes"]["Name"]))
        except ValueError:
            print("Value Error")




