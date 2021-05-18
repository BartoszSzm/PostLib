"""Window for issue specyfic publication to specific person"""

from tkinter import Entry, Toplevel, Frame, Label, Button, messagebox
from tkcalendar import DateEntry
from LMS import options
from LMS.buttons import db_functions as db
from datetime import date, timedelta
from psycopg2 import errors, errorcodes
from sys import exc_info                                

# pylint: disable=unused-variable

class IssueBook(Frame):
    """IssueBook window and all widgets"""
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.grab_set()
        self.initialize_options()
        self.create_widgets()
    
    def initialize_options(self):
        self.penalty = options.PENALTY
        self.issue_limit = options.ISSUE_LIMIT
        self.return_limit = self._return_limit()

    def _return_limit(self):
        """Return date when publication should be returned"""
        return (date.today() + timedelta(days=self.issue_limit))
   
    def create_widgets(self):
        """Create all widgets on window"""
        self._title_label()
        self._entry_labels()
        self._info_labels()
        self.entries_list = self._entries(self.return_limit)
        self._accept_button()
        self._abort_button()
        
    def _title_label(self):
        """Label with window name"""
        Label(self, text='Issue Book', font='Calibri 14 bold').grid(column=0,row=0,
            columnspan=2, pady=10)
        
    def _entry_labels(self):
        """Labels defining each entry"""
        Label(self, text='Library ID', font='Calibri 12').grid(column=0, row=1, padx=30)
        Label(self, text='Reader ID', font='Calibri 12').grid(column=0, row=2, pady=10, padx=30)
        Label(self, text='Issue limit', font='Calibri 12').grid(column=0, row=3, padx=30)
        
    def _info_labels(self):
        """Labels with info about current issue options"""
        Label(self, 
              text=f'Current penalty : {self.penalty}$/day', 
              font='Calibri 11 italic').grid(column=0, row=5, columnspan=2, padx=30)
        
        Label(self, 
              text=f'Current issue limit: {self.issue_limit} days',
              font='Calibri 11 italic').grid(column=0, columnspan=2, row=6, padx=30, pady=15)
        
    def _entries(self, return_limit):
        """Create entries for each input data"""
        lib_id = Entry(self)
        reader_id = Entry(self)
        issue_limit = DateEntry(self)
        issue_limit.set_date(self.return_limit)
        issue_limit.configure(width=18, date_pattern='yyyy-mm-dd')
        
        lib_id.grid(column=1, row=1, padx=20)
        reader_id.grid(column=1, row=2, padx=20)
        issue_limit.grid(column=1, row=3, padx=20)
        # Must be in this order!
        return [lib_id, reader_id, issue_limit]
    
    def _accept_button(self):
        """Button which accepts new issue creation"""
        Button(self, text='Accept', command=self._save_issue).grid(column=0, row=4, pady=10)
    
    def _get_entries_data(self):
        """Return all data from entries"""
        data_list = [entry.get() for entry in self.entries_list]
        return data_list
    
    def _save_issue(self):
        """Save input data, creates new issue"""
        data = self._get_entries_data()
        try:
            db.save_issue(data)
        except errors.lookup(errorcodes.FOREIGN_KEY_VIOLATION):
            messagebox.showerror('Error!', 'The given Library ID or Reader ID does not exist!', parent=self.master)
            return 'FOREIGN_KEY_VIOLATION'
        except errors.lookup(errorcodes.INVALID_TEXT_REPRESENTATION):
            messagebox.showerror('Error!', 'Library ID or Reader ID cannot be empty!', parent=self.master)
            return "INVALID_TEXT_REPRESENTATION"
        except (errors.lookup(errorcodes.INVALID_DATETIME_FORMAT),
                errors.lookup(errorcodes.DATETIME_FIELD_OVERFLOW)):
            messagebox.showerror('Error!', 'Incorrect date format!', parent=self.master)
            return 'INVALID_DATETIME_FORMAT'
        except errors.lookup(errorcodes.CHECK_VIOLATION):
            messagebox.showerror('Error!', 'Issue limit date must be later than today!', parent=self.master)
            return 'CHECK_VIOLATION'
        except errors.lookup(errorcodes.UNIQUE_VIOLATION):
            messagebox.showerror('Error!', 'Publication with this Library ID has already been issued!', parent=self.master)
            return 'UNIQUE_VIOLATION'
        except:
            messagebox.showerror('Error!', f'Unexpected error: {exc_info()[0]}', parent=self.master)
        else:
            self._clear_entries()
            messagebox.showinfo('Ok!','Publication successfully issued.', parent=self.master)
            return 'OK'
        
    def _clear_entries(self):
        """Clear entered text from lib_id and reader_id entry"""
        self.entries_list[0].delete(0,'end')
        self.entries_list[1].delete(0,'end')
        
    def _abort_button(self):
        """Close window button"""
        Button(self, text='Abort', command=self.master.destroy).grid(column=1, row=4, pady=10)
    
def start():
    """Create and run main window"""
    root = Toplevel()
    root.resizable(width=False, height=False)
    issue_book_window = IssueBook(root)
    root.title('Issue Book')
    root.mainloop()
    
# TODO - make infomessages when any of entries left blank (all NOT NULL)
   
    # lib_id must exist in publications table - ForeignKeyViolation v
    
    # lib_id must be not null - InvalidTextRepresentation v
    
    # reader_id must exist in person table - ForeignKeyViolation v
    
    # reader_id must be not null - InvalidTextRepresentation v
    
    # issue_limit must be in correct date format - InvalidDatetimeFormat
        # format 2021-04-1 or 2021-4-1 is correct
    
    # issue_limit must be not null - InvalidDatetimeFormat v
    
    # issue_limit must be higher than issue_date (today) - CheckViolation v
    
    # error when trying to issue alredy issued publication - UniqueViolation v
    
    # List of all errors : 
    # ForeignKeyViolation - InterityError
    # InvalidTextRepresentation - DataError
    # InvalidDateTimeFormat - DataError
    # CheckViolation - IntegrityError
    # UniqueViolation - IntegrityError
     
    #lib_id not present - 1, present - 3
    #reader_id not present - 105, present - 86
