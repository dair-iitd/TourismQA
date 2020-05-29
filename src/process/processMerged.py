import re
import sys
import json
import tqdm
import pickle
import argparse
import itertools
from pathlib import Path

from utils import common
from src.process import process1, process2, process3, process4

def getAveragePostLength(posts):
	post_lengths = [len(post["body"]) for post in posts]
	average_post_length = sum(post_lengths)/len(post_lengths)
	return average_post_length

def processMerged(options):
	posts_dir_path = Path(options.posts_dir_path)
	processed_dir_path = Path(options.processed_dir_path)
	logs_dir_path = Path(options.logs_dir_path)

	common.create(posts_dir_path)
	common.create(processed_dir_path)
	common.create(logs_dir_path)

	cities = open(options.cities_file_path, "r").read().splitlines()
	places = open(options.places_file_path, "r").read().splitlines()
	city_entities = pickle.load(open(options.city_entities_file_path, "rb"))

	file_posts = {}
	for file_path in posts_dir_path.glob("*"):
		posts = list(map(json.loads, re.split("(?<=\\})(?=\\{)", open(file_path).read())))
		file_posts[file_path.name] = posts

	average_post_length = getAveragePostLength(posts = itertools.chain.from_iterable(list(file_posts.values())))

	processed_post_links = set()
	for file_name, posts in file_posts.items():
		log_file_path = logs_dir_path / file_name
		processed_file_path = processed_dir_path / file_name

		if(processed_file_path.exists()):
			print("Skipping file %s! Processed file path %s already exists!\n" % (file_name, processed_file_path))

		log_file = open(log_file_path, "w")
		processed_file = open(processed_file_path, "w")

		print("Processing file %s" % (file_name))
		bar = tqdm.tqdm(total = len(posts))
		for post in posts:
			try:
				if(post["link"] in processed_post_links):
					raise Exception("Duplicate post link")
				processed_post_links.add(post["link"])

				post = process1.process(post, places = places, average_post_length = average_post_length)
				post = process2.process(post)
				post = process3.process(post, cities = cities, city_entities = city_entities)
				post = process4.process(post)

				processed_file.write(json.dumps(post, indent = 4, ensure_ascii = False))

				raise Exception("OK")
			except Exception as e:
				log_file.write(json.dumps({"link": post["link"], "info": str(e)}, indent = 4))

			bar.update()

		bar.close()
		log_file.close()
		processed_file.close()

		print()

if(__name__ == "__main__"):
	defaults = {}

	project_root_path = common.getProjectRootPath()

	defaults["posts_dir_path"] = project_root_path / "data" / "temp"
	defaults["processed_dir_path"] = project_root_path / "data" / "processed"
	defaults["logs_dir_path"] = project_root_path / "data" / "logs"
	defaults["cities_file_path"] = project_root_path / "data" / "common" / "cities.txt"
	defaults["places_file_path"] = project_root_path / "data" / "common" / "places.txt"
	defaults["city_entities_file_path"] = project_root_path / "data" / "generated" / "city_entities.pkl"

	parser = argparse.ArgumentParser(description = "Merged Processing")
	parser.add_argument("--posts_dir_path", type = str, default = defaults["posts_dir_path"])
	parser.add_argument("--processed_dir_path", type = str, default = defaults["processed_dir_path"])
	parser.add_argument("--logs_dir_path", type = str, default = defaults["logs_dir_path"])
	parser.add_argument("--cities_file_path", type = str, default = defaults["cities_file_path"])
	parser.add_argument("--places_file_path", type = str, default = defaults["cities_file_path"])
	parser.add_argument("--city_entities_file_path", type = str, default = defaults["city_entities_file_path"])
	options = parser.parse_args(sys.argv[1:])

	processMerged(options)
