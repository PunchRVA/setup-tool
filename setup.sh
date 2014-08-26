#!/bin/bash

# Existing project:
# 	select repo
# 	clone locally
# 	setup db
# 		create local db
# 		pull name from project config file
# 		pull u/p from computer config file
# 	pull staging db and import to local
# 		pull h/u/p from config file in project
# 	npm install (as needed)

# getRepositories() {
# 	curl --user chrisma:692b2b0c6872274106058d4b51c7552d6494b623528339f47f --user-agent "setup-tool" --header "Content-Type:application/json" https://punchrva.beanstalkapp.com/api/repositories.json > ~/.PUNCH/current_beanstalk_repos.json
# 	cat ~/.PUNCH/current_beanstalk_repos.json
# }

# getRepositories
git pull
clear
# python debug.py
python setuptool.py

exit