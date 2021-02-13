""" All tests for db_functions file"""

import unittest
from buttons import db_functions as db_func
import psycopg2 as db

class TestContextManager(unittest.TestCase):
    """Test all db functions"""
    
    def test_db_context_manager(self):
        """Test if context manager opens connection and cursor and closing all
        after leaving with block"""
        
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
    'host' : '192.168.1.24',
    'port' : '5432'
    }
     
    def setUp(self):
        self.conn = db.connect(**self.TEST_PARAMS) 
        self.cursor = self.conn.cursor()    
       
    def test_save_book(self):
        """Test save_book() function on test database"""
        
        # Create some test data to save
        self.test_data = ('Title','Author','Kind','Publisher',1993,
                          'Language',100,'ISBN')
        
        # Save it to database using function from db_functions
        db_func.save_book(self.test_data, conn_params=self.TEST_PARAMS)
        
        # Check saved record
        self.cursor.execute('SELECT * FROM publications WHERE lib_id > 100;')
        results = self.cursor.fetchone()
        self.assertEqual(self.test_data, results[1:9])
        
        # Delete created test_record
        self.cursor.execute('DELETE FROM publications WHERE lib_id > 100;')
        self.conn.commit()
        
        # Test if function handles expectations properly
    
    def tearDown(self):
        self.cursor.close()
        self.conn.close()
          
        
if __name__ == "__main__":
    unittest.main()
            
        
    