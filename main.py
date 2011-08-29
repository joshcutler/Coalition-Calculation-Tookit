#!/usr/bin/env python

import coalitionsolver
#***********************************************************************************************
#                     Use Coalition class to work on user input
#***********************************************************************************************
# version 1.0 coalition calculator
coal = input("Please enter the coalition in the form [x,y,z...]: ")
print "Working on this coalition: ", coal
coalition = coalitionsolver.Coalition(coal)

if coalition.size() <= 2:
  print("Exiting, Coalition size must be greater than 2")
  exit();

# generate simple majority u
E = coalition.size()
u = coalition.majority_size()

print "\nPulp List"
print coalition._pulp_list

print "\nTie List"
print coalition._tie_list

print "\nMWC: "
print coalition._MWC

print "\nRank: ", coalition._rank

coalition.get_minimum_integer_solution()

#Other stuff....
#************************************************************************************************
#tkeys = MWC.keys()
#organize MWC's by party
#for i in range(0,T):
#    print "Player ", i+1, "'s coalitions:"
#    for j in range(0, len(tkeys)):
#        if coal[i] in tkeys[j]: print "Coalition: ",tkeys[j]," / Size: ",MWC[tkeys[j]]
#    print
#num_coals = len(coalition._MWC)
#print "Number of distinct coalitions: ", num_coals

# pulp code

#for k in varnames:
#    if rank[k]>0:
#        prob += coal_vars[k]>=1, "final constraint "+str(k)

#The constraints are entered
#prob += w1 + w2 - w3 - w4 >=1, "coalition 1"
#prob += w1 - w2 + w3 - w4 >=1, "coalition 2"
#prob += w1 - w2 - w3 + w4 >=1, "coalition 3"
#prob += -w1 + w2 + w3 + w4 >=1, "coalition 4"
#prob += w1 - w2 >=0, "coalition 5"
#prob += w2 - w3 >=0, "coalition 6"
#prob += w3 - w4 >=0, "coalition 7"
#prob += w4 >=0, "coalition 8"