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


# getRepositories
git pull
clear
# python debug.py
python setuptool.py

exit