
from tkinter import Frame, Label, Entry, Button, Toplevel, messagebox
from tkinter.constants import END
from tkinter.ttk import Treeview
from LMS.buttons import db_functions as db
#pylint: disable=unused-variable

class DeleteBookWindow(Frame):
    """delete_book_window class and all widgets"""
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.grid(padx=5)
        self.create_widgets()
        
    def create_widgets(self):
        self._delete_book_label()
        self._library_id_label()
        self._library_id_entry()
        self._search_button()
        self._results_treeview()
        self._accept_abort_buttons()
        
    def _delete_book_label(self):
        Label(self, text = "Delete Book", font='Calibri 14 bold').grid(pady=1)
    
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
        
        self.results_window.grid(pady=20)
        
    def _accept_abort_buttons(self):
        accept = Button(self, text = 'Accept', command = self._accept)
        abort = Button(self, text = 'Cancel', command = self.master.destroy)
        accept.grid(pady=10)
        abort.grid(pady=10)
    
    def _search(self):
        """Search for record by given ID"""
        # Clear results tree, get value from entry, change to int
        self.results_window.delete(*self.results_window.get_children())
        self.lib_id = self.id_entry.get()
        try:
            self.lib_id = int(self.lib_id)
        except ValueError:
            info = messagebox.showerror('Error','ID must be a number...',
                                        parent=self.master)
            return
        # Display results after all
        self._display_results()
        
    def _display_results(self):
        """Display records on tree"""
        # Show results on tree
        for result in db.get_results_by('lib_id',self.lib_id):
            self.results_window.insert('', END, values=result)
        
        # If found something, set search flag to true, else show info
        if self.results_window.get_children():
            self.was_searched = True
        else:
            info = messagebox.showinfo('Results',
                                       'No results matching given value.', 
                                       parent = self.master)
        
    def _accept(self):
        """Delete found record from db"""
        # Delete if record with given lib_id exist, search was performed and 
        # user accepts it
        
        if self.was_searched:
            if self.results_window.get_children():
                warning = messagebox.askyesno('Warning!',f'Deletion of record' 
                                    f'with ID:{self.lib_id} will be permanent.'
                                    f' Are you shure ?', parent=self.master)
                if warning:
                    try:
                        db.delete_record_by('lib_id',self.lib_id,'publications')
                        deleted = messagebox.showinfo('Success',f'Record with '
                                            f'ID:{self.lib_id} deleted '
                                            f'successfully.', parent=self.master)
                    except Exception as error:
                        saving_error = messagebox.showerror('Error',error, parent=self.master)
            else:
                error = messagebox.showerror('Error',
                                    f'Nothing found under ID:{self.lib_id}.', parent=self.master)
        else:
            info = messagebox.showwarning('Info','Please search for record '
                                            'first and check it.', parent=self.master)
        
# Run mainloop
def start():
    """Create delete_book_window"""
    root = Toplevel()
    delete_book_window = DeleteBookWindow(root)
    root.title('Delete Book')
    root.resizable(width=False, height=False)
    root.mainloop()