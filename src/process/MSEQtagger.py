import os
import json
import glpk
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict

class FeatureBuilder:
    def __init__(self, java_dir_path: Path) -> None:
        self.java_dir_path = java_dir_path

    def getFeatures(self, questions: List[str]) -> List[str]:
        ifd, ipath = tempfile.mkstemp()
        ofd, opath = tempfile.mkstemp()
        tfd, tpath = tempfile.mkstemp()

        data = [{"question": question} for question in questions]
        json.dump(data, open(ipath, "w"))

        command = 'java -jar FeatureTools.jar feature "%s" "%s" "%s" .' % (ipath, opath, tpath)
        process = subprocess.Popen(command, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd = str(self.java_dir_path), shell = True)
        process.wait()

        data = json.load(open(opath, "r"))
        features = [item["features"].strip() for item in data]

        os.close(ifd)
        os.close(ofd)
        os.close(tfd)

        return features

class Tagger:
    def __init__(self, java_dir_path: Path) -> None:
        self.java_dir_path = java_dir_path
        self.feature_builder = FeatureBuilder(java_dir_path = java_dir_path)

    def generateFeaturesDirectory(self, features: List[str]) -> Path:
        features_dir_path = tempfile.mkdtemp(dir = str(self.java_dir_path))
        for index, item in enumerate(features):
            _, feature_file_path = tempfile.mkstemp(dir = features_dir_path, prefix = "%d." % index, suffix = ".feat")
            with open(feature_file_path, "w") as file:
                file.write(item)

        return Path(features_dir_path)

    def generateILPfiles(self, features: List[str]) -> List[Path]:
        ilp_dir_path = self.java_dir_path / "ILP_FOLDER"

        if(os.path.exists(ilp_dir_path)):
            shutil.rmtree(ilp_dir_path)
        os.makedirs(ilp_dir_path)

        features_dir_path = self.generateFeaturesDirectory(features)

        command = 'java -jar FeatureTools.jar ilp "%s" .' % (features_dir_path)
        process = subprocess.Popen(command, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd = str(self.java_dir_path), shell = True)
        process.wait()

        shutil.rmtree(features_dir_path)

        ilp_file_paths = [None] * len(features)
        with open(self.java_dir_path / "files_map.txt", "r") as file:
            for line in file.readlines():
                ilp_file_index, feature_file_path = line.split(",")
                feature_file_index = int(Path(feature_file_path).name.split(".", 1)[0])
                ilp_file_path = str(self.java_dir_path / ("ILP_FOLDER/ilp_file_%s.txt" % (ilp_file_index)))
                ilp_file_paths[feature_file_index] = Path(ilp_file_path)
            os.remove(self.java_dir_path / "files_map.txt")

        return ilp_file_paths

    def getLabels(self, ilp_file_paths: List[Path]) -> List[List[str]]:
        glpk.env.term_on = False

        labels = []
        for ilp_file_path in ilp_file_paths:
            ilabels = []
            if(ilp_file_path.exists()):
                solver = glpk.LPX(cpxlp = str(ilp_file_path))
                solver.scale()
                solver.adv_basis()
                solver.simplex(presolve = True)
                solver.intopt()

                for item in solver.cols:
                    x = item.name.split("_")
                    if(item.value == 1):
                        if((x[0] != "D1" and x[0][0] != "Z") and (x[1] != "minus")):
                            if(x[1] == "attr"):
                                ilabels.append("attributes")
                            elif(x[1] == "type"):
                                ilabels.append("types")
                            else:
                                ilabels.append("O")

            labels.append(ilabels)

        shutil.rmtree(self.java_dir_path / "ILP_FOLDER")

        return labels

    def getTags(self, features, labels) -> List[List[str]]:
        tags = []

        for ifeatures, ilabels in zip(features, labels):
            itokens = [x.split(" ", 1)[0] for x in ifeatures.split("\n")]
            itags = {"attributes": [], "types": []}

            if(len(ilabels) > 0):
                current = "O"
                string = ""
                for token, label in zip(itokens, ilabels):
                    if(label == current):
                        string += token + " "
                    else:
                        if(current != "O"):
                            itags[current].append(string.strip())
                        current = label
                        string = token + " "
                if(current != "O"):
                    itags[current].append(string.strip())

            tags.append(itags)

        return tags

    def tag(self, questions: List[str]) -> List[List[str]]:
        features = self.feature_builder.getFeatures(questions)
        ilp_file_paths = self.generateILPfiles(features)
        labels = self.getLabels(ilp_file_paths)
        tags = self.getTags(features, labels)

        return tags

class MSEQtagger:
    def __init__(self, java_dir_path: Path):
        self.tagger = Tagger(java_dir_path = java_dir_path)

    def __call__(self, posts: List[Dict[str, dict]]) -> None:
        if(len(posts) == 0):
            return []

        questions = [post["question"] for post in posts if post is not None]
        tags = self.tagger.tag(questions)
        questionsXtags = dict(zip(questions, tags))

        for post in posts:
            if(post is not None):
                post["tags"] = questionsXtags[post["question"]]
