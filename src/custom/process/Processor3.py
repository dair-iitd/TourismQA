# https://arxiv.org/pdf/1909.03527.pdf
# Type based Filtering

import numpy as np
from collections import defaultdict
from typing import List, Dict, Tuple

class MultiWordEmbeddings:
	def __init__(self, word_embeddings: Dict[str, List[float]]) -> None:
		self.word_embeddings = word_embeddings

	def __call__(self, string: str) -> List[float]:
		embedding = np.zeros(300)

		for word in string.split():
			if(word in self.word_embeddings):
				embedding += np.array(self.word_embeddings[word])

		if(embedding.any()):
			embedding = embedding / np.linalg.norm(embedding)

		return embedding.tolist()

class Processor:
	def __init__(self, cluster_categories: Dict[str, List[str]], word_embeddings: Dict[str, List[float]]) -> None:
		self.embeddings = MultiWordEmbeddings(word_embeddings = word_embeddings)
		self.categoryXcluster = {category: int(cluster) for cluster, categories in cluster_categories.items() for category in categories}

	def getBestClusterForString(self, string: str) -> Tuple[int, float]:
		embedding = self.embeddings(string)
		category_embeddings = np.array([self.embeddings(category) for category in self.categoryXcluster.keys()])

		scores = np.dot(embedding, np.transpose(category_embeddings))
		index = np.argmax(scores)

		cluster = list(self.categoryXcluster.values())[index]
		score = scores[index]

		return cluster, score

	def getBestClusterForTag(self, tag: str) -> Tuple[str, float]:
		tag = tag.replace("where", "place").replace("areas", "").replace("area", "").replace("options", "").replace("option", "").strip()

		if(tag == ""):
		    return (-1, 0)

		if("stay" in tag.split()):
		    return (1, 1)

		if("eat" in tag.split()):
		    return (0, 1)

		return self.getBestClusterForString(string = tag)

	def getBestClusterForPost(self, post: Dict[str, dict]) -> None:
		cutoff = 0.6
		best_cluster, best_score = (-1, 0)

		if(not (len(post["tags"]["types"]) == 1 and (" " not in post["tags"]["types"][0]) and any(post["tags"]["types"][0].startswith(x) for x in ["place", "option", "area", "site"]))):
			for type in post["tags"]["types"]:
				cluster, score = self.getBestClusterForTag(type)
				if(score > best_score):
				    best_score = score
				    best_cluster = cluster

		if(best_score < cutoff):
			for attribute in post["tags"]["attributes"]:
				cluster, score = self.getBestClusterForTag(attribute)
				if(score > best_score):
				    best_score = score
				    best_cluster = cluster

		if(best_score < cutoff):
		    raise Exception("Best cluster score less than cut-off: %f" % cutoff)

		if(best_cluster in [4, 8]):
		    raise Exception("Best cluster found to be %d" % best_cluster)

		return best_cluster

	def removeEntitiesBasedOnType(self, post: Dict[str, dict]) -> None:
		post_cluster = self.getBestClusterForPost(post)

		for entity_id, entity_item in list(post["entities"].items()):
			if(len(entity_item["categories"]) > 0):
				if((("_R_" in entity_id) and (post_cluster == 0)) or (("_H_" in entity_id) and (post_cluster == 1)) or (("_A_" in entity_id) and (post_cluster == 2)) or (post_cluster in [3, 9])):
					continue

				cluster_frequencies = defaultdict(int)
				for category in entity_item["categories"]:
					cluster = self.categoryXcluster[category.lower()]
					cluster_frequencies[cluster] += 1

				entity_cluster = max(cluster_frequencies, key = cluster_frequencies.get)
				if(post_cluster != entity_cluster):
					del post["entities"][entity_id]
			else:
				if(("_H_" in entity_id and post_cluster == 1) or (("_R_" in entity_id and post_cluster in [2, 7]))):
					continue
				del post["entities"][entity_id]

	def __call__(self, post: Dict[str, dict]) -> None:
		if(len(post["tags"]["types"]) == 0):
			raise Exception("No type tags found")

		self.removeEntitiesBasedOnType(post)
		if(len(post["entities"]) == 0):
			raise Exception("Removed Entities based on Cluster and Categories. No entities left.")
