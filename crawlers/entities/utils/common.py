import os

def getStartUrls(name):
    start_urls_file_name = name + ".txt"
    start_urls_file_path = os.path.join("urls", start_urls_file_name)
    with open(start_urls_file_path, "r") as file:
        start_urls = [line.strip() for line in file.readlines()[:1]]
    return start_urls
