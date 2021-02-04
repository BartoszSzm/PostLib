# Book details class
# Create book_details_window
#   Create label - add book details
#   Create 8 entries 
#   Create 8 labels describing each entry
#   Create accept and cancel button below

from tkinter import Tk, Frame, Label, Entry, Button

class BookDetailsWindow(Frame):
    """book_details_window with all widgets"""
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        # Create label 'add book details'
        Label(self, text = "Add Book Details").grid()
        
        # Create 8 label describing each entry field
        entry_labels = ['Author','Title','Kind','Publisher','Date of publish',
                        'Language','Pages','ISBN']
        for label_text in entry_labels:
            Label(self, text = label_text).grid()
        
        # Create 8 entries with book characteristics
        for button in range(8):
            Entry(self).grid()
        
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
    """Create book_details_window"""
    root = Tk()
    book_details_window = BookDetailsWindow(root)
    root.title('Add Book Details')
    root.geometry('400x800')
    root.mainloop()
