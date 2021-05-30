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

#TODO - THINK ABOUT NAME OF APP
#TODO - Now app can be installed via pip3 install (dir with setup.py), think about database setup

#TODO - Create 'Browse issues' window - realy needed
#TODO - Create pg_dump file with db and test db
#TODO - On github in instruction write about how to get all records 
