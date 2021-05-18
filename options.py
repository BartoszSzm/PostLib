"""File contains options variables definitions. Data is aquired from config.ini"""

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

PENALTY = float(config['OTHERS']['penalty'])
ISSUE_LIMIT = int(config['OTHERS']['issue_limit'])
PASSWORD = str(config['OTHERS']['password'])
DB_CONN_PARAMS = dict(config['DB_CONN_PARAMS'])


