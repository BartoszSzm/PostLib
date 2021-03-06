# File contains functions prepared to retrieve or save data from/to database
# MAKE DATABASE CONNECTOR

import psycopg2 as db


PARAMS = {
'database' : 'pi',
'user' : 'pi',
'password' : 'Haslolinux4',
'host' : '192.168.1.16',
'port' : '5432'
}

class PostgresConnectionManager():
    """Context manager to connect to PostgresSQL. Set 'returns' value to True
    if you are retrieving data from db"""
    
    def __init__(self, conn_params, returns=False):
        self.conn_params = conn_params
        self.returns = returns
    
    def __enter__(self):
        self.conn = db.connect(**self.conn_params)
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.returns and not exc_type:
            self.conn.commit()
            print("Changes saved to database")
        self.cursor.close()
        self.conn.close()

def save_book(data, conn_params=PARAMS):
    """Save book data to db"""
    with PostgresConnectionManager(conn_params) as postgres:
        postgres.cursor.execute(f'INSERT INTO publications'
                    f'(title, author, kind, publisher, year_of_publish,'
                    f'language, pages, isbn)'
                    f'VALUES {tuple(data)};')
        
def get_results_by(parameter, value, conn_params=PARAMS):
    """Returns records by given parameter"""
    with PostgresConnectionManager(conn_params, returns=True) as postgres:
        postgres.cursor.execute(f"SELECT * FROM publications "
                                f"WHERE {parameter}='{value}';")
        for result in postgres.cursor:
            yield result

def delete_record_by(lib_id, conn_params=PARAMS):
    """Delete single record with given lib_id"""
    with PostgresConnectionManager(conn_params) as postgres:
        postgres.cursor.execute(f'DELETE FROM publications '
                                f'WHERE lib_id = {lib_id};')
            

    
