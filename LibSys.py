from tkinter import Canvas, Tk, Frame, Label, Button
from tkinter.constants import NSEW

from LMS.buttons import (book_details, delete_book, book_list, create_reader, 
                         issue_book, return_book, readers_list)

from PIL.ImageTk import PhotoImage
from PIL import Image
#pylint: disable=unused-variable

class MainWindow(Frame):
    """main_window and all widgets"""
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets in main_window"""
        self._welcome_label()
        self._info_labels()
        self._create_buttons()
        self._grids()
    
    def _welcome_label(self):
        """Label with welcome text"""
        img = PhotoImage(Image.open('./images/main.jpg'))
        Label(self, text='Welcome to library', image=img).grid(
            column=0, row=0, columnspan=3, sticky=NSEW)    
    
    def _info_labels(self):
        """Category information labels"""
        Label(self, text='BOOKS').grid(column=0, row=1, sticky=NSEW)
        Label(self, text='READERS').grid(column=1, row=1, sticky=NSEW)
        Label(self, text='ISSUES').grid(column=2, row=1, sticky=NSEW)
    
    def _create_buttons(self):
        """Create all buttons in main window"""
        self.book_details_button = Button(self,text = "Add Book Details", 
                              command = book_details.start)
        self.delete_book_button = Button(self,text = "Delete Book", 
                              command = delete_book.start)
        self.book_list_button = Button(self,text = "View Book List", 
                              command = book_list.start)
        self.create_reader_button = Button(self,text = "Create Reader", 
                              command = create_reader.start)
        self.readers_list_button = Button(self,text = "Readers list", 
                              command = readers_list.start)
        self.issue_book_button = Button(self,text = "Issue Book", 
                              command = issue_book.start)
        self.return_book_button = Button(self,text = "Return Book", 
                              command = return_book.start)
        self.exit_button_button = Button(self,text = "Exit", 
                              command = self.master.destroy) 
    
    def _grids(self):
        """Grid all buttons"""
        self.book_details_button.grid(column=0, row=2, sticky=NSEW)
        self.delete_book_button.grid(column=0, row=3, sticky=NSEW)
        self.book_list_button.grid(column=0, row=4, sticky=NSEW)
        
        self.create_reader_button.grid(column=1, row=2, sticky=NSEW)
        self.readers_list_button.grid(column=1, row=3, sticky=NSEW)
        
        self.issue_book_button.grid(column=2, row=2, sticky=NSEW)
        self.return_book_button.grid(column=2, row=3, sticky=NSEW)
        
        self.exit_button_button.grid(column=1, row=5)               
        
# Run mainloop
def start():
    """Create main_window"""
    root = Tk()
    main_window = MainWindow(root)
    root.title('Library Management System')
    root.geometry('418x461')
    root.mainloop()

# Run app
if __name__ == "__main__":
    start()

