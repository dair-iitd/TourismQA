import json
import pickle
from pathlib import Path
from functools import wraps

def getProjectRootPath() -> Path:
    return Path(__file__).parent.parent

def catcher(step):
	def decorator(function):
		@wraps(function)
		def wrapper(post, *args, **kwargs):
			try:
				post = function(post, *args, **kwargs)
				if(len(post["entities"]) == 0):
					raise Exception("No entities left")
				else:
					return post
			except Exception as e:
				raise Exception("%d: %s" % (step, str(e)))
		return wrapper
	return decorator

def create(path) -> None:
    path = Path(path)
    path.mkdir(parents = True, exist_ok = True)

def dumpJSON(data, path, sort_keys = False) -> None:
    path = Path(__file__).parent
    path.mkdir(parents = True, exist_ok = True)
    json.dump(data, open(path, "w"), indent = 4, ensure_ascii = False, sort_keys = sort_keys)

def dumpPickle(data, path) -> None:
    path = Path(__file__).parent
    path.mkdir(parents = True, exist_ok = True)
    pickle.dump(data, open(path, "wb"))
