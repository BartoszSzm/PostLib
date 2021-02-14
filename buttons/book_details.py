# Book details class
# Create book_details_window
#   Create label - add book details
#   Create 8 entries 
#   Create 8 labels describing each entry
#   Create accept and cancel button below

from tkinter import Toplevel, messagebox, Frame, Label, Entry, Button
from tkinter.constants import EW
import psycopg2
from buttons import db_functions as db


class BookDetailsWindow(Frame):
    """book_details_window with all widgets"""
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets in window"""
        self._book_details_label()
        self._info_label()
        self._entries_labels()
        self._entries()
        self._accept_abort_buttons()
        
    def _book_details_label(self):
        """Create label 'add book details'"""
        Label(self, text = "Add Book Details").grid(column=1, row=0, 
                                                    columnspan=2, sticky=EW)
        
    def _info_label(self):
        """Label containg info about data typing"""
        Label(self,text='Highlighted fields cannot be empty.\n'
                        'Field "Year of publish" should contain only number.'
                        ).grid(column=1, row=13, columnspan=2)
    
    def _entries_labels(self):
        """Create label describing each entry field"""   
        entry_labels = ['Title','Author','Kind','Publisher','Year of publish',
                        'Language','Pages','ISBN']
        row_number = 2
        for label_text in entry_labels:
            Label(self, text = label_text).grid(column=1,row=row_number)
            row_number += 1
    
    def _entries(self): 
        """Create entry for each of book characteristics"""    
        row_number = 2
        self.entries_obj = []
        for entry in range(8):
            
            if entry in (0,1,3,4):
                entry_obj = Entry(self,highlightbackground='blue')
            else:
                entry_obj = Entry(self)
            
            entry_obj.grid(column=2, row=row_number)
            self.entries_obj.append(entry_obj)
            row_number += 1
            
    def _accept_abort_buttons(self):
        """Create accept and cancel button"""
        accept = Button(self, text = 'Accept', command = self._accept)
        abort = Button(self, text = 'Cancel', command = self._abort)
        accept.grid(column=1, row=11)
        abort.grid(column=2, row=11)

    def _accept(self):
        """Get entry values, save to db"""
        self.book_data = [parameter.get() for parameter in self.entries_obj]
        if self._answer_ok("Save publication","Save this publication ?"):
            self._save_to_db()
            
    def _save_to_db(self):
        """Save to database with exceptions handling"""
        try:
            db.save_book(self.book_data)
            success_info = messagebox.showinfo(title='Success',
                                    message='Publication successfully added.')
            self.master.destroy()
            
        except psycopg2.IntegrityError:
            error = messagebox.showerror(title='Empty field',
                                         message='Please enter correct data in'
                                                ' remaining fields.')
        except psycopg2.DataError:
            error = messagebox.showerror(title='Invalid data',
                                         message='Field "Year of publish"' 
                                                 ' cannot be empty or contain' 
                                                 ' text.')
           
    def _abort(self):
        if self._answer_ok("Cancel","Are you shure ?"):
            self.master.destroy()
    
    def _answer_ok(self,title, message):
        """Return True if anwser to 'message' question is 'ok'"""
        answer = messagebox.askyesno(title=title,
                                message=message)
        if answer:
            return True
                 
# Run mainloop
def start():
    """Create book_details_window"""
    root = Toplevel()
    book_details_window = BookDetailsWindow(root)
    root.title('Add Book Details')
    root.geometry('469x404')
    root.mainloop()
