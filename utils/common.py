import json
import pickle
from pathlib import Path

def getProjectRootPath() -> Path:
    return Path(__file__).parent.parent

def create(path) -> None:
    path = Path(path)
    path.mkdir(parents = True, exist_ok = True)

def dumpJSON(data, path, sort_keys = False) -> None:
    create(Path(path).parent)
    json.dump(data, open(path, "w"), indent = 4, ensure_ascii = False, sort_keys = sort_keys)

def dumpPickle(data, path) -> None:
    create(Path(path).parent)
    pickle.dump(data, open(path, "wb"))
