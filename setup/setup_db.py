#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Existing project:
#   select repo (2/2)
#   clone locally
#  >setup db
#       create local db
#       pull name from project config file
#       pull u/p from computer config file
#   pull staging db and import to local
#       pull h/u/p from config file in project
#   npm install (as needed)

from global_var import *
from lib import sh
# import mysql.connector
mysql = sh.Command("/Applications/MAMP/Library/bin/mysql")


def create_db(dbname, my_globals):
    # print ''.join(["/Applications/MAMP/Library/bin/mysql",
    #                " -u ", my_globals["database"]["username"],
    #                " -p", my_globals["database"]["password"],
    #                ' -e "create database ', dbname, '"'])
    create_string = ' '.join(['create', 'database', dbname[0]])
    print ""
    print "Creating database."
    mysql(
        "".join(["-p", my_globals["database"]["password"]]),
        u=my_globals["database"]["username"],
        e=create_string
    )
    # pass


def populate_local_db(my_globals):
    dump = pull_from_remote(my_globals)
    pass


def find_database_name(my_globals):
    grunt_package = "package.json"
    project_config = []
    db_name = []

    print ""
    print "Looking for", grunt_package

    import json
    for root, dirs, files in os.walk(my_globals["SITE_DIR"]):
        # try to find grunt config
        if "assets" in root.split('/') and grunt_package in files:
            project_config.append(os.path.join(root, grunt_package))
            print "I found " + ', '.join(project_config)

        # if len(project_config) == 1:
            with open(project_config[0]) as f:
                raw = f.read()
            cfg = json.loads(''.join(raw))

            if hasattr(cfg, 'database') and cfg['database'] not in db_name:
                db_name.append(cfg['database'])

        # trying to pull data from master config
        staging_file = "config.stage.php"

        if "config" in root.split('/') and staging_file in files:
            print "Found master config"

            with open(os.path.join(root, staging_file)) as f:
                master_raw = f.read()

            # Take the Master Config infor and turn it to a dict
            staging_db_config = master_config_to_dict(master_raw)

            # Save it in globals
            my_globals["staging"]["database"] = staging_db_config
            # print my_globals
            # print "-----"
            if staging_db_config['database'] not in db_name:
                db_name.append(staging_db_config['database'])
    # print ""

    if len(db_name) is 1:
        my_globals["db_name"] = db_name
    else:
        my_globals["db_name"] = raw_input("Database name (%s):"
                                          % "|".join(db_name))

    if my_globals["db_name"]:
        create_db(my_globals["db_name"], my_globals)
    else:
        import sys
        sys.exit()

    pass


def master_config_to_dict(raw):
    import re
    config_lines = re.findall("\$env_db\[.*\n", raw)
    cfg = {}
    for item in config_lines:
        # print item
        # Expecting `$env_db['database'] = 'dbname';`
        # split on quotes
        item = re.split('["'+"']", item)
        cfg[item[1]] = item[3]

    return cfg


def pull_from_remote(my_globals):
    import os
    import re
    # global my_globals
    print ""
    print "Pull db from remote"
    dump_file = ''.join([os.environ['HOME'], '/.PUNCH/temp.dump.sql'])

    if not "database" in my_globals["staging"]:
        host = raw_input("Staging DB host: (localhost) ")
        user = raw_input("Staging DB user name: (punchrva_devs) ")
        passwd = raw_input("Staging DB password:")

        # if ssh_host == "":
        #     ssh_host = "punchrva@web328.webfaction.com"
        # if host == "":
        #     host = "localhost"
        # if user == "":
        #     user = "punchrva_devs"

        passwd = ''.join(['"', re.escape(passwd), '"'])
        ssh_host.split('@')

        my_globals["staging"]["database"] = {
            'username': user,
            'password': password,
            'hostname': host,
            'database': my_globals["db_name"],
            'url': ssh_host[1]
        }

    # ********************************************************
    # need to pull from staging object in globals

    print ""
    print "pulling from staging"
    ssh_url = ''.join([my_globals["staging"]["username"],
                      "@",
                      my_globals["staging"]["url"]])
    import re
    escaped_password = re.escape(my_globals["staging"]["database"]["password"])

    # print sh.ssh(ssh_url, "ls")
    my_server = sh.ssh.bake(ssh_url)
    my_server.wait()
    print "Downloading staging database."
    my_server.mysqldump(my_globals["db_name"],
                        u=my_globals["staging"]["database"]["username"],
                        password=escaped_password,
                        _out=dump_file)
    print ""

    # tail(my_server.mysqldump("punchrva_sandbox",
    #                          ''.join(["--password=", passwd]),
    #                          u=user,
    #                          _out=dump_file))

    print "Importing into local database."
    # sql_information = ""
    # with open(dump_file, "r") as f:
    #     sql_information = f.read()

    os.system(
        " ".join(["/Applications/MAMP/Library/bin/mysql",
                 "-u", my_globals["database"]["username"],
                 "--password="+my_globals["database"]["password"],
                 my_globals["db_name"][0],
                 "<",
                 dump_file])
    )

    # mysql(
    #     my_globals["db_name"],
    #     u=my_globals["database"]["username"],
    #     password=my_globals["database"]["password"],
    #     _in=dump_file
    # )
    print "Database added."
