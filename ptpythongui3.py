#!/usr/bin/env python
# GUI Tkinter
# Inga Melkerte
# C00184799
from __future__ import unicode_literals

from tkinter import *
from tkinter.ttk import *
from notebook import Window
import tkinter.scrolledtext as ScrolledText
from tkinter.filedialog import asksaveasfilename, askopenfilename
import traceback
import sys
from prompt_toolkit.history import FileHistory
from prompt_toolkit.contrib.completers import WordCompleter
import os


class Display(Frame):
    def __init__(self, parent=0):
        Frame.__init__(self, parent)
        self.master.title("PtpythonGUI")
        self.namespace = {}
        self.createWidgets()
        self.createMenu()
        self.createNotebook()
        self.createButtons()
        self.createOutput()
               
    def createWidgets(self):
        # top for notebook with tabs and scrollbar
        self.top = Frame(self)
       
        # middle for buttons
        self.middle = Frame(self)
 
        # bottom for output text
        self.bottom = Frame(self)
        self.top.pack(expand=YES, fill=BOTH, side=TOP)
        self.middle.pack(pady= 15)
        self.bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
    
    ### notebook with tabs,text,scrollbar,lineNo from notebook.py
    def createNotebook(self):
        self.prompt = ">>>"
        self.note = Window(self)
        self.note.fileName = "Tab"
        self.note.createtext()
        self.note.pack(in_=self.top, fill=BOTH, expand=True)
        self.note.text.insert("1.0", self.prompt, ("prompt",))
        self.note.text.bind('<F3>', self.onF3Key)
        self.note.text.bind('<Up>', self.onArrowKeyUP)
        
    def createMenu(self):
        self.menubar = Menu(self.master, font=("Courier", 11))
        self.master.config(menu=self.menubar)   
        self.fileMenu()
        self.editMenu()        
        self.helpMenu()        
        
    def fileMenu(self):
        # tearoff - takes off the dashed line
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label='Run', command=self.runButton)
        menu.add_command(label='Open', command=self.openButton)
        menu.add_command(label='Save', command=self.saveButton)        
        menu.add_command(label='Clear Screen', command=self.clearButton)
        menu.add_command(label='New Tab', command=self.newButton)
        # add separated line between exit
        menu.add_separator()
        menu.add_command(label='Exit', command=self.on_quit)
        self.menubar.add_cascade(label='File', underline=0, menu=menu)
        
    def editMenu(self):
        # tearoff - takes off the dashed line
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label='Cut', command=self.cut)
        menu.add_command(label='Paste', command=self.paste)
        # menu.add_command(label='Paste', command=self.onF3Key)
        # menu.add_command(label='Undo', command=self.onF3Key)
        # menu.add_command(label='Find', command=self.onF3Key)
        self.menubar.add_cascade(label='Edit', underline=0, menu=menu)        
        
    def cut(self):
        # remove prompt 
        self.note.text.delete("1.0", "1.3" )
        text = self.note.text.get("1.0", "end") 
        self.note.text.delete("1.0", "end")     
        self.clipboard_clear()              
        self.clipboard_append(text)       
        # add prompt back
        self.note.text.insert("1.0", self.prompt, ("prompt",))
                
    def paste(self):
        text = self.selection_get(selection='CLIPBOARD')
        self.note.text.insert(INSERT, text)
                
    def helpMenu(self):
        # tearoff - takes off the dashed line
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label='About', command=self.onF3Key)
        self.menubar.add_cascade(label='Help', underline=0, menu=menu)

       
#################################################################
#                           HISTORY                             #
#################################################################        
   
    def onF3Key(self,event): 
        our_history = FileHistory('.example-history-file')
        self.history=our_history
        text = []
        root = Tk()
        root.title("History")
        textscroll = ScrolledText.ScrolledText(root,  width=87, height=10,font=("Courier", 12))
        #textarea= Text(root, height=20, width=20)
        textscroll.pack()
        for word in self.history.strings:            
           textscroll.insert("end", word + "\n")
        root.mainloop()
        # self.note.text.insert("end",word + "\n")
        # messagebox.showinfo('History', mytuple) 
        # create new window         
        # first need to clear screen
        # self.note.text.delete("1.0", "end" )
        # self.history.append("print")
        # buffer=Buffer()
        # line = buffer.text
        # a = auto_suggest(self.note.text.get("1.0", END))   
            # self.note.text.insert("end", history.strings)
            # if auto_suggest.index:
            #self.note.text.insert("end",self)
        # print(str(dir(buffer.history)))       
        # print(str(dir(history))) 
        

#################################################################
#                     AUTOCOMPLETION                            #
#################################################################       
    
    def onArrowKeyUP(self, event):
        self.animal_completer = WordCompleter([
            'alligator',
            'ant',
            'ape',
            'bat',
            'bear',
            'beaver',
            'bee',
            'bison',
            'butterfly',
            'cat',
    ], ignore_case=True)
        self.completer=self.animal_completer
        self.complete_while_typing=False
        self.note.text.insert("end",self.completer.words)
       
        self.note.text.insert("end","\n")
        self.note.text.insert("end","\n")
        self.note.text.insert("end","get_completions\n")
        self.note.text.insert("end",self.completer.get_completions)
        self.note.text.insert("end","\n")
        
        self.note.text.insert("end","\n")
        self.note.text.insert("end","completer.words\n")
        for word in self.completer.words:
            self.note.text.insert("end",word + "\n")
        print(str(dir(self.completer)))
        
        
#################################################################
#                     AUTO-SUGGESTION                           #
#################################################################                    
 
        '''our_history = FileHistory('.example-history-file')
        self.history=our_history
        self.auto_suggest = AutoSuggestFromHistory()
        self.enable_history_search=True   
       # print(str(dir(AutoSuggestFromHistory().get_suggestion)))
        self.note.text.insert("end", self.auto_suggest)
        # print(str(dir(self.auto_suggest.get_suggestion)))'''


        
#################################################################
#                           BUTTONS                             #
#################################################################
        
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
        self.output = ScrolledText.ScrolledText(self,  width = 87, height = 10,font=("Courier", 13))
        self.output.pack( pady = 10)
        self.output.configure(state = "disable")
            
        sys.stdout = self
        self.pack()     
    
       
    def runButton(self):
        # remove prompt, so it can evaluate the text
        self.note.text.delete("1.0", "1.3" )
        try:
            #get text from text area
            line = self.note.text.get("1.0", END)
            #store it into the history file
            our_history = FileHistory('.example-history-file')
            self.history=our_history
            self.history.append(line)
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
        # insert back prompt, so it looks nice       
        self.note.text.insert("1.0", self.prompt, ("prompt",))
        
        
    def clearButton(self):
         self.note.text.delete("1.0", END) 
         self.note.text.focus()
         # clear screen and put back the prompt
         self.note.text.insert("1.0", self.prompt, ("prompt",))
          
          
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
        self.note.text.focus()
       # print("nothing")
       
       
    def on_quit(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.quit()   
        
if __name__ == '__main__':
    Display().mainloop()
