import json
import pickle
from pathlib import Path

def getProjectRootPath() -> Path:
    return Path(__file__).parent.parent

def create(path) -> None:
    path = Path(path)
    path.mkdir(parents = True, exist_ok = True)

def loadJSON(path) -> None:
    return json.load(open(path, "r", encoding = "utf-8"))

def dumpJSON(data, path, sort_keys = False) -> None:
    create(Path(path).parent)
    json.dump(data, open(path, "w", encoding = "utf-8"), indent = 4, ensure_ascii = False, sort_keys = sort_keys)

def dumpPickle(data, path) -> None:
    create(Path(path).parent)
    pickle.dump(data, open(path, "wb"))

def update(d, u):
    for k, v in u.items():
        if(isinstance(v, dict)):
            d[k] = update(d[k], v)
        else:
            if(isinstance(v, list)):
                for e in v:
                    if(e not in d[k]):
                        d[k].append(e)
            else:
                d[k] = v
    return d
