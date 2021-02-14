""" All tests for db_functions file"""

import unittest
from unittest.case import skipIf
from buttons import db_functions as db_func
from ddt import ddt, data
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

@ddt   
class TestDbFunctions(unittest.TestCase):
    """Test all functions that make contact whith db"""
 
    TEST_PARAMS = {
    'database' : 'test',
    'user' : 'pi',
    'password' : 'Haslolinux4',
    'host' : '192.168.1.24',
    'port' : '5432'
    }
    
    SAVE_BOOK_TEST_DATA = (
                ('Title','Author','Kind','Publisher',1993,'Language',100,'ISBN'),
                ('Title','Author','Kind','Publisher','','Language',100,'ISBN'),
                ('Title','','Kind','Publisher',1993,'Language',100,'ISBN'),
                ('','Author','Kind','Publisher',1993,'Language',100,'ISBN'),
                ('Title','Author','Kind','',1993,'Language',100,'ISBN'))
    
    GET_RESULTS_TEST_DATA = (
    ('lib_id','5', (5,'Bigfoot Lives','Hermy Ashbe','Adventure|Documentary|Drama','Dryden',2000,'Albanian','306','694852980-1',False)),
    ('author','Rosanna Agnew', (75,'2:37','Rosanna Agnew',None,'Atwood',2005,'Greek',None,None,False)),
    ('title','Moja Ksiazka', (None)),
    ('lib_id', 'a', ('Error here')),
    ('is_issued', 5, ('Error here')), 
    )
    
    def setUp(self):
        self.conn = db.connect(**self.TEST_PARAMS) 
        self.cursor = self.conn.cursor()    
    
    @data(*SAVE_BOOK_TEST_DATA)
    def test_save_book(self, data_list):
        """Test save_book() function on test database"""
        
        # Save it to database using function from db_functions
        try:
            db_func.save_book(data_list, conn_params=self.TEST_PARAMS)
        
            # Check saved record
            self.cursor.execute('SELECT * FROM publications WHERE lib_id > 100;')
            results = self.cursor.fetchone()
            self.assertEqual(data_list, results[1:9])
            
            # Delete created test_record
            self.cursor.execute('DELETE FROM publications WHERE lib_id > 100;')
            self.conn.commit()
        
        # Check expections handling
        except db.IntegrityError:
            for item in data_list:
                if item == '':
                    self.index = data_list.index(item)
            self.assertIn(self.index, (0,1,3,4))
            
        except db.DataError:
            self.assertEqual(data_list[4],'')
    
    @data(*GET_RESULTS_TEST_DATA)
    def test_get_results_by(self, data_list):
        """Test if func returns valid data"""
        # In try except use tested func in for loop, make asertion 
        try:
            for result in db_func.get_results_by(data_list[0],data_list[1]):
                self.assertTupleEqual(result, data_list[2])
        # Check exceptions handling
        except db.DataError:
            if data_list[0] == 'is_issued':
                self.assertNotIsInstance(data_list[1], bool)
            else:
                self.assertNotIsInstance(data_list[1], int)

    
    def tearDown(self):
        self.cursor.close()
        self.conn.close()
          
        
if __name__ == "__main__":
    unittest.main()
            
        
    