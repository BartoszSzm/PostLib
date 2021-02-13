# Library management system
# Create MainWindow
#   Create widgets
#       Label/text 'Add book details'
#       Button Add book details
#       Button Delete book
#       Button View book list
#       Button Issue book to student
#       Button Return book
#       Button Exit

from tkinter import Tk, Frame, Label, Button
from buttons import book_details, delete_book

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
        self._create_buttons()
        
    def _welcome_label(self):
        """Label with welcome text"""
        Label(self, text='Welcome to library').grid()
        
    def _create_buttons(self):
        """Create all buttons in main window"""
        book_details_button = Button(self,text = "Add Book Details", 
                              command = self._book_details)
        book_details_button.grid()
        
        delete_book_button = Button(self,text = "Delete Book", 
                              command = self._delete_book)
        delete_book_button.grid()
        
        book_list_button = Button(self,text = "View Book List", 
                              command = self._book_list)
        book_list_button.grid()
        
        issue_book_button = Button(self,text = "Issue Book", 
                              command = self._issue_book)
        issue_book_button.grid()
        
        return_book_button = Button(self,text = "Return Book", 
                              command = self._return_book)
        return_book_button.grid()
        
        exit_button_button = Button(self,text = "Exit", 
                              command = self._exit)
        exit_button_button.grid()
    
    def _book_details(self):
        book_details.start()

    def _delete_book(self):
        delete_book.start()

    def _book_list(self):
        pass

    def _issue_book(self):
        pass
    
    def _return_book(self):
        pass
    
    def _exit(self):
        """Close main_window"""
        self.master.destroy()
                   
        
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

