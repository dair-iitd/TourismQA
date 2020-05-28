import re
import os
import sys
import bs4
import math
import time
import logging
import argparse
import urllib.request

parent_link = "http://www.tripadvisor.in/"

# get the page text for the link
def getPage(link, retries = 5):
    """ Delay the request for sleep_time seconds. """
    while(retries > 0):
        time.sleep(0.01)
        try:
            response = urllib.request.urlopen(link)
            html = response.read()
            return str(html)
        except:
            retries -= 1
            print("Retrying..({0}).. in page {1} ".format(retries, link))
    return ""

# get the page count from the page text
def getPageCount(page_text):
    soup = bs4.BeautifulSoup(page_text, "html.parser")
    a = soup.findAll("div", attrs = {"class": "pgLinks"})
    return int(a[0].findAll("a", attrs = {"class": "paging taLnk"})[-1].text)

# get links of the forums
def getForumLinks(page_text, num_posts, page_num, num_pinned_posts):
    soup = bs4.BeautifulSoup(page_text, "html.parser")
    alltr = soup.find("table", attrs = {"class": "topics"}).findAll("tr")
    data = [tuple([str(x["href"]) for x in i.findAll("a")[:2]]) for i in alltr[1:]]

    # filter pinned posts on the first page
    if(page_num == 0):
        data = data[num_pinned_posts + 1:]

    href_links = []
    for (href_link, _) in data:
        href_links.append(href_link)
        num_posts -= 1
        if(num_posts == 0):
            break

    return href_links, num_posts

# get the link for the next page
def getNextPage(link, page_num, num_entries_per_page):
    l = re.findall(r"o\d+", link)
    if(len(l) == 0):
        if(page_num == 0):
            e = re.search(r"i\d+", link).end()
            next_link = link[:e] + "-o" + str(num_entries_per_page) + link[e:]
            return next_link
        else:
            print("error: page number is not correct")
            logging.error("page number is not correct")
            sys.exit(1)
    else:
        num = int(l[0][1:])
        if(num == page_num * num_entries_per_page):
            m = re.search(r"o\d+", link)
            s = m.start()
            e = m.end()
            next_link = link[:s + 1] + str(int(link[s + 1:e]) + num_entries_per_page) + link[e:]
            return next_link
        else:
            print("error: page number is not correct, %s != %s" % (num, page_num * num_entries_per_page))
            logging.error("page number is not correct")
            sys.exit(1)

# store the links for all the forums
def storeAllForumLinks(state, link, directory, page_count, num_posts, num_pinned_posts, num_entries_per_page, retries, file):
    count = 0
    total_faults = 0
    post_number = num_pinned_posts + 1
    num_pages = min(math.ceil((num_posts + num_pinned_posts + 1) / num_entries_per_page), page_count)
    while (count < num_pages):
        page_text = getPage(link = link, retries = retries)

        if(not page_text):
            print("warning: Cannot retreive data from %s" % link)
            logging.warning("Cannot retreive data from %s" % link)
            continue

        href_links, num_posts = getForumLinks(page_text = page_text, num_posts = num_posts, page_num = count, num_pinned_posts = num_pinned_posts)

        page_faults = 0
        for href_link in href_links:
            post_number += 1
            forum_link = parent_link + href_link

            try:
                forum_page_text = getPage(link = forum_link, retries = retries)
                if(not forum_page_text):
                    raise Exception("Fault")

                forum_file_name = re.search(r"k\d{8}", href_link).group()
                file.write("%s, %s\n" % (forum_file_name, forum_link))
                with open(os.path.join(directory, forum_file_name), "w") as forum_file:
                    forum_file.write(forum_page_text)
            except:
                page_faults += 1
                total_faults += 1
                print("error: Fault on post number %d of page %d for %s" % (post_number, count + 1, state))
                logging.error("Fault on post number %d of page %d for %s" % (post_number, count + 1, state))

        print("Crawled %d posts from page %d" % (len(href_links) - page_faults, count + 1))
        link = getNextPage(link = link, page_num = count, num_entries_per_page = num_entries_per_page)
        count += 1
        post_number = 0

    print()
    return total_faults

def startCrawling(options):
    # logging the links that have been downloaded
    logging.basicConfig(filename = options.log_file_path, level = logging.INFO)

    # reading the continent file
    lines = open(os.path.join(options.links_dir_path, options.continent + ".csv"), "r").readlines()

    for line in lines:
        state, link = line.strip().split(", ")

        print("State: %s\nLink: %s\n" % (state, link))

        # getting page for the link
        page_text = getPage(link = link, retries = options.retries)
        if (page_text == ""):
            print("warning: Not able to fetch Page %s for %s" % (link, state))
            logging.warning("Not able to fetch Page %s for %s" % (link, state))
            continue

        page_count = getPageCount(page_text = page_text)

        print("Crawling for %s...\nTotal: %d\nRequested: %d\n" % (state, options.num_entries_per_page * page_count, options.num_posts))
        logging.info("Crawling for %s...\nTotal: %d\nRequested: %d\n" % (state, options.num_entries_per_page * page_count, options.num_posts))

        # storing retrieved data
        directory = os.path.join(options.forums_dir_path, options.continent, state, "forum_data")
        if (not os.path.exists(directory)):
            os.makedirs(directory)

        with open(os.path.join(os.path.dirname(directory), "forum_links.csv"), "w") as file:
            total_faults = storeAllForumLinks(state = state, link = link, directory = directory, page_count = page_count, num_posts = options.num_posts, num_pinned_posts = options.num_pinned_posts, num_entries_per_page = options.num_entries_per_page, retries = options.retries, file = file)

        print("Succesfully retrieved %d posts for %s\n" % (options.num_posts - total_faults, state))

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description = "Crawling Forum Posts")
    parser.add_argument("--continent", type = str, required = True)
    parser.add_argument("--num_posts", type = int, required = True)
    parser.add_argument("--log_file_path", type = str, required = True)
    parser.add_argument("--num_pinned_posts", type = int, required = True)
    parser.add_argument("--num_entries_per_page", type = int, required = True)
    parser.add_argument("--retries", type = int, default = 5)
    parser.add_argument("--links_dir_path", type = str, default = "Links")
    parser.add_argument("--forums_dir_path", type = str, default = "Forums")
    options = parser.parse_args(sys.argv[1:])
    startCrawling(options)
