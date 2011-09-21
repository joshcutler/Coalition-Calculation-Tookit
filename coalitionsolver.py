import random
import numpy
import math
import sys
from pulp import *

class Coalition:
  def __init__(self, coalition_array):
    self._coalition_array = []
    self._all_coalitions = {}
    self._pulp_list = []
    self._tie_list = []
    self._temp_list = []
    self._rank = []
    self._MWC = {}

    self._party_filter = []
    self._tie_filter = []
    self._varnames = []
    self._lp_status = "Undetermined"
    self._lp_vars = []
    self._lp_var_results = "Unknown"
    self._lp_total = "Unknown"
    
    coalition_array.sort(reverse=True)
    self._coalition_array = coalition_array
    self.generate_all_subcoalitions()
    self.generate_MWC()
    self.generate_gamson_values()
    self.generate_ordinal_rank()
  
  def size(self):
    return len(self._coalition_array)
  
  def total_votes(self):
    return sum(self._coalition_array)
    
  def majority_size(self):
    return math.floor(sum(self._coalition_array) / 2 ) + 1
  
  def maximum_coalition_size(self):
    _max_size = 0
    for subcoal in self._pulp_list:
      if len(subcoal) > _max_size: _max_size = len(subcoal)
    return _max_size
  
  def generate_all_subcoalitions(self):
    L = []
    for i in range(1, self.size()):
      self._recursive_sub_coalition_generation(self._coalition_array, i , 0, L, self._temp_list)
  
  def generate_MWC(self):
    #now that we have all coalitions, check to see those that are MWC's
    #create new dictionary MWC
    self._MWC = self._all_coalitions.copy()

    _majority_size = self.majority_size()
    # delete non-winning coalitions
    for i in self._MWC.keys():
      if self._MWC[(i)] < _majority_size: del self._MWC[(i)]

    # delete too large coalitions
    for i in self._MWC.keys():
      temp_coal = i
      for j in temp_coal:
        if (self._MWC[(i)] - j) >= _majority_size:
          del self._MWC[(i)]
          break
  
  def generate_ordinal_rank(self):
    for i in range(0, self.size()):
      self._rank.append(0)
   
    _max_size = self.maximum_coalition_size()
    t_mwc = len(self._pulp_list)
    k = 2
    t_dummy = 0
    while k < _max_size + 1:
      for i in range(0, len(self._pulp_list)):
        for j in self._pulp_list[i]:
          if len(self._pulp_list[i]) == k:
            self._rank[j] = self._rank[j] + ((_max_size - k) * (_max_size - k) + 1 ) * t_mwc
            t_dummy = t_dummy + 1
      ranked = 1
      t_mwc = t_mwc - t_dummy
      t_dummy = 0
      for l in range(0, self.size() - 1):
        if self._rank[l] == self._rank[l + 1] and self._coalition_array[l] != self._coalition_array[l + 1]:
          k += 1
          ranked = 0
          break
      if ranked == 1: 
        break
              
  def _recursive_sub_coalition_generation(self, tcoal, tlim, n, L1, tl):
    # tcoal is coalition list, tlim is # of parties in coal, n is starting party
    # and L1 is list of coalitions used to fill dictionary coal_list
    u = self.majority_size()
    for j in range(n, self.size() - tlim + 1):
      tl.append(j)
      L1.append(tcoal[j])
      if tlim - 1 > 0:
        self._recursive_sub_coalition_generation(tcoal, tlim - 1, j + 1, L1, tl)
      if tlim == 1:
        tsum = 0
        for z in range(0, len(L1)): tsum = tsum + L1[z]
        self._all_coalitions[tuple(L1)] = tsum
        if self.total_votes()%2 == 0 and tsum == (u - 1):
          self._tie_list.append(tuple(tl))
        elif tsum >= u:
          self._pulp_list.append(tuple(tl))
          for k in L1:
            if tsum - k >= u:
              self._pulp_list.pop()
              break
      L1.pop()
      tl.pop() 
    return 0
    
  def generate_variable_names(self):
    # generate variable names for parties
    self._varnames=[]
    for i in range(0, self.size()):
      tempname = i
      self._varnames.append(tempname)
    
  def generate_lp_constraints(self):  
    #create filters for weights
    row = []
    for i in range(0, len(self._pulp_list)):
      for j in range(0,len(self._varnames)):
        row.append(-1)
      self._party_filter.append(row)
      row = []

    for i in range (0, len(self._pulp_list)):
      for j in self._pulp_list[i]:
        self._party_filter[i][j] = 1

    row = []
    for i in range(0, len(self._tie_list)):
      for j in range(0,len(self._varnames)):
        row.append(-1)
      self._tie_filter.append(row)
      row = []

    for i in range (0, len(self._tie_list)):
      for j in self._tie_list[i]:
        self._tie_filter[i][j] = 1
        
  def get_minimum_integer_solution(self):
    self.generate_variable_names()
    self.generate_lp_constraints()
    
    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("Minimum Integer Weights", LpMinimize)

    coal_vars = LpVariable.dicts("weight", self._varnames, 0, None, LpInteger)

    # The objective function is added to 'prob' first
    prob += lpSum([coal_vars[i] for i in self._varnames]), "Minimize Weights"

    # The constraints are added to 'prob'
    for i in range(0, len(self._pulp_list)):
      prob += lpSum([self._party_filter[i][j] * coal_vars[j] for j in self._varnames]) >= 1, "coalition constraint " + str(i)

    for i in range(0, len(self._tie_list)):
      prob += lpSum([self._tie_filter[i][j] * coal_vars[j] for j in self._varnames]) == 0, "tie constraint " + str(i)

    #this is a kludge; there must be a better way
    for k in range(0, self.size() - 1):
        if self._rank[k] > self._rank[k+1]:
            prob += coal_vars[k] - coal_vars[k + 1] >= 1, "rank constraint " + str(k)
        elif self._rank[k] == self._rank[k  +1]:
            prob += coal_vars[k] - coal_vars[k+1] == 0, "rank constraint " + str(k)    

    if self._rank[self.size() - 1]> 0: prob += coal_vars[self.size() - 1] >= 1, "final rank constraint"
    
    # The problem data is written to an .lp file
    prob.writeLP("bargain.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    self._lp_status = LpStatus[prob.status]

    # Each of the variables is printed with it's resolved optimum value
    self._lp_vars = prob.variables()
    self._lp_vars.sort(key=lambda var: var.name)
    self._lp_var_results = ""
    for v in self._lp_vars:
      self._lp_var_results += "\n" + str(v.name) + "=" + str(v.varValue)

    # The optimised objective function value is printed to the screen
    self._lp_total = value(prob.objective)
    
  def generate_gamson_values(self):
    #Do something
    self._gamson_values = [None]*self.size()
    #Iterate over each player
    _mwcs = self._MWC.keys()
    for i in range(0, self.size() - 1):
      #See if they are in any MWCs
      smallest_mwc = ()
      for j in range(0, len(_mwcs) - 1):
        try:
          _mwcs[j].index(self._coalition_array[i])
          if sum(smallest_mwc) == 0 or sum(smallest_mwc) > sum(mwcs[j]):
            smallest_mwc = _mwcs[j]
        except:
          continue
      if sum(smallest_mwc) > 0:
        self._gamson_values[i] = round(float(self._coalition_array[i]) / sum(smallest_mwc), 2)