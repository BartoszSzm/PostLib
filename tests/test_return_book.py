from datetime import date
from tkinter.ttk import Treeview
import unittest
from unittest.mock import MagicMock, Mock

from psycopg2.errors import lookup
from LMS.buttons import return_book
from tkinter import Tk, messagebox
from freezegun import freeze_time

class TestEntries(unittest.TestCase):
    """All tests for Entries class"""
    def setUp(self):
        self.root = Tk()
        self.window = return_book.Entries(self.root)
        self.window.run()
    
    def test_getset_penalty_entry_get_correct_pass(self):
        """Test if method gets values from penalty entry - password correct"""
        self.window.corr_pass = True
        self.window.penalty_entry.configure(state='normal')
        self.window.penalty_entry.insert(0,'text')
        self.window.penalty_entry.configure(state='readonly')
        result = self.window._getset_penalty_entry()
        self.assertEqual(result, 'text')
        self.assertEqual(self.window.penalty_entry['state'], 'normal')
    
    def test_getset_penalty_entry_get_incorrect_pass(self):
        """Test if method gets values from penalty entry - password incorrect"""
        self.window.corr_pass = False
        self.window.penalty_entry.configure(state='normal')
        self.window.penalty_entry.insert(0,'text')
        self.window.penalty_entry.configure(state='readonly')
        result = self.window._getset_penalty_entry()
        self.assertEqual(result, 'text')
        self.assertEqual(self.window.penalty_entry['state'], 'readonly')
        
    def test_getset_penalty_entry_set_correct_pass(self):
        """Test if method insert value into the penalty entry - password correct"""
        self.window.corr_pass = True
        self.window._getset_penalty_entry(operation='set',value='text')
        self.window.penalty_entry.configure(state='normal')
        result = self.window.penalty_entry.get()
        self.assertEqual(result,'text')
        self.assertEqual(self.window.penalty_entry['state'], 'normal')

    def test_getset_penalty_entry_set_incorrect_pass(self):
        """Test if method insert value into the penalty entry - password incorrect"""
        self.window.corr_pass = True
        self.window._getset_penalty_entry(operation='set',value='text')
        self.window.penalty_entry.configure(state='normal')
        result = self.window.penalty_entry.get()
        self.assertEqual(result,'text')
        self.assertEqual(self.window.penalty_entry['state'], 'normal') 

    def test_getset_penalty_entry_wrong_operation(self):
        """Test if method raises error when incorrect operation given"""
        with self.assertRaises(ValueError):
            self.window._getset_penalty_entry(operation='give')

    def test_edit_penalty_correct_password(self):
        """Test if method unlocks penalty entry, sets corr_pass value and hide edit button"""
        return_book.simpledialog.askstring = Mock(return_value='test')
        return_book.options.PASSWORD = 'test'
        self.window._edit_penalty()
        self.assertEqual(self.window.penalty_entry['state'], 'normal')
        self.assertEqual(self.window.corr_pass, True)
        self.assertNotIn(self.window.edit_button, self.window.grid_slaves())     
           
    def test_edit_penalty_incorrect_password(self):
        """Test if method changing state of penalty entry - incorrect password"""   
        return_book.options.PASSWORD = 'test'
        return_book.simpledialog.askstring = Mock(return_value='abc') #wrong pass        
        return_book.messagebox.showerror = Mock(return_value='Error')
        # Assert
        result = self.window._edit_penalty()
        self.assertEqual(result, 'Error')
        self.assertEqual(self.window.penalty_entry['state'], 'readonly')
        self.assertEqual(self.window.corr_pass, False)
        self.assertIn(self.window.edit_button, self.window.grid_slaves())
           
    def tearDown(self):
        self.root.destroy()


class TestResultsTree(unittest.TestCase):
    """All tests for ResultsTree class"""
    def setUp(self):
        self.root = Tk()
        self.window = return_book.Entries(self.root)
        self.window.run()
        self.window = self.window.results_tree

    def test_results_tree_widget(self):
        """Test if treeview was created correctly"""
        self.assertEqual(len(self.window.results_tree['columns']), 11)
        self.assertIsInstance(self.window.results_tree, Treeview)
     
    def test_insert_penalty(self):
        """Test if method inserts penalty correctly with correct value"""
        self.window._calculate_penalty = Mock(return_value='10')
        self.window._insert_penalty('<<TreeviewSelect>>')
        penalty_entry = self.window.entries_window.penalty_entry
        penalty_entry.configure(state='normal') #penalty_entry disabled at this moment
        self.assertEqual(penalty_entry.get(), '10')
    
    @freeze_time('2021-04-01')
    def test_calculate_penalty(self):
        """Test if method calculates penalty correctly"""
        return_book.options.PENALTY = 1
        tree = self.window.results_tree
        test_values = ['','','','','','','2021-03-01','2021-03-15',None,'','']
        tree.insert('', 'end', values=test_values)
        tree.selection_add(tree.get_children())
        penalty = self.window._calculate_penalty()
        self.assertEqual(penalty, 17)
        
    @freeze_time('2021-04-01')
    def test_calculate_penalty_already_returned(self):
        """Test if method returns 0 when book already returned"""
        return_book.options.PENALTY = 1
        tree = self.window.results_tree
        test_values = ['','','','','','','2021-03-01','2021-03-15','2021-03-17','','']
        tree.insert('', 'end', values=test_values)
        tree.selection_add(tree.get_children())
        penalty = self.window._calculate_penalty()
        self.assertEqual(penalty, 0)
        
    @freeze_time('2021-03-10')
    def test_calculate_penalty_returned_on_time(self):
        """Test if method returns 0 when book returned on time"""
        return_book.options.PENALTY = 1
        tree = self.window.results_tree
        test_values = ['','','','','','','2021-03-01','2021-03-15',None,'','']
        tree.insert('', 'end', values=test_values)
        tree.selection_add(tree.get_children())
        penalty = self.window._calculate_penalty()
        self.assertEqual(penalty, 0)
        
    def test_get_selected_row(self):
        """Test if method gets data from selected row"""
        tree = self.window.results_tree
        test_values = ['title','author','isbn','issue_id','library_id','reader_id',
                       '2021-03-01','2021-03-15',None,'delay','imposed_penalty']
        tree.insert('', 'end', values=test_values)
        tree.selection_add(tree.get_children())
        
        get_data = self.window._get_selected_row
        self.assertEqual(get_data('title'), ['title'])
        self.assertEqual(get_data('returned_date'), ['None'])
        self.assertEqual(get_data('returned_date', 'isbn'), ['None','isbn'])
        self.assertEqual(get_data('returned_date', 'isbn', 'delay'), ['None','isbn','delay'])
        
    def test_display_results(self):
        """Test if method inserts results from db into treeview correctly"""
        tree = self.window.results_tree
        test_values = [('title','author','isbn','issue_id','library_id','reader_id',
                       '2021-03-01','2021-03-15',None,'delay','imposed_penalty')]
        return_book.db.show_issues = Mock(return_value=test_values)
        
        self.window._display_results()
        
        tree.selection_add(tree.get_children())
        result_data = tree.item(tree.selection(), option='values')
        self.assertTupleEqual(result_data,
                              ('title','author','isbn','issue_id','library_id',
                               'reader_id','2021-03-01','2021-03-15','None','delay','imposed_penalty'))
    
    def test_display_results_invalid_text_representation(self):
        """Test if method correctly raises error when Reader ID is incorrect"""
        return_book.messagebox.showerror = Mock()
        self.window.entries_window.reader_id_entry.insert(0,'abc')
        result = self.window._display_results()
        self.assertEqual(result, 'INVALID_TEXT_REPRESENTATION')
        
    @freeze_time('2021-04-01')
    def test_accept(self):
        """Test if accept method calls mocked return_book() db_func with correct args"""
        #Prepare test record on treeview
        tree = self.window.results_tree
        test_values = ['title','author','isbn','issue_id','library_id','reader_id',
                       '2021-03-01','2021-03-15',None,None,None]
        tree.insert('', 'end', values=test_values)
        return_book.options.PENALTY = 1
        tree.selection_add(tree.get_children())
        self.window._insert_penalty('<<TreeviewSelect>>')
        #Prepare mocks
        return_book.db.return_book = Mock()
        return_book.messagebox.askyesno = Mock(return_value=1) #anwser 'yes' 
        return_book.messagebox.showinfo = Mock()
        result = self.window._accept()
        #Asserts 
        self.assertEqual(result, 1) #method returns 1 when threre's no exceptions during executing
        return_book.db.return_book.assert_called_once_with('issue_id', date(2021,4,1),'17')
        
    def test_accept_no_selection(self):
        """Test if method raises error when no record selected"""
        tree = self.window.results_tree
        test_values = ['title','author','isbn','issue_id','library_id','reader_id',
                       '2021-03-01','2021-03-15',None,None,None]
        tree.insert('', 'end', values=test_values)
        
        return_book.messagebox.showerror = Mock()
        
        result = self.window._accept()
        self.assertEqual(result, 'NO_SELECTION')
        
    def test_accept_publication_returned(self):
        """Test if method raises error when publication was already returned"""
        tree = self.window.results_tree
        test_values = ['title','author','isbn','issue_id','library_id','reader_id',
                       '2021-03-01','2021-03-15','2021-03-10',None,None]
        tree.insert('', 'end', values=test_values)
        tree.selection_add(tree.get_children())
        self.window._insert_penalty('<<TreeviewSelect>>')

        return_book.messagebox.showerror = Mock()
        
        result = self.window._accept()
        self.assertEqual(result, 'PUBLICATION_RETURNED')
          
    def tearDown(self):
        self.root.destroy()
        


if __name__ == '__main__':
    unittest.main()
