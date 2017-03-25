#!/usr/bin/env python
# GUI Tkinter
# Inga Melkerte
# C00184799
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfilename,askopenfilename
import traceback, sys
import tkinter.scrolledtext as ScrolledText
from notebook import Window
#from ptpython.repl import PythonCommandLineInterface
from prompt_toolkit.history import FileHistory
from prompt_toolkit.interface import AbortAction
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# from prompt_toolkit import prompt
# from prompt_toolkit.key_binding.defaults import load_key_bindings_for_prompt
# from prompt_toolkit.keys import Keys


class Display(Frame):
       
    def __init__(self, parent=0):
        Frame.__init__(self, parent)
        self.master.title("PtpythonGUI")
        self.namespace = {}
        self.createWidgets()
        self.createNotebook()
        self.createButtons()
        self.createOutput()
      
    def createWidgets(self):
          
        # top for noteboob with text and scrollbar
        self.top = Frame(self)
       
        # middle for buttons
        self.middle = Frame(self)
 
        # bottom for output text 
        self.bottom = Frame(self)
     
        self.top.pack(expand =YES, fill = BOTH, side = TOP)
        self.middle.pack(pady= 15)
        self.bottom.pack(side = BOTTOM, fill = BOTH, expand = True)
    
    
    ### notebook with tabs,text,scrollbar,lineNo from notebook.py
    def createNotebook(self):
        self.prompt = ">>>"
        self.note = Window(self)
      
        self.note.fileName = "Tab"
        self.note.createtext()
        self.note.pack(in_= self.top, fill= BOTH, expand = True)
        
        self.note.text.insert("1.0", self.prompt, ("prompt",))
        self.note.text.bind('<Up>',self.onArrowKey)
        
    

    
    def onArrowKey(self,event): 
        our_history = FileHistory('.example-history-file')
#history=our_history
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
        on_abort=AbortAction.RETRY
       # self.text.insert("end", history.strings, auto_suggest.index )
       # a = auto_suggest(self.note.text.get("1.0", END))
      
        for word in our_history.strings:
            if auto_suggest.index:
                #self.note.text.insert("end",self)
                self.note.text.insert("end",word + "\n")
                
        #print(str(dir( auto_suggest.index)))
        print(str(dir()))   
    def createButtons(self):        
        self.button1 = Button(self,text="Run", command=self.runButton)
        self.button1.pack(in_=self.middle, side = LEFT, padx = 5)  
        
        self.button2 = Button(self,text="Open", command=self.openButton)
        self.button2.pack(in_=self.middle,side = LEFT, padx = 5)    
       
        self.button3 = Button(self,text="Save", command=self.saveButton)
        self.button3.pack(in_=self.middle, side = LEFT, padx = 5)   
       
        self.button4 = Button(self,text="Clear Screen", command=self.clearButton)
        self.button4.pack(in_=self.middle, side = LEFT, padx = 5) 
       
        self.button5 = Button(self,text="New", command=self.newButton)
        self.button5.pack(in_=self.middle, side = LEFT, padx = 5) 
       
       
    def createOutput(self):
        self.output = ScrolledText.ScrolledText(self,  width = 87, height = 10,font=("Courier", 12))
        self.output.pack( pady = 10)
        self.output.configure(state = "disable")
            
        sys.stdout = self
        self.pack()
       
       
    
       
    def runButton(self):

        try:
        
            result = eval(self.note.text.get("1.0", END))
            if result:
                print (str(result))
        except SyntaxError:
            try:
                result = exec(self.note.text.get("1.0", END), self.namespace)
            except:
                #assign sys.exc_info() to access (type, value, traceback).
                error = sys.exc_info()
                print(error[0],error[1]) 
               
        #self.text.delete("1.0", END)
    def clearButton(self):
         self.note.text.delete("1.0", END)  
          
    def openButton(self):
        filenameforReading = askopenfilename()
        infile = open(filenameforReading, "r")
        self.note.text.insert(END, infile.read())
        infile.close()        
        
    def saveButton(self):
        filenameforWriting = asksaveasfilename()
        outfile = open(filenameforWriting, "w")
        # Write to the file
        outfile.write(self.note.text.get(1.0, END)) 
        outfile.close()

    def write(self, txt):
        #enable text area to output result
        self.output.configure(state="normal")
        self.output.insert(END,str(txt))
        #disable again
        self.output.configure(state="disable")
    
    def newButton(self):
        self.note.addtab()
        self.note.focus()
       # print("nothing")
        
        
if __name__ == '__main__':
    Display().mainloop()
