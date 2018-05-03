'''
Created on Apr 27, 2018

@author: Garret Krawchison

Great Examples at https://likegeeks.com/python-gui-examples-tkinter-tutorial/
Threading with Logging messages example: https://gist.github.com/bitsgalore/901d0abe4b874b483df3ddc4168754aa#file-logginggui-py-L1
'''

try:
    import tkinter as tk # Python 3.x
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText

import threading
import download_by_file_type as dl
import logging


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class GetFilesFromSite(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Download Files in an HTML Page")
        self.geometry('1020x515')
        self.config(padx=10)
        self.config(pady=10)
        
        # Add top level menu
        self.add_top_level_menu()

        # Threads will hold active threads
        self.threads = []

        # Logging configuration
        logging.basicConfig(filename='run.log',
            level=logging.INFO,
            format='(message)s')
        logger = logging.getLogger()
    
               
        """
        Layout
        """
        ############################
        ## Make some high level grid column layout
        ############################
        columnWidth = 475
        # Give frameLeft a min height
        self.grid_columnconfigure(0, minsize=columnWidth)
        # Give frameRight a min height
        self.grid_columnconfigure(1, minsize=columnWidth)
        # The top row will have a minsize
        self.grid_rowconfigure(0, minsize=400)      



        """
        frameLeft
        """
        self.frameLeft = tk.Frame(self, width=columnWidth, height=400, padx=6, pady=6, background="white")
        self.frameLeft.grid(row=0, column=0, sticky = "nsew")
    
        ###### Add left frame content ######
        self.lblUrl = tk.Label(self.frameLeft, text="Enter URL:", background="white")
        self.lblUrl.grid(row=0, column=0, sticky='w')
    
        self.txtUrl = tk.Entry(self.frameLeft, width = 60, relief='sunken', highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
        self.txtUrl.grid(row = 0, column = 2, sticky='w')
    
        self.lblExtension = tk.Label(self.frameLeft, text="Extension:", background="white", anchor='nw')
        self.lblExtension.grid(row=2, column=0, sticky='w')
    
        self.txtExtension = tk.Entry(self.frameLeft, width = 20, relief='sunken', highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
        self.txtExtension.grid(row = 2, column = 2, sticky='w')
    
        # add space between label and entry
        self.frameLeft.grid_columnconfigure(1, minsize=5)
        self.frameLeft.grid_rowconfigure(1, minsize=10)    
    
    
        """
        frameRight
        """
        self.frameRight = tk.Frame(self, width=columnWidth, height=400, padx=6, pady=6, background="white")
        self.frameRight.grid(row=0, column=1, sticky = "nsew")
 
        ###### Add right frame content ######
               
        # Add text widget to display logging info
        self.st = ScrolledText.ScrolledText(self.frameRight, state='disabled', bg="#2196F3", fg="#f3f3f3", padx=6, pady=6)
        self.st.configure(font='TkFixedFont')
        self.st.configure(width=61)
        self.st.grid(column=1, row=0, sticky='nsew', columnspan=4)

        # Create textLogger
        self.text_handler = TextHandler(self.st)
        
        # Add the handler to logger
        logger.addHandler(self.text_handler)  
    
        """
        frameBottom
        """
        self.frameBottom = tk.Frame(self, width=1000, height=150, padx=6, pady=6, background="white")
        self.frameBottom.grid(row=1, columnspan=2, sticky = "nsew")
    
        ###### Add bottom frame content ######
    
        ## The Submit button will call the fnBtnSubmit function and send the values from the text fields above
        self.btnSubmit = tk.Button(self.frameBottom, text='Submit', command= lambda: self.fnBtnSubmit(str(self.txtUrl.get()), str(self.txtExtension.get())), padx=4, pady=4, width=20, height=2)
        self.btnSubmit.grid(row=0, column=1)
    
        ## The Clear button will clear all input values
        self.btnClear = tk.Button(self.frameBottom, text='Clear', command=self.fnBtnClear, padx=4, pady=4, width=20, height=2)
        self.btnClear.grid(row=0, column=3)
    
        ## Cancel button
        self.btnCancel = tk.Button(self.frameBottom, text='Close', padx=4, pady=4, width=20, height=2, command=self.fnBtnClose)
        self.btnCancel.grid(row=0, column=5)
    
        # add space before buttons
        self.frameBottom.grid_columnconfigure(0, minsize=265)
        # add space between buttons
        self.frameBottom.grid_columnconfigure(2, minsize=6)
        # add space between buttons
        self.frameBottom.grid_columnconfigure(4, minsize=6)
    
    

    def fnBtnSubmit(self, url, extension):
        ## Begin threading dl.index() function
        t1 = threading.Thread(target=dl.index, args=[url, extension,])
        t1.start()
        self.threads.append(t1)
        self.txtUrl.focus()

    def fnBtnClose(self):
        # join all threads
        for t in self.threads:
            t.exit()
        self.destroy()

    def fnBtnClear(self):
        self.txtUrl.delete(0,'end')
        self.txtExtension.delete(0,'end')
        #self.logger("CLEAR (CE)")
        self.st.delete(0,'end')
        self.txtUrl.focus()
    
     
    def add_top_level_menu(self):
        """
        Top level menu items
        """
        ###########################
        ## Add top level file menu
        ###########################
        self.menu = tk.Menu(self)
        self.menuFileItems = tk.Menu(self.menu, tearoff=0)
        self.menuFileItems.add_separator()
        self.menuFileItems.add_command(label='Close', command=self.destroy)
        
        ## Populate menuFile
        self.menu.add_cascade(label='File', menu=self.menuFileItems)
        self.config(menu=self.menu)  
        
        ###########################
        ## Add top level about menu
        ###########################
        self.menuAbout = tk.Menu(self)
    
        ## Add items group to about menu
        self.menuAboutItems = tk.Menu(self.menuAbout, tearoff=0)
        self.menuAboutItems.add_command(label='About')

        ## Populate menuAbout
        self.menu.add_cascade(label='About', menu=self.menuAboutItems)

app = GetFilesFromSite()
app.mainloop()



if __name__ == '__main__':
    pass