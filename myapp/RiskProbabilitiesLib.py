## Library of helper functions for RiskProbabilities.py

# requires lists to be sorted already
def compare_dice(att_dice,def_dice):
	att_len = len(att_dice)
	def_len = len(def_dice)
	comps = min(att_len,def_len)
	att_loss = 0
	def_loss = 0
	for ii in range(comps):
		if att_dice[ii] > def_dice[ii]:
			def_loss += 1
		else:
			att_loss += 1
	return [att_loss,def_loss]

# should only be called from select_dice_index(n_att,n_def)
def select_dice(n_att,n_def):
	if n_att > 3:
		att_dice = 3
	else:
		att_dice = n_att
	if n_def > 2:
		def_dice = 2
	else:
		def_dice = n_def
	return [att_dice,def_dice]

def select_dice_index(n_att,n_def):
	[att_dice,def_dice] = select_dice(n_att,n_def)
	return [att_dice-1,def_dice-1]

def get_probs(n_att,n_def,probs):
	[a,d] = select_dice_index(n_att,n_def)
	return probs[a,d]