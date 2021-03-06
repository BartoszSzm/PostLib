"""File contains all test for BookDetailsWindow class"""

import unittest
from .. import buttons
from tkinter import Tk

class TestBookDetailsWindow(unittest.TestCase):
    
    def setUp(self):
        self.root = Tk()
        self.bd_window = book_details.BookDetailsWindow(self.root)
    
    def test_entries_amount(self):
        """Test if amount of generated entries are correct"""
        entries_count = len(self.bd_window.entries_obj)
        self.assertEqual(entries_count,8)
        
    def test_accept(self):
        """Test if book_data list is generated correctly"""
        for entry in self.bd_window.entries_obj:
            entry.insert(0,'text')
        
        self.book_data = [parameter.get() for parameter in self.bd_window.entries_obj]
        
        for data in self.book_data:
            self.assertEqual(data,'text')
            
        
if __name__ == '__main__':
    unittest.main()