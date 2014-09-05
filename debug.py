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

try:
    with open(HOME + "/.PUNCH/config.json") as f:
        raw = f.read()
    cfg = json.loads(''.join(raw))
    my_globals.update(cfg)

except:
    print "You need to set up your computer."
    # cfg = configure_my_computer(my_globals)
    # quit()


try:
    my_globals["SITE_DIR"] = "/Users/bashit/Sites/primate-rescue-center"
    find_database_name(my_globals)
    populate_local_db(my_globals)
except:
    from pprint import pprint as pp
    print "-----***--------------------------------"
    pp(my_globals)
    print "-----***--------------------------------"
    raise
