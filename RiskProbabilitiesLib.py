## Library of helper functions for RiskProbabilities.py

# requires lists to be sorted already
def compareDice(attDice,defDice):
	attLen = len(attDice)
	defLen = len(defDice)
	comps = min(attLen,defLen)
	attLoss = 0
	defLoss = 0
	for ii in range(comps):
		if attDice[ii] > defDice[ii]:
			defLoss += 1
		else:
			attLoss += 1
	return [attLoss,defLoss]

# should only be called from selectDiceIndex(nAtt,nDef)
def selectDice(nAtt,nDef):
	if nAtt > 3:
		attDice = 3
	else:
		attDice = nAtt
	if nDef > 2:
		defDice = 2
	else:
		defDice = nDef
	return [attDice,defDice]

def selectDiceIndex(nAtt,nDef):
	[attDice,defDice] = selectDice(nAtt,nDef)
	return [attDice-1,defDice-1]

def getProbs(nAtt,nDef,probs):
	[a,d] = selectDiceIndex(nAtt,nDef)
	return probs[a,d]