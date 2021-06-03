from setuptools import setup

def readme():
    with open('README.md','r') as readme:
        return readme.read()
    
setup(
   name='LMS',
   version='1.0',
   description='Library management system with Postgresql under hood',
   author='Bartosz Szmyt',
   author_email='bartoszszmyt0@gmail.com',
   packages=['buttons','images','tests'],
   install_requires=['babel', 'configparser', 'pillow', 'psycopg2', 'pytz', 'tkcalendar'],
)

#TODO - THINK ABOUT NAME OF APP - POSTLIB
#TODO - Now app can be installed via pip3 install (dir with setup.py), think about database setup


#TODO -postlib_db.sql is the file with db dump - to create db from it must be logged as postgres
#Then CREATE DATABASE postlib; then psql < postlib_db.sql. After that database will be created 
#Fix the problem with logging when db was created on localhost (authentication)

#TODO - On github in instruction write about how to get all records 
