"""File contains options variables definitions. Data is aquired from config.ini"""

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

PENALTY = float(config['OTHERS']['penalty'])
ISSUE_LIMIT = int(config['OTHERS']['issue_limit'])
PASSWORD = str(config['OTHERS']['password'])
DB_CONN_PARAMS = dict(config['DB_CONN_PARAMS'])
TEST_DB_CONN_PARAMS = dict(config['TEST_DB_CONN_PARAMS'])

