# File contains functions prepared to retrieve or save data from/to database

import psycopg2 as db
from LMS.options import DB_CONN_PARAMS

PARAMS = DB_CONN_PARAMS

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
        if self.returns == False and not exc_type:
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
     
def get_results_by(parameter, value, table='publications', conn_params=PARAMS):
    """Returns records by given parameter from publications"""
    with PostgresConnectionManager(conn_params, returns=True) as postgres:
        if parameter in ('title', 'author', 'kind', 'publisher', 'language',
                         'full_name', 'email'):
                postgres.cursor.execute(f"SELECT * FROM {table} "
                        f"WHERE {parameter} LIKE '{value+'%'}';")
        else:
            postgres.cursor.execute(f"SELECT * FROM {table} "
                        f"WHERE {parameter}='{value}';")       
        for result in postgres.cursor:
            yield result

def delete_record_by(id, value, table, conn_params=PARAMS):
    """Delete single record with given lib_id"""
    with PostgresConnectionManager(conn_params) as postgres:
        postgres.cursor.execute(f"DELETE FROM {table} "
                                f"WHERE {id} = '{value}';")
        
def save_reader(data, conn_params=PARAMS):
    """Save reader data to db"""
    with PostgresConnectionManager(conn_params) as postgres:
        postgres.cursor.execute(f'INSERT INTO person '
                                f'(full_name, phone_number, email, id_card)'
                                f' VALUES {tuple(data)}')

def save_issue(data, conn_params=PARAMS):
    """Save new issue to db (data - lib_id, reader_id, issue_limit)"""
    with PostgresConnectionManager(conn_params) as postgres:
        postgres.cursor.execute(f'INSERT INTO issue '
                                f'(lib_id, reader_id, issue_limit) '
                                f'VALUES {tuple(data)}')

def show_issues(reader_id, conn_params=PARAMS):
    """Return all issues for given reader_id (genetator)"""
    with PostgresConnectionManager(conn_params, returns=True) as postgres:
        postgres.cursor.execute(f"SELECT title,author,isbn, issue.* " 
                                f"FROM publications INNER JOIN issue "
                                f"ON publications.lib_id = issue.lib_id "
                                f"WHERE reader_id ='{reader_id}' ORDER BY returned_date DESC;")
        for result in postgres.cursor:
            yield result

def return_book(issue_id, returned_date, imposed_penalty, conn_params=PARAMS):
    """Update record with return_date and imposed_penalty"""
    with PostgresConnectionManager(conn_params) as postgres:
        postgres.cursor.execute(f"UPDATE issue SET returned_date = '{returned_date}', "
                                f"imposed_penalty='{imposed_penalty}' "
                                f"WHERE issue_id = {issue_id}")


            

    
