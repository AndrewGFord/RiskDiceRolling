# Generates a numpy file with the probabilities used in Risk visualizations

import numpy as np
import RiskProbabilitiesLib as rpl

def generate_probabilities(die, filename, save_file):
	# generate probabilities
	# build pre-sorted dictionaries for one, two, and three dice
	for p in range(die):
		if p == 0:
			one_dict = { p: [p+1] }
		else:
			one_dict[p] = [p+1]
		for q in range(die):
			two_dict_index = die*p+q
			two_dict_entry = sorted([p+1,q+1],reverse=True)
			if two_dict_index == 0:
				two_dict = { two_dict_index: two_dict_entry }
			else:
				two_dict[two_dict_index] = two_dict_entry
			for r in range(die):
				three_dict_index = die*die*p+die*q+r
				three_dict_entry = sorted([p+1,q+1,r+1],reverse=True)
				if three_dict_index == 0:
					three_dict = { three_dict_index: three_dict_entry }
				else:
					three_dict[three_dict_index] = three_dict_entry
	
	dict_key = { 1:one_dict, 2:two_dict, 3:three_dict}
	probs = np.zeros([3,2,3])
	results = np.zeros([3,2,3])
	
	# might be able to make a dictionary of dictionaries to make this code better
	for ai in range(3):
		a_dice = ai + 1
		a_dict = dict_key[a_dice]
		for di in range(2):
			d_dice = di + 1
			d_dict = dict_key[d_dice]
			a_combs = die**a_dice
			d_combs = die**d_dice
			for a in range(a_combs):
				for d in range(d_combs):
					[a_loss,d_loss] = rpl.compare_dice(a_dict[a],d_dict[d])
					results[ai][di][a_loss] += 1
			probs[ai][di] = results[ai][di]/(a_combs*d_combs)
	
	# save probabilities to numpy file
	if save_file:
		np.save(filename, probs)
	return probs