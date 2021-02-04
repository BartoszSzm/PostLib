# Delete book class
# Create class for delete book
#   Delete Book label
#   Library ID label
#   ID Entry
#   Results textbox
#   Accept/Cancel buttons

from tkinter import Tk, Frame, Label, Entry, Button, Text

class DeleteBookWindow(Frame):
    """delete_book_window class and all widgets"""
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        # Delete book label
        Label(self, text = "Delete Book").grid()
        
        # Library ID label
        Label(self, text = "Library ID").grid()
        
        # Entry for library ID
        self.id_entry = Entry(self)
        self.id_entry.grid()
        
        # Results window
        self.results_window = Text(self, height = 7, width = 80)
        self.results_window.grid()
        
        # Accept/Abort buttons
        accept = Button(self, text = 'Accept', command = self.accept)
        abort = Button(self, text = 'Cancel', command = self.abort)
        
        accept.grid()
        abort.grid()
        
    # Accept/Abort buttons functions
    def accept(self):
        pass
    
    def abort(self):
        self.master.destroy()
        
# Run mainloop
def start():
    """Create delete_book_window"""
    root = Tk()
    delete_book_window = DeleteBookWindow(root)
    root.title('Delete Book')
    root.geometry('723x253')
    root.mainloop()