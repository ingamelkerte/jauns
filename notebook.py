# taken from stackoverflow http://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget/16375233#16375233
# Inga Melkerte
# c00184799
import tkinter as tk
import tkinter.ttk as ttk


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        ##
        

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(5,y,anchor="nw", text=linenum, font=("Courier", 13))
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text): 
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # generate the event for certain types of commands
                if {([lindex $args 0] in {insert replace delete}) ||
                    ([lrange $args 0 2] == {mark set insert}) || 
                    ([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {

                    event generate  $widget <<Change>> -when tail
                }

                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))

        self.comment = False

class Window(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.fileName = 'Tab'
        self.notebook = ttk.Notebook(self)
        # self.menubar()
        #self.createtext()

    def createtext(self):
    
        #self.prompt = ">>>"
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.text = CustomText(self.tab1, bd=0, font=("Courier", 13))  

        self.vsb = tk.Scrollbar(self.tab1, orient=tk.VERTICAL)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.configure(command=self.text.yview)

        self.linenumbers = TextLineNumbers(self.tab1, width=55)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.text.focus()
        self.notebook.add(self.tab1, text=self.fileName)
        #self.text.insert("end", self.prompt, ("prompt",))
       # self.text.bind('<Up>',self.onArrowKey)
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
    

    def addtab(self):
        self.newTab = ttk.Frame(self.notebook)
       
        self.text = CustomText(self.newTab, bd=0, font=("Courier", 13))  

        self.vsb = tk.Scrollbar(self.newTab, orient=tk.VERTICAL)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.configure(command=self.text.yview)

        self.linenumbers = TextLineNumbers(self.newTab, width=55)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.notebook.add(self.newTab, text=self.fileName)
        self.notebook.select(self.newTab)# focuses on the new added file

      
    def menubar(self):
        self.menu = tk.Menu(self)
        self.master.config(menu=self.menu)

        self.fileMenu = tk.Menu(self.menu, font=("Courier", 13))
        self.fileMenu.add_command(label="New Window", command=self.addtab)
        self.menu.add_cascade(label="Window", menu=self.fileMenu)

    def _on_change(self, event):
        self.linenumbers.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Window")
    root.geometry("1024x600")
    window = Window(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
