#pylint: disable=unused-wildcard-import

from tkinter import (Button, Entry, Frame, Label, Radiobutton,
                     StringVar, Toplevel, messagebox)
from tkinter.constants import *
from tkinter.ttk import Treeview

from psycopg2 import errorcodes
from psycopg2.errors import lookup

from LMS.buttons import db_functions as db

#pylint: disable=unused-variable


class IssuesList(Frame):
    """Main class contains all window code"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.grid(padx=10)
        self.create_widgets()
        self.master.bind('<Return>', lambda event: self._search())
    
    def create_widgets(self):
        self._title_label()
        self._search_label()
        self._search_entry()
        self._search_criteria_label()
        self._search_radiobuttons()
        self._search_button()
        self._search_tree()
        self._abort_button()
        
    def _title_label(self):
        """Big title label"""
        Label(self, text='SEARCH ISSUES', font='Calibri 14 bold').grid(
            column=0, row=0, columnspan=4, sticky=EW, pady=10)
    
    def _search_label(self):
        """Label with information to search entry"""
        Label(self, text='Type phrase to search:', font='Calibri 11').grid(
            column=0, row=1, columnspan=4, sticky=EW)
    
    def _search_entry(self):
        """Entry for searching phrase"""
        self.search_entry = Entry(self)
        self.search_entry.grid(
            column=0, row=2, columnspan=4, sticky=EW, padx=300)
    
    def _search_criteria_label(self):
        Label(self, text='Search criterias:', font='Calibri 11').grid(
            column=0, row=3, columnspan=4, sticky=EW, pady=10)

    def _search_radiobuttons(self):
        """Radiobuttons for selecting search criteria"""
        self.search_crit = StringVar(value='reader_id')
        criterias = ['issue_id', 'lib_id', 'reader_id', 'issue_date', 'issue_limit',
                     'returned_date', 'delay', 'imposed_penalty']
        
        display_criterias = ['Issue ID', 'Library ID', 'Reader ID', 'Issue Date',
                             'Issue limit', 'Returned date', 'Delay', 'Imposed Penalty']
        
        grids = [(0,4),(0,5),(0,6),
                 (1,4),(1,5),(1,6),
                 (2,4),(2,5)]

        
        for (criteria, display_criteria, grid) in zip(criterias, display_criterias, grids):
            Radiobutton(self, 
                        text=display_criteria, 
                        variable=self.search_crit, 
                        value=criteria).grid(column=grid[0],row=grid[1], sticky=W, padx=70)    
    
    def _search_button(self):
        """Button which run search engine"""
        self.search_button = Button(self, text='Search', command=self._search)
        self.search_button.grid(column=0, row=7, columnspan=4, padx=500, pady=10, sticky=EW)
    
    def _search(self): 
        """Clear results window, get value from entry, run display_results"""
        self.results_window.delete(*self.results_window.get_children())
        self.phrase = self.search_entry.get()
        self._display_results()
        
    def _display_results(self): 
        """Display results on tree"""
        # Use get_results_by from db_functions to get results from db
        try:
            for result in db.get_results_by(self.search_crit.get(), self.phrase, table='issue'):
                self.results_window.insert('', END, values=result)
                
            if not self.results_window.get_children():
                messagebox.showinfo('Results',
                        'No results matching given value.', parent=self.master)
        
        except lookup(errorcodes.INVALID_TEXT_REPRESENTATION):
            messagebox.showerror('Error!', 'Incorrect value.', parent=self.master)
    
    def _search_tree(self):
        """Show results on tree"""
        cols = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8']
        cols_text = ['Issue ID', 'Library ID', 'Reader ID', 'Issue date', 'Issue limit',
                     'Returned date', 'Delay', 'Imposed penalty']
        cols_width = [80, 200, 120, 90, 120, 150, 90, 140]
        
        self.results_window = Treeview(self, columns=cols, show='headings',
                                       height=15)
        
        #Treeview headings
        for (col,text,width) in zip(cols, cols_text, cols_width):
            self.results_window.heading(col, text=text)
            self.results_window.column(col, width=width)
        
        self.results_window.grid(column=0, row=8, columnspan=4)
    
    def _abort_button(self):
        """Button which closing window"""
        Button(self, text='Cancel', command=self.master.destroy).grid(
            column=0, row=9, columnspan=4, padx=500, pady=10, sticky=EW)
    
    
def start():
    """Create and run issues list window"""
    root = Toplevel()
    root.resizable(width=False, height=False)
    issues_list_window = IssuesList(root)
    root.title('Issues List')
    root.mainloop()