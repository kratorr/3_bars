import sys
import json
from geopy.distance import vincenty


def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as json_file:
        decoded_json = json.load(json_file)
    return decoded_json


def get_bars_data(decoded_json):
    bars_data = decoded_json["features"]
    return bars_data


def get_smallest_bar(bars_data):
    smallest_bar = min(
        bars_data,
        key=lambda x: x["properties"]["Attributes"]["SeatsCount"]
    )
    return smallest_bar


def get_biggest_bar(bars_data):
    biggest_bar = max(
        bars_data,
        key=lambda x: x["properties"]["Attributes"]["SeatsCount"]
    )
    return biggest_bar


def get_closest_bar(bars_data, user_coordinates):
    closest_bar = min(
        bars_data, key=lambda x: vincenty(
            user_coordinates, (
                x["geometry"]["coordinates"][0],
                x["geometry"]["coordinates"][1]
            )
        ).km
    )
    return closest_bar


def pprint_bar(bar):
    print("{}, Seats count:{}".format(
        bar["properties"]["Attributes"]["Name"],
        bar["properties"]["Attributes"]["SeatsCount"])
    )


if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
        bars_data = get_bars_data(load_data(file_path))
    except FileNotFoundError:
        exit("File not found")
    except IndexError:
        exit("Arguments error")
    except ValueError:
        exit("File is not a JSON")
    print("Smallest bar: ", end="")
    pprint_bar(get_smallest_bar(bars_data))
    print("Biggest bar: ", end="")
    pprint_bar(get_biggest_bar(bars_data))
    try:
        longitude = float(input("Enter longitude:"))
        latitude = float(input("Enter latitude:"))
        user_coordinates = (longitude, latitude)
        closest_bar = get_closest_bar(bars_data, user_coordinates)
        print("Closest bar: {}".format(
            closest_bar["properties"]["Attributes"]["Name"])
        )
    except ValueError:
        exit("Value Error")