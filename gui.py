#!/usr/local/bin/python     
from Tkinter import *
import tkMessageBox 
import coalitionsolver

class Application(Frame):              
  def __init__(self, master=None):
    Frame.__init__(self, master)   
    self.grid(sticky=N+E+S+W)                    
    top = self.winfo_toplevel()                
    top.rowconfigure(0, weight=1)            
    top.columnconfigure(0, weight=1)
    
    self._results_text = StringVar()
    
    self.create_widgets()
    

  def create_widgets(self):
    #Create the text labels
    self.lbl_input_instructions = Label(self, justify=LEFT,
      text="Enter in a coalition below.  You must specify it as an array of comma seperated integers enclosed in brackets.  \nFor example if you had coalitions of sizes 1, 2 and 3 your input should look like this: [1,2,3]")
    self.columnconfigure(0, weight=1)
    self.lbl_input_instructions.grid(row=1, sticky=N+S+E+W)
    
    #Create the text input
    self.entry_coalition_input = Entry(self, width=75)
    self.entry_coalition_input.grid(row=2, padx=10, pady=10)
    
    #Create the "Process" button
    self.btn_process = Button(self, text="Process", command=self.process_input)
    self.btn_process.grid(row=3)
    
    #Show results
    self.msg_results = Message(self, textvariable=self._results_text, justify=LEFT, width=700)
    self.msg_results.grid(row=4, sticky=N+W)
    
  def process_input(self):
    _inp_coal = self.entry_coalition_input.get()
    # try:
    _coal_array = eval(_inp_coal)
    coalition = coalitionsolver.Coalition(_coal_array)
  
    if coalition.size() <= 2:
      self._results_text.set("Coalition size too small.  Coalition size must be greater than 2")
      return 
    
    self._results_text.set("Computing results...")
    
    results = "Input Array: \n" + str(coalition._coalition_array) + \
      "\n\nMWC: " + str(coalition._MWC) + \
      "\n\nGamson Values: " + str(coalition._gamson_values) + \
      "\n\nPulp List: \n" + str(coalition._pulp_list) + \
      "\n\nTie List: " + str(coalition._tie_list) + \
      "\n\nRank: " + str(coalition._rank)
    
    coalition.get_minimum_integer_solution()
    solved_results = "\n\nStatus: " + coalition._lp_status + \
      coalition._lp_var_results + \
      "\nTotal = " + str(coalition._lp_total)
    
    self._results_text.set(results + solved_results)
    print results + solved_results
    
    # except:
    #   print "Unexpected error: ", sys.exc_info()[0]
    #   self._results_text.set("Error with computation: " + str(sys.exc_info()[0]))
    #   tkMessageBox.showerror("Error processing input", "There was either an error with your input or a codesplosion in MIW.  Please make that it was formatted correctly or contact josh.cutler@duke.edu")

app = Application()                    
app.master.title("Bargaining Coalition Toolkit") 
app.mainloop()                         
