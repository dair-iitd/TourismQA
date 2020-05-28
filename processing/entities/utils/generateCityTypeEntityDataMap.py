import os
import sys
import json
import pickle
import pyprind
import argparse
from collections import defaultdict

def generateCityEntityDataMap(options):
    entity_paths = pickle.load(open(options.entity_paths_path, "rb"))
    cities = {str(index): line.strip() for index, line in enumerate(open(options.cities_file_path, "r").readlines())}
    city_entity_data_map = defaultdict(list)

    bar = pyprind.ProgBar(len(entity_paths), bar_char = "█", monitor = True, title = "Generating City Entity Data Map")
    for entity_path in entity_paths:
        entity_data = json.load(open(entity_path, "r"))
        entity_id = entity_data["id"] if("hotel" in entity_path) else entity_data["key"]
        city_id = entity_id.split("_")[0]
        city_name = cities[city_id]
        entity_name = entity_data["reviews"][0]["hotel_name"].replace(city_name, "").lower() if("hotel" in entity_path) else entity_data["name"][0].lower()
        city_entity_data_map[city_id].append({"id": entity_id, "name": entity_name})
        bar.update()

    json.dump(city_entity_data_map, open(options.city_entity_data_map_path, "w"))

parser = argparse.ArgumentParser(description = "Generate City Entity Data Map")
parser.add_argument("--cities_file_path", type = str, default = "/home/goelshashank007/Desktop/btp/TourQueData (copy)/processing/entities/data/cities.txt")
parser.add_argument("--entity_paths_path", type = str, default = "/home/goelshashank007/Desktop/btp/TourQueData (copy)/processing/entities/data/entity_paths.pkl")
parser.add_argument("--city_entity_data_map_path", type = str, default = "/home/goelshashank007/Desktop/btp/TourQueData (copy)/processing/entities/data/city_entity_data_map.json")
options = parser.parse_args(sys.argv[1:])

generateCityEntityDataMap(options)
