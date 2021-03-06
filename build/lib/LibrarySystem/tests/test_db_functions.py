""" All tests for db_functions file"""

import unittest
from LibrarySystem.buttons import db_functions as db_func
import psycopg2 as db
#pylint: disable=unused-variable

class TestContextManager(unittest.TestCase):
    """Test all db functions"""
    
    def test_db_context_manager(self):
        """Test if context manager opens connection and cursor and closing all
        after leaving 'with' block"""
        
        with db_func.PostgresConnectionManager(db_func.PARAMS) as postgres:
            self.assertFalse(postgres.conn.closed)
            self.assertFalse(postgres.cursor.closed)   
        self.assertTrue(postgres.conn.closed)
        self.assertTrue(postgres.cursor.closed)

class TestDbFunctions(unittest.TestCase):
    """Test all functions that make contact whith db"""
 
    TEST_PARAMS = {
    'database' : 'test',
    'user' : 'pi',
    'password' : 'Haslolinux4',
    'host' : '192.168.1.16',
    'port' : '5432'
    }
    
    def setUp(self):
        self.conn = db.connect(**self.TEST_PARAMS)
        self.cursor = self.conn.cursor()    
    
    
    def test_save_book_save(self):
        """Test if save_book() saving data to db correctly"""
        data_list = ('Title','Author','Kind','Publisher',1993,'Language',100,'ISBN')  
    # Save it to database using function from db_functions
        db_func.save_book(data_list, conn_params=self.TEST_PARAMS)
    # Check saved record
        self.cursor.execute('SELECT * FROM publications WHERE lib_id > 100;')
        results = self.cursor.fetchone()
        self.assertEqual(data_list, results[1:9])   
    # Delete created test_record
        self.cursor.execute('DELETE FROM publications WHERE lib_id > 100;')
        self.conn.commit()
        
    def test_save_book_integrity_error(self):
        """Test if save_book() responding with IntegrityError correctly"""   
        data_list = (('Title','','Kind','Publisher',1993,'Language',100,'ISBN'),
                    ('','Author','Kind','Publisher',1993,'Language',100,'ISBN'),
                    ('Title','Author','Kind','',1993,'Language',100,'ISBN'))               
        for data in data_list:
            with self.assertRaises(db.IntegrityError):
                db_func.save_book(data, conn_params=self.TEST_PARAMS) 
    
    def test_save_book_data_error(self):
        """Test if save_book() responding with DataError correctly"""  
        data_list = ('Title','Author','Kind','Publisher','','Language',100,'ISBN')
        with self.assertRaises(db.DataError):
            db_func.save_book(data_list, conn_params=self.TEST_PARAMS)

    def test_get_results_by(self):
        """Test if get_results_by() returns valid data from db"""
        data_list = (('lib_id','5', (5,'Bigfoot Lives','Hermy Ashbe','Adventure|Documentary|Drama','Dryden',2000,'Albanian','306','694852980-1',False)),
                    ('author','Rosanna Agnew', (75,'2:37','Rosanna Agnew',None,'Atwood',2005,'Greek',None,None,False)),
                    ('title','Moja Ksiazka', (None)))
        for data in data_list:
            for result in db_func.get_results_by(data[0],data[1]):
                self.assertTupleEqual(result, data[2])
        
    def test_get_results_by_data_error(self):
        """Test if get_results_by() rises DataError correctly"""
        data_list = (('lib_id', 'a'),
                    ('is_issued', 5))
        with self.assertRaises(db.DataError):
            for data in data_list:
                for result in db_func.get_results_by(data[0],data[1]):
                    pass
                    
    def test_delete_record_by(self):
        """Test if delete_record_by() deletes record by given lib_id"""
        data_list = (100, '105')
        for test_data in data_list:
            # Delete record with lib_id = test_data if exist
            self.cursor.execute(f'DELETE FROM publications WHERE lib_id = {test_data}')
            self.conn.commit()
            
            # Make test record
            self.cursor.execute(f"INSERT INTO publications"
                        f"(lib_id, title, author, kind, publisher, year_of_publish,"
                        f"language, pages, isbn)"
                        f"VALUES ({test_data},'text','text','text','text',1993,'text','100','text');")
            self.conn.commit()
        
            # Delete test record using tested func
            db_func.delete_record_by(test_data, conn_params=self.TEST_PARAMS)
            
            # Check if record was deleted
            self.cursor.execute(f'SELECT * FROM publications WHERE lib_id = {test_data}')
            for record in self.cursor:
                self.assertTrue(record == None)
        
    def test_delete_record_by_programming_error(self):
        """Test if delete_record_by() raises programming error correctly"""
        data_list = ('abc', 'text')
        for test_data in data_list:
            with self.assertRaises(db.ProgrammingError):
                db_func.delete_record_by(test_data, conn_params=self.TEST_PARAMS)
               
                  
    def tearDown(self):
        self.cursor.close()
        self.conn.close()
          
        
if __name__ == "__main__":
    unittest.main()
    
# Think about making separate class for each db_functions function
# Verify test data for each method - some are not neccessary

            
        
    