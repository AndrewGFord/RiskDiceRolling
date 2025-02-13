# Calculating probabilities of results of die rolls from the board game Risk

# Attacker rolls up to 3 dice
# Defender rolls up to 2 dice
# Highest rolls from each are compared
# Defender wins ties

import numpy as np
import matplotlib.pyplot as plt
import RiskProbabilitiesLib as rpl

# future idea: add a variable to simulate other die sizes?

# building pre-sorted dictionaries for one, two, and three dice
for p in range(6):
	if p == 0:
		oneDict = { p: [p+1] }
	else:
		oneDict[p] = [p+1]
	for q in range(6):
		twoDictIndex = 6*p+q
		twoDictEntry = sorted([p+1,q+1],reverse=True)
		if twoDictIndex == 0:
			twoDict = { twoDictIndex: twoDictEntry }
		else:
			twoDict[twoDictIndex] = twoDictEntry
		for r in range(6):
			threeDictIndex = 36*p+6*q+r
			threeDictEntry = sorted([p+1,q+1,r+1],reverse=True)
			if threeDictIndex == 0:
				threeDict = { threeDictIndex: threeDictEntry }
			else:
				threeDict[threeDictIndex] = threeDictEntry

dictKey = { 1:oneDict, 2:twoDict, 3:threeDict}
probs = np.zeros([3,2,3])
results = np.zeros([3,2,3])

# might be able to make a dictionary of dictionaries to make this code better
for ai in range(3):
	aDice = ai + 1
	aDict = dictKey[aDice]
	for di in range(2):
		dDice = di + 1
		dDict = dictKey[dDice]
		aCombs = 6**aDice
		dCombs = 6**dDice
		for a in range(aCombs):
			for d in range(dCombs):
				[aLoss,dLoss] = rpl.compareDice(aDict[a],dDict[d])
				results[ai][di][aLoss] += 1
		probs[ai][di] = results[ai][di]/(aCombs*dCombs)

chartSize = 11
chart = np.zeros([chartSize,chartSize])
## dimension 1 is number of attackers, dimension 2 is number of defenders

## initializing a 100% chance of the attackers winning if there are 0 defenders
for ii in range(1,chartSize):
	chart[ii][0] = 1

## filling in the case where there is 1 attacker and 1 defender
chart[1][1] = probs[0][0][0]
for ii in range(2,chartSize):
	[p0,p1,p2] = rpl.getProbs(ii,1,probs)
	chart[ii][1] = p0*chart[ii][0] + p1*chart[ii-1][1] #second term should be 0
	[p0,p1,p2] = rpl.getProbs(1,ii,probs)
	chart[1][ii] = p0*chart[1][ii-1] + p1*chart[0][ii] #first term should be 0
for m in range(2,chartSize):
	[p0,p1,p2] = rpl.getProbs(m,m,probs)
	chart[m][m] = p0*chart[m][m-2] + p1*chart[m-1][m-1] + p2*chart[m-2][m]
	for ii in range(m+1,chartSize):
		[p0,p1,p2] = rpl.getProbs(ii,m,probs)
		chart[ii][m] = (p0*chart[ii][m-2]) + (p1*chart[ii-1][m-1]) + (p2*chart[ii-2][m])
		[p0,p1,p2] = rpl.getProbs(m,ii,probs)
		chart[m][ii] = p0*chart[m][ii-2] + p1*chart[m-1][ii-1] + p2*chart[m-2][ii]

ch = plt.imshow(chart[1:chartSize,1:chartSize],cmap = 'Reds',origin='lower',extent=(0.5,chartSize-0.5,0.5,chartSize-0.5))
ticks = [i for i in range(1,chartSize)]
plt.xticks(ticks)
plt.yticks(ticks)
plt.xlabel("Defending Army Size")
plt.ylabel("Attacking Army Size")
plt.title("Probability of winning an attack in the board game Risk")

for ii in range(1,chartSize):
	for jj in range(1,chartSize):
		p = chart[ii][jj]
		if p >= 0.995:
			pStr = '>0.99'
		elif p < 0.005:
			pStr = '<0.01'
		else:
			pStr = str("%.2f" % chart[ii][jj])
		if p > 0.5:
			cStr = 'white'
		else:
			cStr = 'black'
		plt.annotate(pStr, xy=(jj,ii), ha='center', va='center', color=cStr)

plt.show()