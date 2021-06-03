"""Tests for book_list window"""

from tkinter.constants import END
import unittest
from tkinter import Tk
from unittest.mock import Mock

from psycopg2.errors import lookup
from psycopg2 import errorcodes

from LMS.buttons import book_list


class TestBookList(unittest.TestCase):
    """All tests for BookListWindow class"""
    
    def setUp(self):
        self.root = Tk()
        self.db_get_results_by = book_list.db.get_results_by
        book_list.messagebox = Mock()
        self.window = book_list.BookListWindow(self.root)
        self.tree = self.window.results_window
        self.test_values = ('id','title','author','kind','publisher','year','lang','pages','isbn','false')
    
    def test_search_command(self):
        """Test if search command inserts data into tree"""
        # Add test record, check it
        self.tree.insert('',END, values=self.test_values)
        for item in self.tree.get_children():
            self.assertEqual(self.tree.item(item)['values'], list(self.test_values))
        
        self.window._display_results = Mock()
        self.window.search_entry.insert(0,'test')
        self.window._search()
        
        # Asserts
        self.assertEqual(self.tree.get_children(), tuple(''))
        self.assertEqual(self.window.phrase, 'test')
        self.window._display_results.assert_called_once()
        
    def test_display_results_ok(self):
        """Test if method correctly displaying results"""
        book_list.db.get_results_by = Mock(return_value=(self.test_values,))
        
        self.window.phrase = 'test'
        self.window._display_results()

        for item in self.tree.get_children():
            self.assertEqual(self.tree.item(item)['values'], list(self.test_values))
    
    def test_display_results_wrong_value(self):
        """Test if method raises error when db raises"""
        book_list.db.get_results_by = Mock(side_effect=lookup(errorcodes.INVALID_TEXT_REPRESENTATION))
        self.window.phrase = 'test'
        result = self.window._display_results()
        self.assertEqual(result,'INVALID_TEXT_REPRESENTATION')
        
    def test_display_results_nothing_found(self):
        """Test if method informs when nothing was found"""
        book_list.db.get_results_by = Mock(return_value=())
        self.window.phrase = 'test'
        result = self.window._display_results()
        self.assertEqual(result, 'NOTHING_FOUND') 
    
    def tearDown(self):
        book_list.db.get_results_by = self.db_get_results_by
        self.root.destroy()
        
if __name__ == '__main__':
    unittest.main()