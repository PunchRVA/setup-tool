#!/usr/bin/env python

# Existing project:
#  >select repo (1/2)
#   clone locally
#   setup db
#       create local db
#       pull name from project config file
#       pull u/p from computer config file
#   pull staging db and import to local
#       pull h/u/p from config file in project
#   npm install (as needed)

import urllib2
import json
import os
import math

from global_var import *


def getRepositories(my_globals):
    url = my_globals["repo_api"]["url"]
    user = my_globals["repo_api"]["username"]
    password = my_globals["repo_api"]["password"]
    content_type = "application/json"

    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, user, password)

    handler = urllib2.HTTPBasicAuthHandler(p)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

    req = urllib2.Request(url)
    req.add_header('Content-Type', content_type)
    req.add_header('User-Agent', "setup tool")
    resp = urllib2.urlopen(req)

    my_globals["repoJSON"] = json.loads(resp.read())

    # Pretty print for debugging
    # print json.dumps(my_globals["repoJSON"], sort_keys=True, indent=2, separators=(',', ': '))

    # save to file
    with open(os.environ['HOME'] +
              "/.PUNCH/current_beanstalk_repos.json", "w") as outFile:
        json.dump(my_globals["repoJSON"], outFile)

    # print repo names for user
    my_globals["allTitles"] = []
    for repo in my_globals["repoJSON"]:
        my_globals["allTitles"].append(repo["repository"]["title"])
    # print ", ".join(my_globals["allTitles"])
    # Columns!
    allTitles = my_globals["allTitles"]
    longestName = 0
    for name in allTitles:
        l = len(name)
        if l > longestName:
            longestName = l + 1

    cols = int(math.floor(80/longestName))

    split = [allTitles[i:i+len(allTitles)/cols]
             for i in range(0, len(allTitles), len(allTitles)/cols)]
    for row in zip(*split):
        print "".join(str.ljust(str(i), longestName) for i in row)


if __name__ == "__main__":
    getRepositories()
