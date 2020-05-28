import re
import os
import sys
import json
import time
import bs4
import urllib.request

parent_dir = 'PostAnswers'
tourquedata_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
forum_dir = os.path.abspath(os.path.join(tourquedata_dir, 'crawlers', 'posts', 'Forums'))

def getAllPostData(forum_text):
    soup = bs4.BeautifulSoup(forum_text, 'html.parser')

    try:
        titles = soup.findAll('div', attrs = {'class': "\\'postTitle\\'"})
        titles = [title.text for title in titles]
    except AttributeError:
        print('Title not found!')

    try:
        bodies = soup.findAll('div', attrs = {'class': "\\'postBody\\'"})
        bodies = [body.text for body in bodies]
    except AttributeError:
        print('Body not found!')

    try:
        dates = soup.findAll('div', attrs = {'class': "\\'postDate\\'"})
        dates = [date.string for date in dates]
    except AttributeError:
        print('Date not found!')

    return (titles, bodies, dates)

def extractAnswers(titles, bodies, dates):
    title, body, date = ('', '', '')
    answers = []

    if (len(dates) > 0):
        title, body, date = (titles[0], bodies[0], dates[0])
        for i in range(1, len(dates)):
            answer = {'title': titles[i], 'body': bodies[i], 'date': dates[i]}
            answers.append(answer)

    return (title, body, date, answers)

def filter_posts(forum_dict):
    accepted_forum_dict = {'posts': []}
    rejected_forum_dict = {'posts': []}

    for post in forum_dict['posts']:
        q_lc = post['body']
        if(any(i in q_lc for i in ['recommend', 'suggest', 'place to', 'where', 'option', 'best'])):
            accepted_forum_dict['posts'].append(post)
        else:
            rejected_forum_dict['posts'].append(post)

    return accepted_forum_dict, rejected_forum_dict

def buildJSON(continent):
    input_continent_dir = os.path.join(forum_dir, continent)
    output_continent_dir = os.path.join(parent_dir, continent)

    structs = list(os.walk(input_continent_dir))[1:]
    for i in range(0, len(structs), 2):
        forum_dict = {'posts': []}
        state = os.path.relpath(structs[i][0], input_continent_dir)

        forum_data_path = os.path.join(structs[i][0], structs[i][1][0])
        forum_link_path = os.path.join(structs[i][0], structs[i][2][0])

        with open(forum_link_path, 'r') as file:
            file_links = {i:j for i, j in [k.strip().split(', ') for k in file.readlines()]}

        for file_name in structs[i + 1][2]:
            if(file_name not in file_links):
                continue

            link = file_links[file_name]
            with open(os.path.join(forum_data_path, file_name), 'r') as file:
                forum_text = '\n'.join(file.readlines())

            titles, bodies, dates = getAllPostData(forum_text)
            title, body, date, answers = extractAnswers(titles = titles, bodies = bodies, dates = dates)

            element = {'continent': continent, 'state': state, 'link': link, 'title': title, 'body': body, 'date': date, 'answers': answers}
            forum_dict['posts'].append(element)

        output_state_dir = os.path.join(output_continent_dir, state)
        if(not os.path.exists(output_state_dir)):
            os.makedirs(output_state_dir)

        file1_name = 'accepted_forum_posts.json'
        file1_path = os.path.join(output_state_dir, file1_name)

        file2_name = 'rejected_forum_posts.json'
        file2_path = os.path.join(output_state_dir, file2_name)

        accepted_forum_dict, rejected_forum_dict = filter_posts(forum_dict = forum_dict)

        print('Creating files: %s (%d entries) & %s (%d entries)' % (file1_path, len(accepted_forum_dict['posts']), file2_path, len(rejected_forum_dict['posts'])))

        with open(file1_path, 'w') as file:
            file.write(json.dumps(accepted_forum_dict, indent = 4))

        with open(file2_path, 'w') as file:
            file.write(json.dumps(rejected_forum_dict, indent = 4))

buildJSON(continent = 'America_Europe')
