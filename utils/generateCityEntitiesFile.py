import sys
import json
import glob
import tqdm
import argparse
from pathlib import Path
from collections import defaultdict
from utils import common

def generate(input_dir_path, output_file_path):
    data = defaultdict(dict)

    files = glob.glob(str(input_dir_path / "**/*.json"), recursive = True)
    for file in files:
        item = common.loadJSON(file)
        data[item["id"].split("_")[0]][item["id"]] = {"id": item["id"], "name": item["name"], "categories": item["properties"], "location": [item["latitude"], item["longitude"]]}

    common.dumpJSON(data, output_file_path)

if(__name__ == "__main__"):
    project_root_path = common.getProjectRootPath()

    defaults = {}

    defaults["input_dir_path"] = project_root_path / "data" / "tourque" / "entities" / "data"
    defaults["output_file_path"] = project_root_path / "data" / "generated" / "city_entities.tourque.json"

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_dir_path", type = str, default = defaults["input_dir_path"])
    parser.add_argument("-o", "--output_file_path", type = str, default = defaults["output_file_path"])

    options = parser.parse_args(sys.argv[1:])

    generate(input_dir_path = Path(options.input_dir_path), output_file_path = Path(options.output_file_path))
