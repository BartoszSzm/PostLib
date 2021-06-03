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

