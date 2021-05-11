#pylint: disable=unused-wildcard-import

from tkinter import (Button, Entry, Frame, Label, Radiobutton,
                     StringVar, Toplevel, messagebox)
from tkinter.constants import *
from tkinter.ttk import Treeview

import psycopg2

from LMS.buttons import db_functions as db

#pylint: disable=unused-variable


class ReadersList(Frame):
    """Main class contains all window code"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.grid(padx=10)
        self.create_widgets()
    
    def create_widgets(self):
        self._title_label()
        self._search_label()
        self._search_entry()
        self._search_radiobuttons()
        self._search_button()
        self._search_tree()
        self._abort_button()
        
    def _title_label(self):
        """Big title label"""
        Label(self, text='SEARCH READERS').grid(
            column=0, row=0, columnspan=4, sticky=EW)
    
    def _search_label(self):
        """Label with information to search entry"""
        Label(self, text='Search:').grid(
            column=0, row=1, columnspan=4, sticky=EW)
    
    def _search_entry(self):
        """Entry for searching phrase"""
        self.search_entry = Entry(self)
        self.search_entry.grid(
            column=0, row=2, columnspan=4, sticky=EW, padx=300)

    def _search_radiobuttons(self):
        """Radiobuttons for selecting search criteria"""
        self.search_crit = StringVar(value='reader_id')
        criterias = ['reader_id','full_name','phone_number','email','id_card',
                     'total_penalty']
        
        display_criterias = ['Reader ID','Full Name','Phone Number','Email','ID Card',
                             'Total Penalty']
        
        grids = [(0,3),(0,4),(0,5),
                 (1,3),(1,4),(1,5)]

        
        for (criteria, display_criteria, grid) in zip(criterias, display_criterias, grids):
            Radiobutton(self, 
                        text=display_criteria, 
                        variable=self.search_crit, 
                        value=criteria).grid(column=grid[0],row=grid[1], sticky=W)    
    
    def _search_button(self):
        """Button which run search engine"""
        self.search_button = Button(self, text='Search', command=self._search)
        self.search_button.grid(column=0, row=6, columnspan=4, padx=500, sticky=EW)
    
    def _search(self): 
        """Clear results window, get value from entry, run display_results"""
        self.results_window.delete(*self.results_window.get_children())
        self.phrase = self.search_entry.get()
        self._display_results()
        
    def _display_results(self): 
        """Display results on tree"""
        # Use get_results_by from db_functions to get results from db
        for result in db.get_results_by(self.search_crit.get(), self.phrase, table='person'):
            self.results_window.insert('', END, values=result)
            
        if not self.results_window.get_children():
            messagebox.showinfo('Results',
                    'No results matching given value.', parent=self.master)  
    
    def _search_tree(self):
        """Show results on tree"""
        cols = ['#1', '#2', '#3', '#4', '#5', '#6']
        cols_text = ['Reader ID','Full Name','Phone Number','Email','ID Card',
                     'Total Penalty']
        cols_width = [50, 200, 120, 90, 120, 150]
        
        self.results_window = Treeview(self, columns=cols, show='headings',
                                       height=25)
        
        #Treeview headings
        for (col,text,width) in zip(cols, cols_text, cols_width):
            self.results_window.heading(col, text=text)
            self.results_window.column(col, width=width)
        
        self.results_window.grid(column=0, row=7, columnspan=4)
    
    def _abort_button(self):
        """Button which closing window"""
        Button(self, text='Cancel', command=self.master.destroy).grid(
            column=0, row=8, columnspan=4, padx=500, sticky=EW)
    
    
def start():
    """Create and run readers list window"""
    root = Toplevel()
    reader_list_window = ReadersList(root)
    root.geometry('1162x747')
    root.title('Readers list')
    root.mainloop()