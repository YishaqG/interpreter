import tkinter as tk
import logging
from views import TextBox
from views.submenu import File as subFile
from views.submenu import Debug as subDebug
from views.Console import Console

class Menu(tk.Menu):
    def __init__(self, *args, **kwargs):
        tk.Menu.__init__(self, *args, **kwargs)

    def setUp(self, file, debug):
        subFile.setUp(menubar=self, objFile=file)
        subDebug.setUp(menubar=self, interpreter=debug)

class Editor(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = TextBox.setUp(self)

    def get_text(self):
        return self.text

def setUp_Logger(log_level):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=log_level,
                        format='%(name)s:%(levelname)s: %(message)s')

if __name__ == "__main__":
    setUp_Logger(logging.INFO)
    root = tk.Tk()
    console = Console(root)
    console.pack(side='right', fill='y', expand=True)
    editor = Editor(root)
    editor.pack(side='left', fill='y', expand=True)

    file = subFile.File(root, editor.get_text())
    debug = subDebug.Debug( editor.get_text() )
    menu = Menu(root)
    menu.setUp( file, debug )
    root.config(menu=menu)

    root.mainloop()
