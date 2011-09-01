#!/usr/local/bin/python     
from Tkinter import *
import tkMessageBox 
import coalitionsolver

class Application(Frame):              
  def __init__(self, master=None):
    Frame.__init__(self, master, bg="#CCC")   
    self.grid(sticky=N+E+S+W)                    
    top = self.winfo_toplevel()                
    top.rowconfigure(0, weight=1)            
    top.columnconfigure(0, weight=1)
    self.create_widgets()

  def create_widgets(self):
    #Create the text labels
    self.lbl_input_instructions = Label(self, justify=LEFT,
      text="Enter in a coalition below.  You must specify it as an array of comma seperated integers enclosed in brackets.  \nFor example if you had coalitions of sizes 1, 2 and 3 your input should look like this: [1,2,3]")
    self.lbl_input_instructions.grid(row=1)
    
    #Create the text input
    self.entry_coalition_input = Entry(self)
    self.entry_coalition_input.grid(row=2)
    
    #Create the "Process" button
    self.btn_process = Button(self, text="Process", command=self.process_input)
    self.btn_process.grid(row=3)
    
  def process_input(self):
    _inp_coal = self.entry_coalition_input.get()
#    try:
    _coal_array = eval(_inp_coal)
    coalition = coalitionsolver.Coalition(_coal_array)
    
    if coalition.size() <= 2:
      tkMessageBox.showerror("Coalition size too small", "Coalition size must be greater than 2")
      return 
      
    print "\nInput Array"
    print coalition._coalition_array
      
    print "\nPulp List"
    print coalition._pulp_list

    print "\nTie List"
    print coalition._tie_list

    print "\nMWC: "
    print coalition._MWC

    print "\nRank: ", coalition._rank

    coalition.get_minimum_integer_solution()
#    except:
#      print "Unexpected error:", sys.exc_info()[0]
#      tkMessageBox.showerror("Error processing input", "There was an error with your input.  Please make that it was formatted correctly")

app = Application()                    
app.master.title("Minimum Winning Coalition Solver") 
app.mainloop()                         
