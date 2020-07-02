import os
import re
import sys
import json
import time
import tqdm
import pickle
import argparse
import itertools
import datetime
from pathlib import Path
from typing import List, Dict, Tuple

from . import Processor1, Processor2, MSEQtagger, Processor3, Processor4
from utils import common

def getAveragePostLength(posts):
	post_lengths = [len(post["body"]) for post in posts]
	average_post_length = sum(post_lengths)/len(post_lengths)
	return average_post_length

class Processor:
	def __init__(self, average_post_length: int, cities_file_path: Path, city_entities_file_path: Path, cluster_categories_file_path: Path, common_names_file_path: Path, java_dir_path: Path, neighborhood_words_file_path: Path, places_file_path: Path, stop_words_file_path: Path, word_embeddings_file_path: Path) -> None:
		cities = json.load(open(cities_file_path))
		city_entities = json.load(open(city_entities_file_path))
		cluster_categories = json.load(open(cluster_categories_file_path))
		common_names = json.load(open(common_names_file_path))
		neighborhood_words = json.load(open(neighborhood_words_file_path))
		places = json.load(open(places_file_path))
		stop_words = json.load(open(stop_words_file_path))
		word_embeddings = pickle.load(open(word_embeddings_file_path, "rb"))

		self.processors1 = []
		self.processors1.append(Processor.wrap(1, Processor1.Processor(average_post_length = average_post_length)))
		self.processors1.append(Processor.wrap(2, Processor2.Processor(cities = cities, city_entities = city_entities, neighborhood_words = neighborhood_words)))

		self.MSEQtagger = MSEQtagger.MSEQtagger(java_dir_path = java_dir_path)

		self.processors2 = []
		self.processors2.append(Processor.wrap(3, Processor3.Processor(cluster_categories = cluster_categories, word_embeddings = word_embeddings)))
		self.processors2.append(Processor.wrap(4, Processor4.Processor(common_names = common_names, city_entities = city_entities, places = places, stop_words = stop_words)))

	@staticmethod
	def wrap(id: float, function) -> None:
		def processor(post):
			try:
				function(post)
			except Exception as e:
				raise Exception("Processor %d: %s" % (id, str(e)))
		return processor

	def process(self, posts: List[Dict[str, dict]], processors, statuses: List[str]) -> Tuple[List[Dict[str, dict]], List[str]]:
		processed_posts = []
		processed_statuses = []

		bar = tqdm.tqdm(total = statuses.count("OK"))
		for index, (post, status) in enumerate(zip(posts, statuses)):
			if(status == "OK"):
				try:
					for processor in processors:
						processor(post)
					processed_posts.append(post)
					processed_statuses.append("OK")
				except Exception as e:
					processed_posts.append(None)
					processed_statuses.append(str(e))
			else:
				processed_posts.append(None)
				processed_statuses.append(status)
			bar.update()
		bar.close()

		return processed_posts, processed_statuses

	def __call__(self, posts_dir_path: Path, processed_dir_path: Path, logs_dir_path: Path, replace: bool) -> None:
		posts_dir_path = options.posts_dir_path
		processed_dir_path = options.processed_dir_path
		logs_dir_path = options.logs_dir_path

		common.create(posts_dir_path)
		common.create(processed_dir_path)
		common.create(logs_dir_path)

		file_posts = {}
		for file_path in posts_dir_path.glob("**/*.json"):
		    file_posts[str(file_path)] = json.load(open(file_path))

		for file_path, posts in file_posts.items():
			logs_file_path = logs_dir_path / Path(file_path).relative_to(posts_dir_path).with_suffix(".logs.json")
			processed_file_path = processed_dir_path / Path(file_path).relative_to(posts_dir_path).with_suffix(".processed.json")

			common.create(logs_file_path.parent)
			common.create(processed_file_path.parent)

			if(replace == False and processed_file_path.exists()):
			    print("Skipping file %s! Processed file path %s already exists!\n" % (file_path, processed_file_path))
			    continue

			statuses = ["OK"] * len(posts)

			processed_post_links = set()
			for index, post in enumerate(posts):
				if(post["link"] in processed_post_links):
					posts[i] = None
					statuses[i] = "Duplicate post link"
				processed_post_links.add(post["link"])

			links = [post["link"] for post in posts]

			print("Processing file %s" % (file_path))

			print("Running Processing Step 1, 2 . . .")
			posts, statuses = self.process(posts, self.processors1, statuses)

			print("Running MSEQ tagger on Posts . . .", end = "\t")
			start = time.time()
			self.MSEQtagger(posts)
			end = time.time()
			print(str(datetime.timedelta(seconds = int(end - start))), "HH:MM:SS")

			print("Running Processing Step 3, 4 . . .")
			posts, statuses = self.process(posts, self.processors2, statuses)

			logs = [{"link": link, "status": status} for link, status in zip(links, statuses)]
			processed_posts = list(filter(lambda post: post is not None, posts))

			json.dump(logs, open(logs_file_path, "w"), indent = 4, ensure_ascii = False)
			json.dump(processed_posts, open(processed_file_path, "w"), indent = 4, ensure_ascii = False)

			print()

if(__name__ == "__main__"):
	project_root_path = common.getProjectRootPath()

	defaults = {}

	defaults["posts_dir_path"] = project_root_path / "data" / "input"
	defaults["processed_dir_path"] = project_root_path / "data" / "processed"
	defaults["logs_dir_path"] = project_root_path / "data" / "logs"
	defaults["cities_file_path"] = project_root_path / "data" / "common" / "cities.json"
	defaults["city_entities_file_path"] = project_root_path / "data" / "generated" / "city_entities.json"
	defaults["cluster_categories_file_path"] = project_root_path / "data" / "common" / "cluster_categories.json"
	defaults["common_names_file_path"] = project_root_path / "data" / "common" / "common_names.json"
	defaults["java_dir_path"] = project_root_path / "java"
	defaults["neighborhood_words_file_path"] = project_root_path / "data" / "common" / "neighborhood_words.json"
	defaults["places_file_path"] = project_root_path / "data" / "common" / "places.json"
	defaults["stop_words_file_path"] = project_root_path / "data" / "common" / "stop_words.json"
	defaults["word_embeddings_file_path"] = project_root_path / "data" / "common" / "word_embeddings.pkl"

	parser = argparse.ArgumentParser(description = "Merged Processing")

	parser.add_argument("--posts_dir_path", type = str, default = defaults["posts_dir_path"])
	parser.add_argument("--processed_dir_path", type = str, default = defaults["processed_dir_path"])
	parser.add_argument("--logs_dir_path", type = str, default = defaults["logs_dir_path"])
	parser.add_argument("--cities_file_path", type = str, default = defaults["cities_file_path"])
	parser.add_argument("--city_entities_file_path", type = str, default = defaults["city_entities_file_path"])
	parser.add_argument("--cluster_categories_file_path", type = str, default = defaults["cluster_categories_file_path"])
	parser.add_argument("--common_names_file_path", type = str, default = defaults["common_names_file_path"])
	parser.add_argument("--java_dir_path", type = str, default = defaults["java_dir_path"])
	parser.add_argument("--neighborhood_words_file_path", type = str, default = defaults["neighborhood_words_file_path"])
	parser.add_argument("--places_file_path", type = str, default = defaults["places_file_path"])
	parser.add_argument("--stop_words_file_path", type = str, default = defaults["stop_words_file_path"])
	parser.add_argument("--word_embeddings_file_path", type = str, default = defaults["word_embeddings_file_path"])
	parser.add_argument("--replace", type = str, default = True)

	options = parser.parse_args(sys.argv[1:])

	posts = []
	for file_path in options.posts_dir_path.glob("**/*.json"):
	    posts += json.load(open(file_path))
	average_post_length = getAveragePostLength(posts)

	processor = Processor(average_post_length = average_post_length, cities_file_path = Path(options.cities_file_path), city_entities_file_path = Path(options.city_entities_file_path), cluster_categories_file_path = Path(options.cluster_categories_file_path), common_names_file_path = Path(options.common_names_file_path), java_dir_path = Path(options.java_dir_path), neighborhood_words_file_path = Path(options.neighborhood_words_file_path), places_file_path = Path(options.places_file_path), stop_words_file_path = Path(options.stop_words_file_path), word_embeddings_file_path = Path(options.word_embeddings_file_path))

	processor(posts_dir_path = Path(options.posts_dir_path), processed_dir_path = Path(options.processed_dir_path), logs_dir_path = Path(options.logs_dir_path), replace = options.replace)
