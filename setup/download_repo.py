#!/usr/bin/env python

# Existing project:
#  >select repo (2/2)
#  >clone locally
#   setup db
#       create local db
#       pull name from project config file
#       pull u/p from computer config file
#   pull staging db and import to local
#       pull h/u/p from config file in project
#   npm install (as needed)

# import sys
import json
import os
from os.path import exists

from global_var import *

name = ''
matchingTitles = []


def check_for_repo_match(name, my_globals):
    global matchingTitles
    # print name, my_globals["allTitles"]
    matchingTitles = []
    if name in my_globals["allTitles"]:
        matchingTitles.append(title)
        return True

    for title in my_globals["allTitles"]:
        if title.lower().startswith(name.lower()):
            matchingTitles.append(title)
    numMatches = len(matchingTitles)
    if numMatches == 1:
        return True

    if numMatches > 1:
        print " ".join(["Which of these projects:", ", ".join(matchingTitles)])
    return False


def ask_for_name(my_globals):
    global name
    name = raw_input("What project do you want to download: ")

    if check_for_repo_match(name, my_globals):
        print "Okay! Downloading", matchingTitles[0]
        getRepo(matchingTitles[0], my_globals)
    else:
        print "try again"
        ask_for_name(my_globals)


def getRepo(title, my_globals):
    for repo in my_globals['repoJSON']:
        if title == repo["repository"]["title"]:
            # print repo["repository"]["repository_url"]

            # converting spaces to dashes for directory name
            title = '-'.join(title.split(' '))

            my_globals['SITE_DIR'] = \
                ''.join([my_globals['projects_dir'], "/", title.lower()])

            if not exists(my_globals['SITE_DIR']):
                os.mkdir(my_globals['SITE_DIR'])

            os.chdir(my_globals['SITE_DIR'])
            print " ".join(["git", "clone",
                            repo["repository"]["repository_url"],
                            my_globals['SITE_DIR']])

            os.system(" ".join(["git",
                      "clone",
                      repo["repository"]["repository_url"],
                      my_globals['SITE_DIR']]))

            # os.chdir(my_globals['SITE_DIR'])
            os.system("git fetch --all")
            os.system("git checkout staging")
            os.system("git pull")

            # Add to tower
            os.system("open .git/ -a /Applications/Tower.app/")

            del my_globals["repoJSON"]
    pass

# for line in sys.argv:
#   print line

if __name__ == "__main__":

    with open(HOME + "/.PUNCH/current_beanstalk_repos.json") as f:
        repoJSON = f.read()
    repoJSON = json.loads(''.join(repoJSON))

    for repo in repoJSON:
        my_globals["allTitles"].append(str(repo["repository"]["title"]))

    print ', '.join(my_globals["allTitles"])
    ask_for_name(my_globals)
