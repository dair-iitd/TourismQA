import os
import sys
import pickle
import argparse

def generateEntityPaths(options):
    entity_paths = []

    input_path = os.path.join(options.tourque_data_path, "2018_ATTR_rEST_PROCESSED")
    for city_dir_name in os.listdir(input_path):
        input_city_dir_path = os.path.join(input_path, city_dir_name)
        for entity_file_name in os.listdir(input_city_dir_path):
            entity_file_path = os.path.join(input_city_dir_path, entity_file_name)
            entity_paths.append(entity_file_path)

    input_path = os.path.join(options.tourque_data_path, "2018_HOTELS", "processed-hotels-v3")
    for city_dir_name in os.listdir(input_path):
        input_city_dir_path = os.path.join(input_path, city_dir_name)
        for entity_file_name in os.listdir(input_city_dir_path):
            entity_file_path = os.path.join(input_city_dir_path, entity_file_name)
            entity_paths.append(entity_file_path)

    pickle.dump(entity_paths, open(options.entity_paths_path, "wb"))

parser = argparse.ArgumentParser(description = "Generate Entity Paths")
parser.add_argument("--tourque_data_path", type = str, default = "/home/goelshashank007/Desktop/btp/TOURQUE_DATA_JUNE_2018/PROCESSED_DATA_JUNE_2018_FULL")
parser.add_argument("--entity_paths_path", type = str, default = "entity_paths.pkl")
options = parser.parse_args(sys.argv[1:])
generateEntityPaths(options)
