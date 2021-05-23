""" All tests for db_functions file"""

import decimal
import unittest
from unittest.case import TestCase

from LMS.buttons import db_functions as db_func
from LMS import options

import psycopg2 as db
from psycopg2.errors import lookup
from psycopg2 import errorcodes

from datetime import date, timedelta
#pylint: disable=unused-variable 

TEST_PARAMS = options.TEST_DB_CONN_PARAMS

class TestContextManager(unittest.TestCase):
    """Test all db functions"""
    
    def test_db_context_manager(self):
        """Test if context manager opens connection and cursor and closing all
        after leaving 'with' block"""
        
        with db_func.PostgresConnectionManager(TEST_PARAMS) as postgres:
            self.assertFalse(postgres.conn.closed)
            self.assertFalse(postgres.cursor.closed)   
        self.assertTrue(postgres.conn.closed)
        self.assertTrue(postgres.cursor.closed)
        
class TestSaveBook(unittest.TestCase):
    """Test save_book() function"""
    
    @classmethod
    def setUpClass(self):
        self.conn = db.connect(**TEST_PARAMS)
        self.cursor = self.conn.cursor()
    
    def test_save_book_save(self):
        """Test if save_book() saving data to db correctly"""
        data_list = ('Title','Author','Kind','Publisher',1993,'Language','100','ISBN')  
        db_func.save_book(data_list, conn_params=TEST_PARAMS)
        self.cursor.execute("SELECT * FROM publications WHERE title = 'Title' AND author = 'Author';")
        results = self.cursor.fetchone()
        self.assertEqual(data_list, results[1:9])   
        
    def test_save_book_integrity_error(self):
        """Test if method raises CheckViolation correctly - constraint 'not empty"""   
        data_list = (('Title','','Kind','Publisher',1993,'Language',100,'ISBN'),
                    ('','Author','Kind','Publisher',1993,'Language',100,'ISBN'),
                    ('Title','Author','Kind','',1993,'Language',100,'ISBN'))               
        for data in data_list:
            with self.assertRaises(lookup(errorcodes.CHECK_VIOLATION)):
                db_func.save_book(data, conn_params=TEST_PARAMS)
    
    def test_save_book_data_error(self):
        """Test if method raises InvalidTextRepresentation correctly - int expected"""  
        data_list = ('Title','Author','Kind','Publisher','','Language',100,'ISBN')
        with self.assertRaises(lookup(errorcodes.INVALID_TEXT_REPRESENTATION)):
            db_func.save_book(data_list, conn_params=TEST_PARAMS)

    @classmethod
    def tearDownClass(self):
        """Delete test record, close connection"""
        self.cursor.execute("DELETE FROM publications WHERE title = 'Title' AND author = 'Author';")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class TestGetResultsBy(unittest.TestCase):
    """Test get_results_by() method"""
    
    @classmethod
    def setUpClass(self):
        self.conn = db.connect(**TEST_PARAMS)
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO publications (lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn, is_issued)"
                            " VALUES (1500, 'title', 'author', 'kind', 'publisher', 1993, 'language', '203','ISBN','False')")
        self.cursor.execute("INSERT INTO publications (lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn, is_issued)"
                            " VALUES (1501, 'python', 'django', 'flask', 'tkinter', 1990, 'numpy', '200','0000','False')")
        self.cursor.execute("INSERT INTO publications (lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn, is_issued)"
                            " VALUES (1502, 'computer', 'ssd', 'ram', 'intel', 2000, 'delphi', '205','1111','False')")
        self.cursor.execute("INSERT INTO PERSON (reader_id, full_name, phone_number, email, id_card, total_penalty)"
                            " VALUES (1503, 'bartosz', '123123123', 'bartosz@bartosz', '123', 10.50)")
        self.conn.commit()
        
    def test_get_results_by(self):
        """Test if get_results_by() returns valid data from db"""
        data_list = (('lib_id','1500', (1500,'title','author','kind','publisher',1993,'language','203','ISBN',False)),
                    ('author','python', (1501,'python','django','flask','tkinter',1990,'numpy',200,0000,False)),
                    ('title','Moja Ksiazka', (None)))
        for data in data_list:
            for result in db_func.get_results_by(data[0],data[1], conn_params=TEST_PARAMS):
                self.assertEqual(result, data[2])
                
    def test_get_results_by_invalid_text_representation(self):
        """Test if get_results_by() rises INVALID_TEXT_REPRESENTATION correctly"""
        data_list = (('lib_id', 'a'),
                     ('is_issued', 5))
        with self.assertRaises(lookup(errorcodes.INVALID_TEXT_REPRESENTATION)):
            for data in data_list:
                for result in db_func.get_results_by(data[0], data[1], conn_params=TEST_PARAMS):
                    pass

    def test_get_results_by_different_table(self):
        """Test if get_results_by() get record from another table also"""
        data_list = (('reader_id','1503', (1503,'bartosz','123123123','bartosz@bartosz','123',10.50)),)
        for data in data_list:
            for result in db_func.get_results_by(data[0],data[1], table='person',conn_params=TEST_PARAMS):
                self.assertEqual(result, data[2])    

    @classmethod
    def tearDownClass(self):
        self.cursor.execute('DELETE FROM publications WHERE lib_id BETWEEN 1500 AND 1502')
        self.cursor.execute('DELETE FROM person WHERE reader_id = 1503')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
                    
class TestDeleteRecordBy(unittest.TestCase):
    """Test delete_record_by() from db_functions"""
    
    def setUp(self):
        self.conn = db.connect(**TEST_PARAMS)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"INSERT INTO publications"
                    f"(lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn)"
                    f"VALUES (100,'text','text','text','text',1993,'text','100','text');")        
        self.cursor.execute(f"INSERT INTO person"
                    f"(reader_id, full_name, phone_number, email, id_card) "
                    f"VALUES (105, 'text', 'text', 'text', 'text');")
        self.cursor.execute(f"INSERT INTO issue (issue_id, lib_id, reader_id, issue_limit) "
                            f"VALUES (110, 100, 105, '2100-04-17')")
        self.conn.commit()

    def test_delete_record_by_foreign_key_violation(self):
        """Test if delete_record_by() raises foreign_key_violation correctly"""
        with self.assertRaises(lookup(errorcodes.FOREIGN_KEY_VIOLATION)):
            db_func.delete_record_by('lib_id', '100', 'publications', conn_params=TEST_PARAMS)     

    def test_delete_record_by(self):
        """Test if delete_record_by() deletes record by given lib_id"""

        self.cursor.execute(f'DELETE FROM issue WHERE issue_id = 110')
        self.conn.commit()
        
        # Delete test records using tested func
        db_func.delete_record_by('lib_id',100,'publications',conn_params=TEST_PARAMS)
        db_func.delete_record_by('reader_id',105,'person',conn_params=TEST_PARAMS)
            
        # Check if records was deleted
        self.cursor.execute(f'SELECT * FROM publications WHERE lib_id = 100')
        self.cursor.execute(f'SELECT * FROM person WHERE reader_id = 105')
        for record in self.cursor:
            self.assertTrue(record == None)      
    
    def test_delete_record_by_invalid_text_representation_publications(self):
        """Test if delete_record_by() raises invalid_text_representation correctly"""
        with self.assertRaises(lookup(errorcodes.INVALID_TEXT_REPRESENTATION)):
            db_func.delete_record_by('lib_id', 'abc', 'publications', conn_params=TEST_PARAMS)

    def test_delete_record_by_invalid_text_representation_person(self):
        """Test if delete_record_by() raises invalid_text_representation correctly"""
        with self.assertRaises(lookup(errorcodes.INVALID_TEXT_REPRESENTATION)):
            db_func.delete_record_by('reader_id', 'abc', 'person', conn_params=TEST_PARAMS)

    def tearDown(self):
        self.cursor.execute(f'DELETE FROM issue WHERE issue_id = 110')
        self.cursor.execute(f'DELETE FROM publications WHERE lib_id = 100')
        self.cursor.execute(f'DELETE FROM person WHERE reader_id = 105')
        self.conn.commit()
        self.cursor.close()
        self.conn.close() 

class TestSaveReader(unittest.TestCase):
    """Test save_reader() function from db_functions"""
    
    @classmethod
    def setUpClass(self):
        self.conn = db.connect(**TEST_PARAMS)
        self.cursor = self.conn.cursor()
                                
    def test_save_reader(self):
        """Test if save_reader saving data to db properly"""
        # Create test record
        data_list = ('Full Name','123456789','email@email','ID123')
        db_func.save_reader(data_list,conn_params=TEST_PARAMS)
        # Get saved test record from db
        self.cursor.execute("SELECT * FROM person WHERE full_name = 'Full Name'")
        results = self.cursor.fetchone()
        # Assert
        self.assertEqual(results[1:5], data_list)
        self.cursor.execute("DELETE FROM person WHERE full_name = 'Full Name'")
        self.conn.commit()
    
    def test_save_reader_not_empty_error(self):
        """Test if function properly raising check constriant violation"""
        data_list = (('','123456789','email@email','ID123'),
                    ('Full Name','123456789','email@email',''))
        for data in data_list:
            with self.assertRaises(lookup(errorcodes.CHECK_VIOLATION)):
                db_func.save_reader(data, conn_params=TEST_PARAMS)
    
    def test_save_reader_unique_violation_error(self):
        """Test if function properly raising unique violation error"""
        self.cursor.execute(f"INSERT INTO person"
                            f" (full_name, phone_number, email, id_card)"
                            f" VALUES('Bartosz', '123123', 'email@email', '123123');")
        self.conn.commit()
        
        data = ('Bartosz','123123','email@email','123123')
        with self.assertRaises(lookup(errorcodes.UNIQUE_VIOLATION)):
            db_func.save_reader(data, conn_params=TEST_PARAMS)
        
        self.cursor.execute(f"DELETE FROM person WHERE full_name='Bartosz' AND "
                            f"email = 'email@email';")
        self.conn.commit()
    
    @classmethod                          
    def tearDownClass(self):
        self.cursor.close()
        self.conn.close()

class TestSaveIssue(TestCase):
    """All test for save_issue function"""
    
    def setUp(self):
        self.conn = db.connect(**TEST_PARAMS)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"INSERT INTO publications"
                    f"(lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn)"
                    f"VALUES (100,'text','text','text','text',1993,'text','100','text');")        
        self.cursor.execute(f"INSERT INTO person"
                    f"(reader_id, full_name, phone_number, email, id_card) "
                    f"VALUES (105, 'text', 'text', 'text', 'text');")
        self.conn.commit()        
        self.today = date.today()
        self.month_issue_limit = date.today()+timedelta(30)

    def test_save_issue(self):
        """Test if save_issue making new issue in db correctly with correct data"""
        # Create test record
        data = ['100','105', str(self.month_issue_limit)]
        db_func.save_issue(data, conn_params=TEST_PARAMS)
        
        # Assert this record
        self.cursor.execute('SELECT * FROM issue WHERE lib_id=100 AND reader_id=105')
        result = self.cursor.fetchone()
        self.assertEqual(result[1:], 
                         (100, 105, self.today, self.month_issue_limit, None, None, None))
    
    def test_save_issue_foreign_key_violation(self):
        """Test raising foreign key violation error when saving issue"""
        test_data = [(1, 105, str(self.month_issue_limit)),
                     (3, 105, str(self.month_issue_limit)),
                     (1, 86, str(self.month_issue_limit))]
        for data in test_data:
            with self.assertRaises(lookup(errorcodes.FOREIGN_KEY_VIOLATION)):
                db_func.save_issue(data, conn_params=TEST_PARAMS)
    
    def test_save_issue_invalid_text_representation(self):
        """Test if method raising error when wrong data type was given"""
        test_data = [('', '', str(self.month_issue_limit)),
                     (100, '', str(self.month_issue_limit)),
                     ('', 105, str(self.month_issue_limit))]
        for data in test_data:
            with self.assertRaises(lookup(errorcodes.INVALID_TEXT_REPRESENTATION)):
                db_func.save_issue(data, conn_params=TEST_PARAMS)
   
    def test_save_issue_invalid_invalid_datetime_format(self):
        """Test if method raising error when date was typed in wrong way"""
        test_data = [(100, 105, '124'),
                     (100, 105, 'some data'),
                     (100, 105, '2021-05-'),
                     (100, 105, '20-05-02')]
        for data in test_data:
            with self.assertRaises((lookup(errorcodes.INVALID_DATETIME_FORMAT),
                                    lookup(errorcodes.DATETIME_FIELD_OVERFLOW))):
                db_func.save_issue(data, conn_params=TEST_PARAMS)

    def test_save_issue_check_violation(self):
        """Test if method raising error when issue_limit is lower than issue_date"""
        test_data = [(100, 105, '2000-05-04'),
                     (100, 105, '2021-03-04'),
                     (100, 105, '2021-04-03')]
        for data in test_data:
            with self.assertRaises(lookup(errorcodes.CHECK_VIOLATION)):
                db_func.save_issue(data, conn_params=TEST_PARAMS)

    def test_save_issue_unique_violation(self):
        """Test raising unique_violation error when trying to add already issued book"""
        
        #Add issue
        self.cursor.execute(f"INSERT INTO issue (lib_id, reader_id, issue_limit) "
                            f"VALUES (100, 105, '{self.month_issue_limit}');")
        self.conn.commit()
        
        #Try issue same book
        test_data = [(100, 105, str(self.month_issue_limit))]
        for data in test_data:
            with self.assertRaises(lookup(errorcodes.UNIQUE_VIOLATION)):
                db_func.save_issue(data, conn_params=TEST_PARAMS)  
       
    def tearDown(self):
        self.cursor.execute(f'DELETE FROM issue;')
        self.cursor.execute(f'DELETE FROM publications WHERE lib_id = 100')
        self.cursor.execute(f'DELETE FROM person WHERE reader_id = 105')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()  

         
class TestShowIssues(unittest.TestCase):
    """All tests for show_issues function"""
    def setUp(self):
        self.conn = db.connect(**TEST_PARAMS)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"INSERT INTO publications"
                    f"(lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn)"
                    f"VALUES (100,'text','text','text','text',1993,'text','100','text');")        
        self.cursor.execute(f"INSERT INTO person"
                    f"(reader_id, full_name, phone_number, email, id_card) "
                    f"VALUES (105, 'text', 'text', 'text', 'text');")
        self.cursor.execute(f"INSERT INTO issue (issue_id, lib_id, reader_id, issue_date, issue_limit) "
                            f"VALUES (110, 100, 105, '2021-04-01','2021-05-01')")
        self.conn.commit()
        
    def test_show_issues(self):
        """Test if method gets valid data (inner join publications+issue)"""
        for result in db_func.show_issues(105,conn_params=TEST_PARAMS):
            self.assertEqual(result,
                             ('text','text','text', 110, 100, 105, date(2021,4,1), date(2021,5,1), None, None, None))
    
    def test_show_issues_invalid_text_representation(self):
        """Test if method raises error when invalid data was typed"""
        with self.assertRaises(lookup(errorcodes.INVALID_TEXT_REPRESENTATION)):
             for results in db_func.show_issues('abc', conn_params=TEST_PARAMS):
                pass
    
    def test_show_issues_no_reader_found(self):
        """Test if method returns none when given reader_id not exist"""
        for result in db_func.show_issues(50000, conn_params=TEST_PARAMS):
            self.assertEqual(result, None)  
        
    def tearDown(self):
        self.cursor.execute(f'DELETE FROM issue WHERE issue_id = 110')
        self.cursor.execute(f'DELETE FROM publications WHERE lib_id = 100')
        self.cursor.execute(f'DELETE FROM person WHERE reader_id = 105')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class TestReturnBook(unittest.TestCase):
    """All test for return_book method"""
    def setUp(self):
        self.conn = db.connect(**TEST_PARAMS)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"INSERT INTO publications"
                    f"(lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn)"
                    f"VALUES (100,'text','text','text','text',1993,'text','100','text');")        
        self.cursor.execute(f"INSERT INTO person"
                    f"(reader_id, full_name, phone_number, email, id_card) "
                    f"VALUES (105, 'text', 'text', 'text', 'text');")
        self.cursor.execute(f"INSERT INTO issue (issue_id, lib_id, reader_id, issue_date, issue_limit) "
                            f"VALUES (110, 100, 105, '2021-04-01','2021-05-01')")
        self.conn.commit()

    def test_return_book(self):
        """Test if method updates db record correctly"""
        db_func.return_book(110, '2021-05-02', 0.2, conn_params=TEST_PARAMS)
        self.cursor.execute('SELECT * FROM issue WHERE issue_id = 110;')
        for result in self.cursor:
            self.assertEqual(result,
                             (110, 100, 105, date(2021,4,1), date(2021,5,1), date(2021, 5, 2), 1, decimal.Decimal('0.20')))
    
    def test_return_book_datetime_field_overflow(self):
        """Test if method raises error when invalid date was given"""
        with self.assertRaises(lookup(errorcodes.DATETIME_FIELD_OVERFLOW)):
            db_func.return_book(110, '2021-05-0', 0.2, conn_params=TEST_PARAMS)
            
    def test_return_book_invalid_datetime_format(self):
        """Test if method raises error when invalid date was given"""
        with self.assertRaises(lookup(errorcodes.INVALID_DATETIME_FORMAT)):
            db_func.return_book(110, '2021-05', 0.2, conn_params=TEST_PARAMS)
            
    def test_return_book_invalid_text_representation(self):
        """Test if method raises error when wrong data given as penalty"""
        with self.assertRaises(lookup(errorcodes.INVALID_TEXT_REPRESENTATION)):
            db_func.return_book(100,'2021-04-21', 'abc', conn_params=TEST_PARAMS)
    
        

    def tearDown(self):
        self.cursor.execute(f'DELETE FROM issue WHERE issue_id = 110')
        self.cursor.execute(f'DELETE FROM publications WHERE lib_id = 100')
        self.cursor.execute(f'DELETE FROM person WHERE reader_id = 105')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
          
        
if __name__ == "__main__":
    unittest.main()



# TODO -  Verify test data for each method - some are not neccessary


            
        
    