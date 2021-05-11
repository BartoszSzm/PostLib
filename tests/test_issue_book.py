from datetime import date
import unittest
from unittest.mock import Mock

from tkcalendar.dateentry import DateEntry
from LMS.buttons import issue_book
from tkinter import Entry, Tk
from freezegun import freeze_time
from psycopg2 import errorcodes, errors
from datetime import date

class TestIssueBook(unittest.TestCase):
    """Test IssueBook class"""
    @freeze_time('2000-01-01')    
    def setUp(self):
        """Initialize class for tests"""
        self.root = Tk()
        self.issue_book = issue_book.IssueBook(self.root)
        self.lib_id_entry = self.issue_book.entries_list[0]
        self.reader_id_entry = self.issue_book.entries_list[1]
        self.issue_limit_entry = self.issue_book.entries_list[2]
    
    @freeze_time('2000-01-01')
    def test_return_limit(self):
        """Test whether function returns correct return limit date"""
        return_limit = self.issue_book._return_limit()
        self.assertEqual(return_limit, date(2000,1,31))
        self.assertNotEqual(return_limit, date(2000,1,4))
        
    def test_entries_amount(self):
        """Test whether correct amount of entries was created"""
        self.assertEqual(len(self.issue_book.entries_list), 3)
    
    def test_entries_instance(self):
        """Test whether there are two Entry objects and one DateEntry"""
        self.assertIsInstance(self.lib_id_entry, Entry)
        self.assertIsInstance(self.reader_id_entry, Entry)
        self.assertIsInstance(self.issue_limit_entry, DateEntry)
    
    def test_date_entry_date_display(self):
        """Test whether DateEntry displaying correct date when created"""
        self.assertEqual(self.issue_limit_entry.get(), '2000-01-31')
    
    def test_get_entries_data(self):
        """Test whether function retrieves data from entries properly"""
        self.lib_id_entry.insert(0,'some data')
        self.reader_id_entry.insert(0,'some data')
        self.issue_limit_entry.delete(0,'end')
        self.issue_limit_entry.insert(0,'2021-03-15')

        retrieved_data = self.issue_book._get_entries_data()

        self.assertEqual(retrieved_data[0],'some data')
        self.assertEqual(retrieved_data[1],'some data')
        self.assertEqual(retrieved_data[2],'2021-03-15')
    
    def test_clear_entries(self):
        """Test whether _clear_entries() deleting data from lib_id and reader_id entry"""
        self.lib_id_entry.insert(0,'some data')
        self.reader_id_entry.insert(0,'some data')
        
        self.issue_book._clear_entries()
        
        self.assertEqual(self.lib_id_entry.get(),'')
        self.assertEqual(self.reader_id_entry.get(),'')
        self.assertEqual(self.issue_limit_entry.get(), '2000-01-31')

    
    def tearDown(self):
        self.issue_book.master.destroy()
        
class TestSaveIssueMethod(unittest.TestCase):
    
    def setUp(self):
        """Prepare window object, create mocks of db function and messagebox"""
        self.root = Tk()
        self.issue_book = issue_book.IssueBook(self.root)
        self.entries = self.issue_book.entries_list
        issue_book.messagebox.showerror = Mock()
        
    def test_foreign_key_violation_error(self):
        """Test whether method properly respond to FOREIGN_KEY_VIOLATION error"""
        issue_book.db.save_issue = Mock(side_effect=errors.lookup(errorcodes.FOREIGN_KEY_VIOLATION))
        result = self.issue_book._save_issue()
        self.assertEqual(result, 'FOREIGN_KEY_VIOLATION')
    
    def test_invalid_text_representation(self):
        """Test whether method properly respond to INVALID_TEXT_REPRESENTATION error"""
        issue_book.db.save_issue = Mock(side_effect=errors.lookup(errorcodes.INVALID_TEXT_REPRESENTATION))
        result = self.issue_book._save_issue()
        self.assertEqual(result, 'INVALID_TEXT_REPRESENTATION')
        
    def test_invalid_datetime_format_error(self):
        """Test whether method properly respond to INVALID_DATETIME_FORMAT error"""
        issue_book.db.save_issue = Mock(side_effect=errors.lookup(errorcodes.INVALID_DATETIME_FORMAT))
        result = self.issue_book._save_issue()
        self.assertEqual(result, 'INVALID_DATETIME_FORMAT')
        
    def test_check_violation_error(self):
        """Test whether method properly respond to CHECK_VIOLATION error"""
        issue_book.db.save_issue = Mock(side_effect=errors.lookup(errorcodes.CHECK_VIOLATION))
        result = self.issue_book._save_issue()
        self.assertEqual(result, 'CHECK_VIOLATION')
        
    def test_unique_violation_error(self):
        """Test whether method properly respond to UNIQUE_VIOLATION error"""
        issue_book.db.save_issue = Mock(side_effect=errors.lookup(errorcodes.UNIQUE_VIOLATION))
        result = self.issue_book._save_issue()
        self.assertEqual(result, 'UNIQUE_VIOLATION')
    
    def tearDown(self):
        self.root.destroy()
        
#FIXME - get rid of annoying errors while test run


if __name__ == '__main__':
    unittest.main()