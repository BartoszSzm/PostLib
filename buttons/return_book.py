"""Window where end user can return book to the library stock"""

from datetime import date, datetime
from tkinter import Entry, Frame, Toplevel, Label, Button, messagebox, simpledialog
from tkinter.ttk import Treeview
import LMS.options as options
from LMS.buttons import db_functions as db
from psycopg2.errors import lookup
from psycopg2 import errorcodes
from sys import exc_info

#pylint: disable=unused-variable

class Entries(Frame):
    """Return book window and all widgets"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.corr_pass = False #Changed when user type correct password to edit penalty
    
    def run(self):
        """Generate Entries and ResultsTree Frame"""
        self.grid()
        self.create_widgets()
        self.widgets_grids()
        self.results_tree = ResultsTree(self.master, self)
    
    def widgets_grids(self):
        """Grid all widgets"""
        self.title_label.grid(column=0, row=0,columnspan=3, pady=10)
        self.reader_id_label.grid(column=0, row=1, sticky='e', pady=10)
        self.penalty_label.grid(column=0, row=2, sticky='e')
        self.reader_id_entry.grid(column=1, row=1, sticky='w')
        self.penalty_entry.grid(column=1, row=2, sticky='w')
        self.edit_button.grid(column=2, row=2, sticky='w')
        self.info_label.grid(column=0, row=3, columnspan=3, pady=10)
        
    def create_widgets(self):
        """Call all widget generating functions"""
        self.title_label = self._title_label()
        self.reader_id_label = self._reader_id_label()
        self.penalty_label = self._penalty_label()
        self.reader_id_entry = self._reader_id_entry()
        self.penalty_entry = self._penalty_entry()
        self.edit_button = self._edit_button()
        self.info_label = self._info_label()
        
    def _title_label(self): 
        return Label(self, text='Return Book', font='Calibri 14 bold')
    
    def _reader_id_label(self): 
        return Label(self,text='Reader ID', font='Calibri 12')   
    
    def _penalty_label(self):
        return Label(self,text='Penalty', font='Calibri 12')
    
    def _reader_id_entry(self): 
        return Entry(self)

    def _get_readerid_entry(self):
        return self.reader_id_entry.get()
    
    def _penalty_entry(self):
        return Entry(self, state='readonly')
    
    def _getset_penalty_entry(self, operation='get', value=''):
        """Get or set value in entry depends on 'operation' value"""
        self.penalty_entry.configure(state='normal')
        if operation == 'get':
            entry_value = self.penalty_entry.get()
            if not self.corr_pass: self.penalty_entry.configure(state='readonly')
            return entry_value
        elif operation == 'set':
            self.penalty_entry.delete(0,'end')
            self.penalty_entry.insert(0, value)
            if not self.corr_pass: self.penalty_entry.configure(state='readonly')
        else:
            raise ValueError('Operation type should be "get" or "set"')  
    
    def _edit_button(self): 
        """Button allows to edit penalty entry when type password"""
        return Button(self, text='Edit', command=self._edit_penalty)
    
    def _edit_penalty(self):
        """Allow to edit penalty entry when password typed"""
        pass_ans = simpledialog.askstring('Password',
                                          'Enter password:', show='*', 
                                          parent=self.master)
        if str(pass_ans) == options.PASSWORD:
            self.penalty_entry.configure(state='normal')
            self.corr_pass = True
            self.edit_button.grid_forget()
        else:
            return messagebox.showerror('Wrong password!','Incorrect password',
                                 parent=self.master)
                  
    def _info_label(self): 
        return Label(self,text='Select publication to be returned:', font='Calibri 12')


class ResultsTree(Frame):
    """Generate results tree and handle all operations associated with it"""
    def __init__(self, master, entries_window):
        super().__init__(master)
        self.master = master
        self.entries_window = entries_window
        self.grid()
        self._create_widgets()
        self._widgets_grids()
        self.master.bind('<Return>', lambda event: self._search())
    
    def _create_widgets(self):
        """Call all widget generating functions"""
        self.results_tree = self._results_tree()
        self.search_button = self._search_button()
        self.accept_button = self._accept_button()
        self.abort_button = self._abort_button()
    
    def _widgets_grids(self):
        """Grid all widgets"""
        self.results_tree.grid(padx=10)
        self.search_button.grid()
        self.accept_button.grid()
        self.abort_button.grid()
    
    def _results_tree(self):
        """Create treeview widget"""
        cols = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8','#9','#10','#11']
        cols_text = ['Title','Author','ISBN','Issue ID','Library ID','Reader ID',
                     'Issue date','Issue limit','Date of return','Delay','Imposed penalty']
        cols_width = [300, 100, 120, 80, 90, 90, 100, 100, 120, 50, 140]
        results_window = Treeview(self, columns=cols, show='headings',
                                       height=15, selectmode='browse')
        results_window.bind('<<TreeviewSelect>>',self._insert_penalty)
        #Treeview headings
        for (col,text,width) in zip(cols, cols_text, cols_width):
            results_window.heading(col, text=text)
            results_window.column(col, width=width)
        return results_window
    
    def _insert_penalty(self,event): 
        """Insert calculated penalty to the penalty entry"""
        self.entries_window._getset_penalty_entry(operation='set',value='') #Clear penalty entry
        penalty = self._calculate_penalty()
        if penalty != None:
            self.entries_window._getset_penalty_entry(operation='set', value=penalty)

    def _calculate_penalty(self):
        """Return penalty value"""
        if self.results_tree.selection():
            selected_issue_limit = self._get_selected_row('issue_limit')
            selected_issue_limit = datetime.strptime(selected_issue_limit[0],'%Y-%m-%d')
            selected_returned_date = self._get_selected_row('returned_date')  
            delay = date.today() - selected_issue_limit.date()
            delay = int(delay.days)
            if delay > 0 and selected_returned_date[0] == 'None':
                penalty = round((options.PENALTY * delay),2)
                return penalty
            else:  
                return 0
            
    def _get_selected_row(self, *args): 
        """Return list with specified data from selected row"""
        selected_row_data = self.results_tree.item(self.results_tree.selection(),
                            option='values')
        cols = ['title','author','isbn','issue_id','library_id','reader_id',
                'issue_date','issue_limit','returned_date','delay','imposed_penalty']
        data = {}
        for key,value in zip(cols,selected_row_data):
            data[key] = value   
        return [data[element] for element in args if data]

    def _search_button(self): 
        return Button(self, text='Search', command=self._search)            

    def _search(self):
        """Clear results tree, display new results"""
        self.results_tree.selection_clear()
        self.results_tree.delete(*self.results_tree.get_children())
        self._display_results()    
    
    def _display_results(self):
        """Insert results on tree"""
        try:
            for result in db.show_issues(self.entries_window._get_readerid_entry()):
                self.results_tree.insert('', 'end', values=result)
            if not self.results_tree.get_children():
                messagebox.showinfo(title='Nothing found!', 
                                    message="There's no issues for given reader ID.", parent=self.master)
        
        except lookup(errorcodes.INVALID_TEXT_REPRESENTATION):
            messagebox.showerror(title='Error!',
                                 message='Incorrect Reader ID value!',
                                 parent=self.master)
            return 'INVALID_TEXT_REPRESENTATION'
        
        except:
            messagebox.showerror(title='Error!',
                                 message=f'An error occurred: {exc_info()[0]}',
                                 parent=self.master)
            return 'OTHER_ERROR'
    
    def _accept_button(self): 
        """Save data to db"""
        return Button(self, text='Accept', command=self._accept)
    
    def _accept(self):
        """Update db record (issue)"""
        if self.results_tree.selection():
            selected_issue_id = self._get_selected_row('issue_id')[0]
            selected_returned_date = self._get_selected_row('returned_date')[0]
            penalty = self.entries_window._getset_penalty_entry(operation='get')
            if selected_returned_date == 'None':
                if messagebox.askyesno('Info',f'Upon return, a penalty of {penalty} '
                                    f'will be charged. Do you approve?', 
                                    parent = self.master):
                    db.return_book(selected_issue_id, date.today(), penalty)
                    messagebox.showinfo('Ok!','Publication successfully returned.',
                                        parent=self.master)
                    return 1
            else:
                messagebox.showerror('Error!','This publication was already returned!', 
                                    parent=self.master)
                return 'PUBLICATION_RETURNED'
        else:
            messagebox.showerror('Error!','Select publication to return.',
                                 parent=self.master)
            return 'NO_SELECTION'
        
    def _abort_button(self): 
        return Button(self, text='Abort', command=self.master.destroy)


def start():
    """Run window"""
    root = Toplevel()
    root.resizable(width=False, height=False)
    entries_buttons = Entries(root)
    entries_buttons.run()
    root.title('Return Book')
    root.mainloop()
