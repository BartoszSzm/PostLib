"""Class representing create_reader window"""
# pylint: disable=unused-variable

from tkinter import Entry, Toplevel, Frame, Button, Label, messagebox
from tkinter.constants import E, EW, W
from LMS.buttons.db_functions import save_reader
from psycopg2.errors import lookup
from psycopg2 import errorcodes

class CreateReader(Frame):
    """create_reader window with all widgets"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.grid()
        self.create_widgets()
        self.master.bind('<Return>', lambda event: self._save_reader())
        
    def create_widgets(self):
        """Create all widgets"""
        self._title_label()
        self._entries_labels()
        self.entries_list = self._entries()
        self._info_label()
        self._accept_button()
        self._abort_button()
        
    def _title_label(self):
        """Create label with window title"""
        Label(self,text="Create reader", font='Calibri 14 bold').grid(
            column=0,row=0,columnspan=2, pady=10)
        
    def _entries_labels(self):
        """Create labels to all entries"""
        Label(self, text='Full name', font='Calibri 12').grid(column=0,row=1, pady=10, padx=20)
        Label(self, text='Phone number', font='Calibri 12').grid(column=0,row=2, pady=10, padx=20)
        Label(self, text='Email', font='Calibri 12').grid(column=0,row=3, pady=10, padx=20)
        Label(self, text='ID card', font='Calibri 12').grid(column=0,row=4, pady=10, padx=20)
    
    def _entries(self):
        """Create entry for each input data"""
        entries_obj = []
        for entry_number in range(4):
            if entry_number in (0,3):
                entry = Entry(self, highlightbackground='red',highlightthickness=2)
            else:
                entry = Entry(self)
            entry.grid(column=1,row=(entry_number + 1), padx=20)
            entries_obj.append(entry)
        return entries_obj
    
    def _info_label(self):
        Label(self, text='Highlighted fields cannot be empty.', font='Calibri 11').grid(
            column=0, columnspan=2, row=5, pady=10, padx=60, sticky=E)
    
    def _accept_button(self):
        """Button accepting input data, run save to db"""
        Button(self,text='Accept',command=self._save_reader).grid(column=0,row=6, pady=15, sticky=E)
    
    def _abort_button(self):
        """Button closes window"""
        Button(self,text='Abort',command=self.master.destroy).grid(column=1,row=6, sticky=W, pady=15, padx=40)
    
    def _get_entries_data(self, entries):
        """Return list of given data in entries"""
        entries_data_list = []
        for entry in entries:
            data = entry.get()
            entries_data_list.append(data)
        return entries_data_list
        
    def _save_reader(self):
        """Save given data to db"""
        try:
            save_reader(self._get_entries_data(self.entries_list))
        
        except lookup(errorcodes.CHECK_VIOLATION):
            messagebox.showerror('Error!',
                            'Fields "Full name" and "ID card" cannot be empty!',
                            parent=self.master)
            return 'CHECK_VIOLATION'
        
        except lookup(errorcodes.UNIQUE_VIOLATION):
            messagebox.showerror('Error!',
                                 'Reader with given full name and ID card already exists.',
                                 parent=self.master)
            return 'UNIQUE_VIOLATION'
        else:
            messagebox.showinfo('OK!','Reader successfully added.', 
                                parent=self.master)
            self.master.destroy()
            return 'OK'

# Run window
def start():
    """Create and run create_reader window"""
    root = Toplevel()
    create_reader_window = CreateReader(root)
    root.title('Create reader')
    root.resizable(width=False, height=False)
    root.mainloop()
    