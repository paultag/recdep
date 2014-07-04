#!/bin/bash

./manage.py sqlclear recdep | ./manage.py dbshell
./manage.py syncdb
./manage.py migrate
