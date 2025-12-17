# Calculating probabilities of results of die rolls from the board game Risk

# Attacker rolls up to 3 dice
# Defender rolls up to 2 dice
# Highest rolls from each are compared
# Defender wins ties

import numpy as np
import matplotlib.pyplot as plt
import RiskProbabilitiesLib as rpl
import RiskGenerateProbs as rgp
import os

die = 8 # number of faces on each die, 6 in standard game

### BEGINNING OF LOGIC COPIED TO RiskGenerateProbs.py
# use a try-catch to see if the probabilities already exist for the given die size
filename = 'Risk-Probabilities-'+str(die)+'-Sided-Dice.npy'
if os.path.exists(filename):
	probs = np.load(filename)
	# add try-catch here to make sure it's a valid file
else:
	# generate probabilities
	# build pre-sorted dictionaries for one, two, and three dice
	probs = rgp.generate_probabilities(die, filename)

chart_size = 30
chart = np.zeros([chart_size,chart_size])
## dimension 1 is number of attackers, dimension 2 is number of defenders

## initializing a 100% chance of the attackers winning if there are 0 defenders
for ii in range(1,chart_size):
	chart[ii][0] = 1

## filling in the case where there is 1 attacker and 1 defender
chart[1][1] = probs[0][0][0]
for ii in range(2,chart_size):
	[p0,p1,p2] = rpl.get_probs(ii,1,probs)
	chart[ii][1] = p0*chart[ii][0] + p1*chart[ii-1][1] #second term should be 0
	[p0,p1,p2] = rpl.get_probs(1,ii,probs)
	chart[1][ii] = p0*chart[1][ii-1] + p1*chart[0][ii] #first term should be 0
for m in range(2,chart_size):
	[p0,p1,p2] = rpl.get_probs(m,m,probs)
	chart[m][m] = p0*chart[m][m-2] + p1*chart[m-1][m-1] + p2*chart[m-2][m]
	for ii in range(m+1,chart_size):
		[p0,p1,p2] = rpl.get_probs(ii,m,probs)
		chart[ii][m] = (p0*chart[ii][m-2]) + (p1*chart[ii-1][m-1]) + (p2*chart[ii-2][m])
		[p0,p1,p2] = rpl.get_probs(m,ii,probs)
		chart[m][ii] = p0*chart[m][ii-2] + p1*chart[m-1][ii-1] + p2*chart[m-2][ii]

ch = plt.imshow(chart[1:chart_size,1:chart_size],cmap = 'Reds',origin='lower',extent=(0.5,chart_size-0.5,0.5,chart_size-0.5))
ticks = [i for i in range(1,chart_size)]
plt.xticks(ticks)
plt.yticks(ticks)
plt.xlabel("Defending Army Size")
plt.ylabel("Attacking Army Size")
plt.title("Probability of winning an attack in the board game Risk")

annotate_plot = True
if chart_size <= 11:
	font_size_str = 'medium'
elif chart_size <= 16:
	font_size_str = 'small'
elif chart_size <= 21:
	font_size_str = 'x-small'
elif chart_size <= 31:
	font_size_str = 'xx-small'
else:
	annotate_plot = False

if annotate_plot:
	for ii in range(1,chart_size):
		for jj in range(1,chart_size):
			p = chart[ii][jj]
			if p >= 0.995:
				p_str = '>.99'
			elif p < 0.005:
				p_str = '<.01'
			else:
				p_str = str("%.2f" % chart[ii][jj])
			if p > 0.5:
				c_str = 'white'
			else:
				c_str = 'black'
			plt.annotate(p_str, xy=(jj,ii), ha='center', va='center', color=c_str, fontsize = font_size_str)

plt.show()