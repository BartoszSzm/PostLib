from tkinter import Tk, Frame, Label, Button
from tkinter.constants import SUNKEN

from buttons import (book_details, delete_book, book_list, create_reader, 
                         issue_book, return_book, readers_list, issues_list)

from PIL.ImageTk import PhotoImage
from PIL import Image
#pylint: disable=unused-variable

WIN_HEIGHT = 600
WIN_WIDTH = 850

class MainWindow(Frame):
    """main_window and all widgets"""
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.configure(background='#1c2729')
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets in main_window"""
        self._info_labels()
        self._create_buttons()
        self._grids()
        
    def _info_labels(self):
        """Category information labels"""
        Label(self, text='BOOKS', font='Verdana 16 bold italic', width=12).grid(column=0, row=1, padx=50, pady=30)
        Label(self, text='READERS', font='Verdana 16 bold italic', width=12).grid(column=1, row=1, padx=50, pady=30)
        Label(self, text='ISSUES', font='Verdana 16 bold italic', width=12).grid(column=2, row=1, padx=50, pady=30)
    
    def _create_buttons(self):
        """Create all buttons in main window"""
        self.book_details_button = Button(self,text = "Add Book Details", 
                              command = book_details.start, font='Calibri 12', overrelief=SUNKEN)
        self.delete_book_button = Button(self,text = "Delete Book", 
                              command = delete_book.start, font='Calibri 12', overrelief=SUNKEN)
        self.book_list_button = Button(self,text = "View Book List", 
                              command = book_list.start, font='Calibri 12', overrelief=SUNKEN)
        self.create_reader_button = Button(self,text = "Create Reader", 
                              command = create_reader.start, font='Calibri 12', overrelief=SUNKEN)
        self.readers_list_button = Button(self,text = "Readers list", 
                              command = readers_list.start, font='Calibri 12', overrelief=SUNKEN)
        self.issue_book_button = Button(self,text = "Issue Book", 
                              command = issue_book.start, font='Calibri 12', overrelief=SUNKEN)
        self.issues_list_button = Button(self,text = "Issues List", 
                              command = issues_list.start, font='Calibri 12', overrelief=SUNKEN)
        self.return_book_button = Button(self,text = "Return Book", 
                              command = return_book.start, font='Calibri 12', overrelief=SUNKEN)
        self.exit_button_button = Button(self,text = "Exit", 
                              command = self.master.destroy, font='Calibri 12', overrelief=SUNKEN) 
    
    def _grids(self):
        """Grid all buttons"""
        self.book_details_button.grid(column=0, row=2, padx=50, pady=10)
        self.delete_book_button.grid(column=0, row=3, padx=50, pady=10)
        self.book_list_button.grid(column=0, row=4, padx=50, pady=10)
        
        self.create_reader_button.grid(column=1, row=2, padx=50, pady=10)
        self.readers_list_button.grid(column=1, row=3, padx=50, pady=10)
        
        self.issue_book_button.grid(column=2, row=2, padx=50, pady=10)
        self.issues_list_button.grid(column=2, row=3, padx=50, pady=10)
        self.return_book_button.grid(column=2, row=4, padx=50, pady=10)
        
        self.exit_button_button.grid(column=1, row=5, padx=50, pady=80)        
        
# Run mainloop
def start():
    """Create main_window"""
    root = Tk()
    root.configure(background='#1c2729')
    root.resizable(width=False, height=False)
    
    img = Image.open('./images/main.jpg')
    img = img.resize((WIN_WIDTH, round(WIN_HEIGHT/3)))
    img = PhotoImage(img)
    Label(root, image=img).grid()
    
    main_window = MainWindow(root)
    root.title('Library Management System')
    root.mainloop()
    
# Run app
if __name__ == "__main__":
    start()
    





