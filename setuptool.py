#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Update itself
# import sh
# updated = sh.git('pull')
# if updated == "Already up-to-date."

import os
from os.path import exists
import json

# constants
HOME = os.environ['HOME']
PUNCHDIR = HOME + '/.PUNCH'


cfg = {}
my_globals = {
    # Conputer config
    "HOME": HOME,

    # Local collection of repos
    "repoJSON": None,
    "allTitles": []
}

from setup.get_repos import *
from setup.download_repo import *
from setup.setup_db import *
from setup.configure_computer import *

print HOME
try:
    with open(HOME + "/.PUNCH/config.json") as f:
        raw = f.read()
    cfg = json.loads(''.join(raw))

except:
    print "You need to set up your computer."
    cfg = configure_my_computer(my_globals)
    # quit()

my_globals.update(cfg)

if not exists(my_globals['projects_dir']):
    os.mkdir(my_globals['projects_dir'])

# Checking for PUNCH folder and config file
# pch_dir = HOME + "/.PUNCH/"
# if not exists(pch_dir):
#     os.mkdir(pch_dir)
#     configure_my_computer()
#     pass

if not exists(HOME + '/.ssh/id_rsa'):
    # setup_SSH_key()
    print "You need to set up ssh keys"
    quit()


# Start it all off
os.system('clear')
whatarewedoing = raw_input('new or existing project? (n/e) ')
if whatarewedoing == "e":

    try:
        # Existing project:
        #   download list of repos
        getRepositories(my_globals)
        #   select repo
        #   clone locally
        ask_for_name(my_globals)
        #   setup db
        #       pull name from project config file
        find_database_name(my_globals)
        #       pull u/p from computer config file
        #       create local db
        populate_local_db(my_globals)
        #   pull staging db and import to local
        #       pull h/u/p from config file in project
        #   npm install (as needed)
    except:
        from pprint import pprint as pp
        print "-----***--------------------------------"
        pp(my_globals)
        print "-----***--------------------------------"
        raise

elif whatarewedoing == "n":
    print "Sorry, that's not ready yet."
    print my_globals


    # New project:
    #   create local repo
    #   make first commit
    #   create beanstalk repo, push first commit
    #   Create config data
    #   create db
    #   download software (when available)
    #   copy package.json and Gruntfile from .PUNCH
    #   NPM install
    #   create staging environment(?) (https://docs.webfaction.com/xmlrpc-api/)
else:
    print ' '.join(["Can't help you right now.",
                   "Try again. Next time type",
                   '"e" or "n".'])
