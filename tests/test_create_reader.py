"""All test for create_reader window"""

import unittest
from tkinter import Button, Entry, Label, Tk

import psycopg2
from psycopg2 import errorcodes
from psycopg2.errors import lookup
from LMS.buttons import create_reader
from LMS.buttons.create_reader import CreateReader
from unittest.mock import Mock

class TestCreateReader(unittest.TestCase):
    """Test CreateReader methods"""
    
    def setUp(self):
        self.root = Tk()
        self.create_reader_window = create_reader.CreateReader(self.root)
        self.entries_list = self.create_reader_window.entries_list
        create_reader.messagebox = Mock()
        
    def test_all_labels_amount(self):
        """Test if class creates proper labels amount"""
        labels_list = [label for label in self.create_reader_window.winfo_children() 
                       if isinstance(label, Label)]
        self.assertEqual(len(labels_list), 5)    
    
    def test_create_entries_amount(self):
        """Test created entries amount"""
        self.assertEqual(len(self.entries_list),4)
    
    def test_create_entries_instance(self):
        """Test if entries was created with proper class"""
        for entry in self.entries_list:
            self.assertIsInstance(entry, Entry)
    
    def test_get_entries_data(self):
        """Test if method gets data from entry properly"""
        for entry in self.entries_list:
            entry.insert(0,'some data')
        data = self.create_reader_window._get_entries_data(self.entries_list)
        self.assertListEqual(data,['some data','some data','some data','some data'])

    def test_save_reader_check_violation(self):
        """Test if method correctly raising check_violation error"""
        create_reader.save_reader = Mock(side_effect=lookup(errorcodes.CHECK_VIOLATION))
        result = self.create_reader_window._save_reader()
        self.assertEqual(result,'CHECK_VIOLATION')
    
    def test_save_reader_unique_violation(self):
        """Test if method correctly raising unique violation error"""
        create_reader.save_reader = Mock(side_effect=lookup(errorcodes.UNIQUE_VIOLATION))
        result = self.create_reader_window._save_reader()
        self.assertEqual(result,'UNIQUE_VIOLATION')
    
    def tearDown(self):
        self.root.destroy()

 
class TestSaveReader(unittest.TestCase):
    """Tests for _save_reader method without tearDown"""
    
    def setUp(self):
        """Create window object"""
        self.root = Tk()
        self.create_reader_window = create_reader.CreateReader(self.root)
        self.entries_list = self.create_reader_window.entries_list

    def test_save_reader_success(self):
        """Test if method successfully calls save_reader method"""
        # Insert some data to entries
        for entry in self.entries_list:
            entry.insert(0,'some data')
        # Mock save_reader function
        create_reader.save_reader = Mock()
        # Assert
        self.assertEqual(self.create_reader_window._save_reader(), 'OK')
    
        
if __name__ == '__main__':
    unittest.main()