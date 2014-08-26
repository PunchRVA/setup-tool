#!/usr/bin/env python

# Steps to set up a comuter for production work:
# 1. Set conneciton to db
# 2. Set up project directory
# 3. Set up SSH key


import os
import json
import urllib2
import requests
from requests.auth import HTTPBasicAuth
from os.path import exists

# globals
my_globals = {}

# config object
cfg = {
    "local_hostname": "localhost",
    "local_username": "root",
    "local_password": "root",
    "projects_dir": "~/Sites/"
}


def configure_my_computer(gobal_vars):
    global my_globals
    my_globals.update(gobal_vars)
    # setup_environments()
    configure_db()
    setup_project_folder()
    get_remote_info()
    write_config()
    return cfg


def setup_environments():
    try:
        with open(my_globals['HOME'] +
                  "/.PUNCH/config.json") as f:
            raw = f.read()
        envs = json.loads(''.join(raw))

    except:
        "Let's get remote environment credentials."
        envs = {}
        print "What is your staging environment's:"
        url = raw_input('server url ' +
                        '(like "web320.webfaction.com"): ')
        username = raw_input('user name: ')
        password = raw_input('password: ')
        staging = {
            "url": url,
            "username": username,
            "password": password
        }

        envs["staging"] = staging
        return envs
    pass


def configure_db():
    global cfg

    db_connection = raw_input("What's the database host name? (localhost)  ")
    db_user = raw_input("What's the user name to your database? (root)  ")
    db_pass = raw_input("What's the password to your database? (root)  ")

    if db_connection is not '':
        cfg["local_hostname"] = db_connection

    if db_user is not '':
        cfg["local_username"] = db_user

    if db_pass is not '':
        cfg["local_password"] = db_pass


def get_remote_info():
    remotes = {
        "staging": {},
        "repo": {}
    }

    remotes["staging"]["host"] = raw_input("What")
    pass


def home_to_absolute_path(str):
    return str.replace('~', os.environ['HOME'])


def setup_project_folder():

    projects_folder = \
        raw_input("What folder are all your projects in? (~/Sites/) ")

    if (projects_folder is ''):
        projects_folder = cfg['projects_dir']

    projects_folder = home_to_absolute_path(projects_folder)

    print 'looking for ' + projects_folder
    if not exists(projects_folder):
        os.mkdir(projects_folder)
        print 'made ' + projects_folder
    cfg["projects_dir"] = projects_folder
    pass


def write_config():
    global my_globals
    pch_dir = os.environ['HOME'] + "/.PUNCH/"
    if not exists(pch_dir):
        os.mkdir(pch_dir)

    # save to file
    with open(pch_dir + "config.json", "w") as outFile:
        json.dump(cfg, outFile)

    my_globals.update(cfg)


def setup_SSH_key():
    ssh_dir = os.environ['HOME'] + '/.ssh/'
    if not exists(ssh_dir):
        os.mkdir(ssh_dir)
    if exists(ssh_dir + "id_rsa.pub"):
        return True
    else:
        os.chdir(ssh_dir)
        create_ssh_key = os.system('ssh-keygen -t rsa')
        if create_ssh_key is not 0:
            setup_SSH_key()
        send_ssh_to_webfaction()
        send_SSH_key_to_beanstalk()

    pass


def send_SSH_key_to_beanstalk():
    base_url = "https://punchrva.beanstalkapp.com/api/"
    public_key_url = base_url + "public_keys.json"
    users_url = base_url + "users.json"
    user = "chrisma"
    password = "692b2b0c6872274106058d4b51c7552d6494b623528339f47f"
    content_type = "application/json"

    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, base_url, user, password)

    handler = urllib2.HTTPBasicAuthHandler(p)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

    user_json = get_user_list()
    userList = []
    for record in user_json:
        userList.append(record['user']['login'])

    chosen_user = choose_user(userList, 0)

    user_id = ''
    for record in user_json:
        if record['user']['login'] == chosen_user:
            user_id = record['user']['id']

    with open(os.environ["HOME"] + "/.ssh/id_rsa.pub", "r") as pub_key:
        this_public_key = pub_key.read()
    data = {
        "user_id": str(user_id),
        "public_key": {"content": this_public_key}
    }

    print "this will send"
    print data

    headers = {
        'content-type': content_type,
        'user-agent': "setup tool-add public key"
    }

    req = requests.post(
        public_key_url,
        data=json.dumps(data),
        headers=headers,
        auth=HTTPBasicAuth(user, password)
    )

    if not req.ok:
        print "Error with uploading to Beanstalk."
        import pprint
        import sys
        pprint.pprint(req)
        print req.content
        print req.text
        print req.headers
        print req.status_code
        sys.exit()
    pass


def choose_user(user_list, errorCount):
    os.system('clear')
    if errorCount > 0:
        print "User name not found."
        print ""
    print "Beanstalk users:"
    print ', '.join(user_list)

    this_username = raw_input("What is your username on Beanstalk? ")
    if this_username not in user_list:
        errorCount += 1
        if errorCount is 7:
            import sys
            print "Sorry."
            os.remove(os.environ['HOME'] + "/.ssh/id_rsa.pub")
            os.remove(os.environ['HOME'] + "/.ssh/id_rsa")
            sys.exit()

        choose_user(user_list, errorCount)
    else:
        return this_username


def get_user_list():
    base_url = "https://punchrva.beanstalkapp.com/api/"
    users_url = base_url + "users.json"
    content_type = "application/json"

    user_req = urllib2.Request(users_url)
    user_req.add_header('Content-Type', content_type)
    user_req.add_header('User-Agent', "setup tool-add public key")
    raw_users = urllib2.urlopen(user_req)
    user_json = json.loads(raw_users.read())
    return user_json


def send_ssh_to_webfaction():
    import xmlrpclib
    from sh import scp

    # Secure copy public key to staging
    scp(
        '~/.ssh/id_rsa.pub',
        'punchrva@web328.webfaction.com:temp_id_rsa_key.pub'
    )

    server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
    session_id, account = server.login('punchrva', '163553fb')
    server.system(session_id,
                  "cat ~/temp_id_rsa_key.pub >> ~/.ssh/authorized_keys")
    server.system(session_id, "rm ~/temp_id_rsa_key.pub")

    pass
