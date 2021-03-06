from tkinter import Button,Toplevel,Entry,Radiobutton,Label,Frame,IntVar
from tkinter.ttk import Treeview
#pylint: disable=unused-variable

class BookListWindow(Frame):
    """Main class contains all window code"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        self._title_label()
        self._search_label()
        self._search_entry()
        self._search_radiobuttons()
        self._search_button()
        self._search_tree()
        self._abort_button()
        
    def _title_label(self):
        """Big title label"""
        Label(self, text='SEARCH PUBLICATIONS').grid()
    
    def _search_label(self):
        """Label with information to search entry"""
        Label(self, text='Search:').grid()
    
    def _search_entry(self):
        """Entry for searching phrase"""
        self.search_entry = Entry(self)
        self.search_entry.grid()

    def _search_radiobuttons(self):
        """Radiobuttons for selecting search criteria"""
        self.search_crit = IntVar()
        criterias = ['ID','Title','Author','Kind','Publisher','Year of publish',
                     'Language','Pages','ISBN','Issued?','Reader ID']
        it_criterias = iter(criterias)
        
        for crit_number in range(len(criterias)):
            Radiobutton(self, text=next(it_criterias), variable=self.search_crit, 
                        value=crit_number).grid()
        print(self.search_crit)

    def _search_button(self):
        """Button which run search engine"""
        self.search_button = Button(self, text='Search', command=self._search)
        self.search_button.grid()
    
    def _search(self):
        """All search engine logic"""
        pass
       
    def _search_tree(self):
        pass
    
    def _abort_button(self):
        """Button which closing window"""
        Button(self, text='Cancel', command=self._abort).grid()
    
    def _abort(self):
        self.master.destroy()
    
    
def start():
    """Create and run view_book_list window"""
    root = Toplevel()
    book_list_window = BookListWindow(root)
    root.geometry('1300x400')
    root.title('View book')
    root.mainloop()
    
