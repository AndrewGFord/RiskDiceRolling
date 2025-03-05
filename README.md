# RiskDiceRolling
This code generates visualizations of the probability of winning a battle in the board game Risk for various starting army sizes.

The attacking army size does not include the single troop which must be left behind in the attacking territory.

# Running the code
The script which generates the visualization is found in RiskProbabilities.py. A library of helper functions is found in RiskProbabilitiesLib.py. A visualization for battles up to 10 attackers and 10 defenders is also included.

# Color scheme
The color scheme of the visualizations was chosen to represent the dice used in the game. The attacker's dice are red with white pips, and the defender's dice are white with black pips. To represent this, the background of each cell in the visualization is colored on a white-red spectrum. The text is white when the attacker is more likely to win, and the text is black when the defender is more likely to win.

When the size of the chart is sufficiently large, the text with probabilities is removed.