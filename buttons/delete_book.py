# Delete book class
# Create class for delete book
#   Delete Book label
#   Library ID label
#   ID Entry
#   Results textbox
#   Accept/Cancel buttons

from tkinter import Frame, Label, Entry, Button, Toplevel, messagebox
from tkinter.constants import END
from tkinter.ttk import Treeview
from buttons import db_functions as db

class DeleteBookWindow(Frame):
    """delete_book_window class and all widgets"""
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        self._delete_book_label()
        self._library_id_label()
        self._library_id_entry()
        self._search_button()
        self._results_treeview()
        self._accept_abort_buttons()
        
    def _delete_book_label(self):
        Label(self, text = "Delete Book").grid()
    
    def _library_id_label(self):
        Label(self, text = "Library ID").grid()
    
    def _library_id_entry(self):
        self.id_entry = Entry(self)
        self.id_entry.grid()
    
    def _search_button(self):
        self.search_button = Button(self, text='Search', command=self._search)
        self.search_button.grid()
        self.was_searched = False
        
    def _results_treeview(self):
        """Show results in treeview"""
        # Treeview params
        cols = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10']
        cols_text = ['ID','Title','Author','Kind','Publisher',
                          'Year of publish','Language','Pages','ISBN','Issued?']
        cols_width = [50, 200, 120, 90, 120, 150, 100, 70, 150, 90]
        
        self.results_window = Treeview(self, columns=cols, show='headings',
                                       height=2)
        
        #Treeview headings
        for (col,text,width) in zip(cols, cols_text, cols_width):
            self.results_window.heading(col, text=text)
            self.results_window.column(col, width=width)
        
        self.results_window.grid()
        
    def _accept_abort_buttons(self):
        accept = Button(self, text = 'Accept', command = self._accept)
        abort = Button(self, text = 'Cancel', command = self._abort)
        
        accept.grid()
        abort.grid()
    
    def _search(self):
        """Search and view result in treeview"""
        # Clear tree
        self.results_window.delete(*self.results_window.get_children())
        
        # Get value from entry - only numbers allowed
        self.lib_id = self.id_entry.get()
        try:
            self.lib_id = int(self.lib_id)
        except ValueError:
            info = messagebox.showerror('Error','ID must be a number...')
            return
 
        # Show results in tree
        for result in db.get_results_by('lib_id',self.lib_id):
            self.results_window.insert('', END, values=result)
        
        # If no results throw info
        if not self.results_window.get_children():
            info = messagebox.showinfo('Results',
                                       'No results matching given value.')
        
        # Flag determines if search was performed
        self.was_searched = True
        
    def _accept(self):
        """Delete found record from db"""
        
        if not self.was_searched:
            info = messagebox.showwarning('Info','Please search for record '
                                          'first and check it.')
            return
        if self.results_window.get_children():
            warning = messagebox.askyesno('Warning!','Deletion will be permanent.'
                                    '\nAre you shure ?')
            if warning:
                try:
                    db.delete_record_by(self.lib_id)
                    deleted = messagebox.showinfo('Success','Record deleted successfully.')
                except Exception as error:
                    saving_error = messagebox.showerror('Error',error)
        else:
            error = messagebox.showerror('Error','Nothing found under given ID.')
    
    def _abort(self):
        self.master.destroy()
        
# Run mainloop
def start():
    """Create delete_book_window"""
    root = Toplevel()
    delete_book_window = DeleteBookWindow(root)
    root.title('Delete Book')
    root.geometry('1150x255')
    root.mainloop()