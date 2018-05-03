'''
Created on Apr 27, 2018

@author: Garret Krawchison

Great Examples at https://likegeeks.com/python-gui-examples-tkinter-tutorial/
Threading with Logging messages example: https://gist.github.com/bitsgalore/901d0abe4b874b483df3ddc4168754aa#file-logginggui-py-L1
'''


#from Tkinter import *
#import Tkinter as tk
import download_by_file_type as dl


import threading
import logging
#import os

try:
    import tkinter as tk # Python 3.x
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText


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

class myGUI(tk.Frame):
    # This class defines the graphical user interface 
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()
        
    def build_gui(self):                    
        # Build GUI
        #self.root.title('TEST')
        #self.root.option_add('*tearOff', 'FALSE')
        self.configure(background="white")
        self.grid(column=0, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')
        
        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state='disabled', bg="#2196F3", fg="#f3f3f3", padx=6, pady=6)
        st.configure(font='TkFixedFont')
        st.configure(width=61)
        st.grid(column=0, row=1, sticky='nsew', columnspan=4)

        # Create textLogger
        text_handler = TextHandler(st)
        
        # Logging configuration
        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='(message)s')        
        
        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)

   
def main(): 
    root = tk.Tk() 
    
    root.title("Download Files in an HTML Page")
    root.geometry('1020x515')
    #root.configure(background="white")
    root.configure(padx=10)
    root.configure(pady=10)
 
    ## Set favicon
    #thisPath = os.path.dirname(os.path.abspath(__file__))
    #imgicon = tk.PhotoImage(file=os.path.join(thisPath,'favicon.gif'))
    #root.tk.call('wm', 'iconphoto', root._w, imgicon)  
    
    ## Set toolbar icon
    #root.iconbitmap(os.path.join(thisPath,'favicon.gif'))
 
    ## Array of threads which can be manipulated
    threads = []
    
    def fnBtnSubmit(url, extension):    
        ## Begin threading dl.index() function
        t1 = threading.Thread(target=dl.index, args=[url, extension,])
        t1.start()
        threads.append(t1)
 
    def fnBtnClose():
        # join all threads
        for t in threads:
            t.join()
        root.destroy()
 
    def fnBtnClear():
        txtUrl.delete(0,'end')
        txtExtension.delete(0,'end')
        frameRight.st.delete(1,'end')
        
        
    """
    Top level menu items
    """
    ###########################
    ## Add top level file menu
    ###########################
    menu = tk.Menu(root)
        
    ## Add items group to file menu
    menuFileItems = tk.Menu(menu, tearoff=0)
    menuFileItems.add_separator()
    menuFileItems.add_command(label='Close', command=root.destroy)
    
    ## Populate menuFile
    menu.add_cascade(label='File', menu=menuFileItems)
    root.config(menu=menu)
    
    
    ###########################
    ## Add top level about menu
    ###########################
    menuAbout = tk.Menu(root)
    
    ## Add items group to about menu
    menuAboutItems = tk.Menu(menuAbout, tearoff=0)
    menuAboutItems.add_command(label='About')
    
    ## Populate menuAbout
    menu.add_cascade(label='About', menu=menuAboutItems)
    
    """
    Layout
    """
    ############################
    ## Make some high level grid column layout
    ############################
    columnWidth = 475
    # Give frameLeft a min height
    root.grid_columnconfigure(0, minsize=columnWidth)
    # Give frameRight a min height
    root.grid_columnconfigure(1, minsize=columnWidth)
    # The top row will have a minsize
    root.grid_rowconfigure(0, minsize=400)
    
    """
    frameLeft
    """
    frameLeft = tk.Frame(root, width=columnWidth, height=400, padx=6, pady=6, background="white")
    frameLeft.grid(row=0, column=0, sticky = "nsew")
    
    ###### Add left frame content ######
    lblUrl = tk.Label(frameLeft, text="Enter URL:", background="white")
    lblUrl.grid(row=0, column=0, sticky='w')
    
    txtUrl = tk.Entry(frameLeft, width = 60, relief='sunken', highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
    txtUrl.grid(row = 0, column = 2, sticky='w')

    lblExtension = tk.Label(frameLeft, text="Extension:", background="white", anchor='nw')
    lblExtension.grid(row=2, column=0, sticky='w')
    
    txtExtension = tk.Entry(frameLeft, width = 20, relief='sunken', highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
    txtExtension.grid(row = 2, column = 2, sticky='w') 
    
    # add space between label and entry
    frameLeft.grid_columnconfigure(1, minsize=5)
    frameLeft.grid_rowconfigure(1, minsize=10)
    
    
    
    """
    frameRight
    """
    frameRight = tk.Frame(root, width=columnWidth, height=400, padx=6, pady=6, background="white")
    frameRight.grid(row=0, column=1, sticky = "nsew")
    
    ###### Add right frame content ######
    ## myGUI function will fill the right frame with a scrolling text area with logging text
    myGUI(frameRight)
            
    
    """
    frameBottom
    """    
    frameBottom = tk.Frame(root, width=1000, height=150, padx=6, pady=6, background="white")
    frameBottom.grid(row=1, columnspan=2, sticky = "nsew")    
    
    ###### Add bottom frame content ######    
    
    ## The Submit button will call the fnBtnSubmit function and send the values from the text fields above
    btnSubmit = tk.Button(frameBottom, text='Submit', command= lambda: fnBtnSubmit(str(txtUrl.get()), str(txtExtension.get())), padx=4, pady=4, width=20, height=2)
    btnSubmit.grid(row=0, column=1)    
    
    ## The Submit button will call the fnBtnSubmit function and send the values from the text fields above
    btnClear = tk.Button(frameBottom, text='Clear', command=fnBtnClear, padx=4, pady=4, width=20, height=2)
    btnClear.grid(row=0, column=3)    
    
    ## Cancel button
    btnCancel = tk.Button(frameBottom, text='Close', padx=4, pady=4, width=20, height=2, command=fnBtnClose)
    btnCancel.grid(row=0, column=5)
    
    # add space before buttons
    frameBottom.grid_columnconfigure(0, minsize=265)
    # add space between buttons
    frameBottom.grid_columnconfigure(2, minsize=6)
    # add space between buttons
    frameBottom.grid_columnconfigure(4, minsize=6)
 
 
 
    """
    mainloop
    """
    ## Set focus to first entry text
    txtUrl.focus()
    
    ## Start tkinter root
    root.mainloop() 


if __name__ == '__main__':
    main()

    