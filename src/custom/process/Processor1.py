# https://arxiv.org/pdf/1909.03527.pdf
# Filter Trip Reports
# Inappropriate Posts
# Long Posts
# Irrelevant Posts

from typing import Dict, List

class Processor:
	def __init__(self, average_post_length: int) -> None:
		self.average_post_length = average_post_length

	def isTripReport(self, title: str) -> bool:
		b1 = any(x in title for x in ["TR ", "TR-", "TR/", "TR:", "TR."])
		b2 = any(x in title.lower() for x in ["trip report", "trip review"])
		return b1 or b2

	def isNotAppropriate(self, answers: List[Dict[str, str]]) -> bool:
		return any("This post was determined to be inappropriate by the TripAdvisor community" in answer["body"] for answer in answers)

	def isLongPost(self, question: str) -> bool:
		return len(question) > 1.7 * self.average_post_length

	def isIrrelevantPost(self, title: str, question: str) -> bool:
		b1 = any(x in title.lower() for x in ["vs", " or ", "your thoughts", "route", "transfer", "how", "itinerary", "review"])
		b2 = any(x in question.lower() for x in ["itinerary"])
		return b1 or b2

	def __call__(self, post: Dict[str, dict]) -> None:
		if(self.isTripReport(post["title"])):
			raise Exception("Trip Report")

		if(self.isNotAppropriate(post["answers"])):
			raise Exception("Is Not Appropriate")

		if(self.isLongPost(post["question"])):
			raise Exception("Long Post")

		if(self.isIrrelevantPost(post["title"], post["question"])):
			raise Exception("Irrelevant Post")
