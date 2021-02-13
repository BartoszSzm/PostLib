# File contains functions prepared to retrieve or save data from/to database


import psycopg2 as db


PARAMS = {
'database' : 'pi',
'user' : 'pi',
'password' : 'Haslolinux4',
'host' : '192.168.1.24',
'port' : '5432'
}

class PostgresConnectionManager():
    """Context manager to connect to PostgresSQL. Set 'returns' value to True
    if you are retrieving data from db"""
    
    def __init__(self, conn_params, returns= False):
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


    
            

    
