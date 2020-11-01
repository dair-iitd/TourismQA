import os
import re
import sys
import json
import argparse
import itertools
from pathlib import Path
from  datetime import datetime
from typing import List, Dict, Tuple
from utils import common

def convert(post: Dict[str, dict]) -> List[Dict[str, dict]]:
    outposts = []

    question = post["question"]
    url = post["url"]
    answer_entity_ids = list(post["entities"].keys())

    for answer_entity_id in answer_entity_ids:
        outpost = {}
        outpost["question"] = question
        outpost["url"] = url
        outpost["answer_entity_id"] = answer_entity_id
        outpost["answer_lat_long"] = post["entities"][answer_entity_id]["location"]
        outpost["answer_entity_ids"] = answer_entity_ids
        outposts.append(outpost)

    return outposts

def convertProcessedPostsToDataFormat(processed_dir_path: Path, dataformat_dir_path: Path, start_date: int, end_date: int, replace: bool, ignore: bool) -> None:
    processed_dir_path = options.processed_dir_path
    dataformat_dir_path = options.dataformat_dir_path

    start_date = datetime.strptime(start_date, "%d%m%Y")
    end_date = datetime.strptime(end_date, "%d%m%Y")

    def check(x):
        try:
            date = datetime.strptime(x.split(",")[0].strip(), "%d %b %Y")
            return (date >= start_date) and (date <= end_date)
        except:
            return ignore

    file_posts = {}
    for file_path in processed_dir_path.glob("**/*.json"):
        file_posts[str(file_path)] = json.load(open(file_path, encoding = "utf-8"))

    for file_path, processed_posts in file_posts.items():
        dataformat_file_path = dataformat_dir_path / Path(file_path).relative_to(processed_dir_path).with_suffix(".dataformat.json")

        if(replace == False and dataformat_file_path.exists()):
            print("Skipping file %s! DataFormat file path %s already exists!\n" % (file_path, dataformat_file_path))
            continue

        print("Processing file %s" % (file_path))

        dataformat_posts = [convert(post) for post in processed_posts if check(post["date"])]
        print("Accepted %d of %d posts" % (len(dataformat_posts), len(processed_posts)))

        dataformat_posts = list(itertools.chain.from_iterable(dataformat_posts))
        common.dumpJSON(dataformat_posts, dataformat_file_path)

if(__name__ == "__main__"):
    project_root_path = common.getProjectRootPath()

    defaults = {}

    defaults["processed_dir_path"] = project_root_path / "data" / "posts" / "processed"
    defaults["dataformat_dir_path"] = project_root_path / "data" / "posts" / "dataformat"
    defaults["start_date"] = "01010001"
    defaults["end_date"] = "31129999"
    defaults["replace"] = False
    defaults["ignore"] = False

    parser = argparse.ArgumentParser(description = "Convert processed posts to data format")

    parser.add_argument("--processed_dir_path", type = str, default = defaults["processed_dir_path"])
    parser.add_argument("--dataformat_dir_path", type = str, default = defaults["dataformat_dir_path"])
    parser.add_argument("--start_date", type = str, default = defaults["start_date"])
    parser.add_argument("--end_date", type = str, default = defaults["end_date"])
    parser.add_argument("--replace", action = "store_true", default = defaults["replace"])
    parser.add_argument("--ignore", action = "store_true", default = defaults["ignore"])

    options = parser.parse_args(sys.argv[1:])

    convertProcessedPostsToDataFormat(processed_dir_path = Path(options.processed_dir_path), dataformat_dir_path = Path(options.dataformat_dir_path), start_date = options.start_date, end_date = options.end_date, replace = options.replace, ignore = options.ignore)
