#!/usr/bin/env pythonimport numpyimport mathimport sysfrom pulp import *class Coalition:  _coalition_array = []  _all_coalitions = {}  _pulp_list = []  _tie_list = []  _temp_list = []  _rank = []  _MWC = {}    def __init__(self, coalition_array):    self._coalition_array = coalition_array    self.generate_all_subcoalitions()    self.generate_MWC()    self.generate_ordinal_rank()    def size(self):    return len(self._coalition_array)      def majority_size(self):    return math.floor(sum(self._coalition_array) / 2 ) + 1    def maximum_coalition_size(self):    _max_size = 0    for subcoal in self._pulp_list:      if len(subcoal) > _max_size: max_size = len(subcoal)    return _max_size    def generate_all_subcoalitions(self):    L = []    for i in range(1, self.size()):      self._recursive_sub_coalition_generation(self._coalition_array, i , 0, L, self._temp_list)    def generate_MWC(self):    #now that we have all coalitions, check to see those that are MWC's    #create new dictionary MWC    self._MWC = self._all_coalitions.copy()    _majority_size = self.majority_size()    # delete non-winning coalitions    for i in self._MWC.keys():      if self._MWC[(i)] < _majority_size: del self._MWC[(i)]    # delete too large coalitions    for i in self._MWC.keys():      temp_coal = i      for j in temp_coal:        if (self._MWC[(i)] - j) >= _majority_size:          del self._MWC[(i)]          break    def generate_ordinal_rank(self):    for i in range(0, self.size()):      self._rank.append(0)       _max_size = self.maximum_coalition_size()    t_mwc = len(self._pulp_list)    k = 2    t_dummy = 0    while k < _max_size + 1:      for i in range(0, len(self._pulp_list)):        for j in self._pulp_list[i]:          if len(self._pulp_list[i]) == k:            self._rank[j] = self._rank[j] + ((_max_size - k) * (_max_size - k) + 1 ) * t_mwc            t_dummy = t_dummy + 1        ranked = 1        t_mwc = t_mwc - t_dummy        t_dummy = 0        for l in range(0, self.size() - 1):          if self._rank[l] == self._rank[l + 1] and self._coalition_array[l] != self._coalition_array[l + 1]:            k = k + 1            ranked = 0            break        if ranked == 1:           break                def _recursive_sub_coalition_generation(self, tcoal, tlim, n, L1, tl):    # tcoal is coalition list, tlim is # of parties in coal, n is starting party    # and L1 is list of coalitions used to fill dictionary coal_list    u = self.majority_size()    for j in range(n, self.size() - tlim + 1):      tl.append(j)      L1.append(tcoal[j])      if tlim - 1 > 0:        self._recursive_sub_coalition_generation(tcoal, tlim - 1, j + 1, L1, tl)      if tlim == 1:        tsum = 0        for z in range(0, len(L1)): tsum = tsum + L1[z]        self._all_coalitions[tuple(L1)] = tsum        if self.size()%2 == 0 and tsum == (u - 1):          self._tie_list.append(tuple(tl))        elif tsum >= u:          self._pulp_list.append(tuple(tl))          for k in L1:            if tsum - k >= u:              self._pulp_list.pop()              break      L1.pop()      tl.pop()     return 0    # version 1.0 coalition calculatorcoal = input("Please enter the coalition in the form [x,y,z...]: ")print "Working on this coalition: ", coalcoalition = Coalition(coal)if coalition.size() <= 2:  print("Exiting, Coalition size must be greater than 2")  exit();# generate simple majority uE = coalition.size()u = coalition.majority_size()# generate variable names for partiesvarnames=[]for i in range(0, coalition.size()):  tempname = i  varnames.append(tempname)  tempname = ""print "\nPulp List"print coalition._pulp_listprint "\nTie List"print coalition._tie_listprint "\nMWC: "print coalition._MWCprint "\nRank: ", coalition._ranktkeys = MWC.keys()#organize MWC's by party#for i in range(0,T):#    print "Player ", i+1, "'s coalitions:"#    for j in range(0, len(tkeys)):#        if coal[i] in tkeys[j]: print "Coalition: ",tkeys[j]," / Size: ",MWC[tkeys[j]]#    printnum_coals = len(MWC)#print "Number of distinct coalitions: ", num_coals# pulp code#create filters for weightsparty_filter = []tie_filter = []row = []for i in range(0, len(pulp_list)):    for j in range(0,len(varnames)):        row.append(-1)    party_filter.append(row)    row = []for i in range (0, len(pulp_list)):    for j in pulp_list[i]:        party_filter[i][j] = 1row = []for i in range(0, len(tie_list)):    for j in range(0,len(varnames)):        row.append(-1)    tie_filter.append(row)    row = []for i in range (0, len(tie_list)):    for j in tie_list[i]:        tie_filter[i][j] = 1# Create the 'prob' variable to contain the problem dataprob = LpProblem("Minimum Integer Weights", LpMinimize)coal_vars = LpVariable.dicts("weight",varnames, 0, None, LpInteger)# The objective function is added to 'prob' firstprob += lpSum([coal_vars[i] for i in varnames]), "Minimize Weights"# The constraints are added to 'prob'for i in range(0, len(pulp_list)):    prob += lpSum([party_filter[i][j] * coal_vars[j] for j in varnames]) >= 1, "coalition constraint "+str(i)for i in range(0, len(tie_list)):    prob += lpSum([tie_filter[i][j] * coal_vars[j] for j in varnames]) == 0, "tie constraint "+str(i)#this is a kludge; there must be a better wayfor k in range(0, coalition.size() - 1):    if rank[k] > rank[k+1]:        prob += coal_vars[k] - coal_vars[k + 1] >= 1, "rank constraint " + str(k)    elif rank[k]==rank[k  +1]:        prob += coal_vars[k] - coal_vars[k+1] == 0, "rank constraint " + str(k)    if rank[coalition.size() - 1]> 0: prob += coal_vars[coalition.size() - 1] >= 1, "final rank constraint"#for k in varnames:#    if rank[k]>0:#        prob += coal_vars[k]>=1, "final constraint "+str(k)#The constraints are entered#prob += w1 + w2 - w3 - w4 >=1, "coalition 1"#prob += w1 - w2 + w3 - w4 >=1, "coalition 2"#prob += w1 - w2 - w3 + w4 >=1, "coalition 3"#prob += -w1 + w2 + w3 + w4 >=1, "coalition 4"#prob += w1 - w2 >=0, "coalition 5"#prob += w2 - w3 >=0, "coalition 6"#prob += w3 - w4 >=0, "coalition 7"#prob += w4 >=0, "coalition 8"# The problem data is written to an .lp fileprob.writeLP("bargain1.lp")# The problem is solved using PuLP's choice of Solverprob.solve(GLPK(msg = 0))# The status of the solution is printed to the screenprint "\nStatus:", LpStatus[prob.status]# Each of the variables is printed with it's resolved optimum valuefor v in prob.variables():    print v.name, "=", v.varValue# The optimised objective function value is printed to the screenprint "Total = ", value(prob.objective)