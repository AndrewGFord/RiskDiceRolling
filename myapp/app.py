# Shiny app for Risk board game probability data
from shiny import App, Inputs, Outputs, Session, reactive, render, ui

import numpy as np
import matplotlib.pyplot as plt
import RiskProbabilitiesLib as rpl
import RiskGenerateProbs as rgp

die_size = 6 # Number of sides on the die
probs = rgp.generate_probabilities(die=die_size, filename='', save_file=False)
# Move these to server logic later to allow users to change die size

# TODO: Add a tab that shows the distribution of outcomes for a battle
# with a given number of attackers and defenders, and a given die size.
# This could be a bar chart with the possible outcomes on the x-axis
# and the probabilities on the y-axis.

app_ui = ui.page_fluid(
    ui.navset_pill(
        ui.nav_panel(
            'About',
            ui.h3('Risk Battle Probability Calculator'),
            ui.p('This webapp calculates and displays the probabilities of attackers winning battles in the board game Risk.'),
            ui.p('The "Probability Grid" tab shows a heatmap of the chances of attackers winning against defenders for various army sizes. The "Single Battle Probability" tab allows you to select specific numbers of attackers and defenders to see the exact probability of victory.'),
            ui.p('While this webapp tells you the probability of winning a battle when both the attacker and defender roll the optimal number of dice, it does not tell you whether attacking an opponent is a better idea than simply not fighting a specific battle.'),
            ui.p('You can adjust the number of faces on the dice used in battles, which affects the probabilities. The default is a standard 6-sided die, but dice in the shape of any other Platonic solid (4, 8, 12, or 20 faces) can be chosen.'),
            ui.p('This webapp was created using Python and the Shiny framework.'),
        ),
        ui.nav_panel(
            'Probability Grid',
            ui.h3('Probability Grid'),
            # TODO: Adjust relative sizes using CSS
            ui.card(
                ui.layout_columns(
                    ui.input_slider('chart_size_slider', 'Chart Size', min=1, max=30, value=10, width='100%'),
                    ui.input_numeric('chart_size_numeric', label = ' ', value=10, min=1, max=30, step=1),
                    col_widths=[6,2,-4],
                ),
            ),
            ui.input_selectize('die_size', 'Number of Faces on Die', choices=[4, 6, 8, 12, 20], selected=6),
            ui.output_plot('plot_probs'),
        ),
        ui.nav_panel(
            'Single Battle Probability',
            ui.h3('Single Battle Probability'),
            # TODO: Adjust relative sizes using CSS
            ui.input_selectize('die_size_single_battle', 'Number of Faces on Die', choices=[4, 6, 8, 12, 20], selected=6),
            ui.card(
                ui.layout_columns(
                    ui.input_slider('num_att_slider', 'Number of Attackers', min=1, max=30, value=1, width='100%'),
                    ui.input_numeric('num_att_numeric', label = ' ', value=1, min=1, max=30, step=1),
                    col_widths=[6,2,-4],
                ),
            ),
            ui.card(
                ui.layout_columns(
                    ui.input_slider('num_def_slider', 'Number of Defenders', min=1, max=30, value=1, width='100%'),
                    ui.input_numeric('num_def_numeric', label = ' ', value=1, min=1, max=30, step=1),
                    col_widths=[6,2,-4],
                ),
            ),
            ui.output_text('selected_probability'),
        ),
        ui.nav_panel(
            'Battle Outcome Distribution',
            ui.h3('Battle Outcome Distribution'),
            ui.p('This shows the probability distribution for the outcomes of a complete battle when starting with the given number of attackers and defenders.'),
            ui.input_selectize('die_size_dist', 'Number of Faces on Die', choices=[4, 6, 8, 12, 20], selected=6),
            ui.card(
                ui.layout_columns(
                    ui.input_slider('num_att_dist_slider', 'Number of Attackers', min=1, max=30, value=1, width='100%'),
                    ui.input_numeric('num_att_dist_numeric', label = ' ', value=1, min=1, max=30, step=1),
                    col_widths=[6,2,-4],
                ),
            ),
            ui.card(
                ui.layout_columns(
                    ui.input_slider('num_def_dist_slider', 'Number of Defenders', min=1, max=30, value=1, width='100%'),
                    ui.input_numeric('num_def_dist_numeric', label = ' ', value=1, min=1, max=30, step=1),
                    col_widths=[6,2,-4],
                ),
            ),
            ui.output_plot('plot_dist'),
            ui.output_text('dist_summary'),
        ),
    ),
)

def server(input: Inputs, output: Outputs, session: Session):
    # builds the probability chart for the chosen slider value and die size
    # called both to display chart and for the single battle probability
    @reactive.effect
    @reactive.event(input.chart_size_slider)
    def update_chart_size_numeric_from_slider():
        try:
            if input.chart_size_numeric() != input.chart_size_slider():
                ui.update_numeric(session=session, id='chart_size_numeric', value=input.chart_size_slider())
                #input.chart_size_numeric.set_value(input.chart_size_slider())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.chart_size_numeric)
    def update_chart_size_slider_from_numeric():
        try:
            if input.chart_size_slider() != input.chart_size_numeric():
                ui.update_slider(session=session, id='chart_size_slider', value=input.chart_size_numeric())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_att_slider)
    def update_num_att_numeric_from_slider():
        try:
            if input.num_att_numeric() != input.num_att_slider():
                ui.update_numeric(session=session, id='num_att_numeric', value=input.num_att_slider())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_att_numeric)
    def update_num_att_slider_from_numeric():
        try:
            if input.num_att_slider() != input.num_att_numeric():
                ui.update_slider(session=session, id='num_att_slider', value=input.num_att_numeric())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_def_slider)
    def update_num_def_numeric_from_slider():
        try:
            if input.num_def_numeric() != input.num_def_slider():
                ui.update_numeric(session=session, id='num_def_numeric', value=input.num_def_slider())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_def_numeric)
    def update_num_def_slider_from_numeric():
        try:
            if input.num_def_slider() != input.num_def_numeric():
                ui.update_slider(session=session, id='num_def_slider', value=input.num_def_numeric())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.die_size)
    def update_die_size_single_battle():
        try:
            if input.die_size_single_battle() != input.die_size():
                ui.update_selectize(session=session, id='die_size_single_battle', selected=input.die_size())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.die_size_single_battle)
    def update_die_size_from_single_battle():
        try:
            if input.die_size() != input.die_size_single_battle():
                ui.update_selectize(session=session, id='die_size', selected=input.die_size_single_battle())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_att_dist_slider)
    def update_num_att_dist_numeric_from_slider():
        try:
            if input.num_att_dist_numeric() != input.num_att_dist_slider():
                ui.update_numeric(session=session, id='num_att_dist_numeric', value=input.num_att_dist_slider())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_att_dist_numeric)
    def update_num_att_dist_slider_from_numeric():
        try:
            if input.num_att_dist_slider() != input.num_att_dist_numeric():
                ui.update_slider(session=session, id='num_att_dist_slider', value=input.num_att_dist_numeric())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_def_dist_slider)
    def update_num_def_dist_numeric_from_slider():
        try:
            if input.num_def_dist_numeric() != input.num_def_dist_slider():
                ui.update_numeric(session=session, id='num_def_dist_numeric', value=input.num_def_dist_slider())
        except:
            pass
    
    @reactive.effect
    @reactive.event(input.num_def_dist_numeric)
    def update_num_def_dist_slider_from_numeric():
        try:
            if input.num_def_dist_slider() != input.num_def_dist_numeric():
                ui.update_slider(session=session, id='num_def_dist_slider', value=input.num_def_dist_numeric())
        except:
            pass

    @reactive.calc
    def prob_chart():
        die_size = int(input.die_size()) # Number of sides on the die
        probs = rgp.generate_probabilities(die=die_size, filename='', save_file=False)

        #chart_size = input.chart_size()
        # loads a larger chart in the background, not necessarily all displayed
        chart_size = 30
        chart = np.zeros([chart_size+1, chart_size+1])

        # initialize a 100% chance of the attackers winning with 0 defenders
        for i in range(chart_size+1):
            chart[i,0] = 1

        # fill in the case where there is 1 attacker and 1 defender
        chart[1,1] = probs[0,0,0]

        # fill in the cases with 2 attackers OR 2 defenders
        for i in range(2,chart_size+1):
            [p0,p1,p2] = rpl.get_probs(i,1,probs)
            chart[i,1] = p0*chart[i,0] + p1*chart[i-1,1] # first term should be p0
            [p0,p1,p2] = rpl.get_probs(1,i,probs)
            chart[1,i] = p0*chart[1,i-1] + p1*chart[0,i] # second term should be 0
        
        # fill in the rest of the chart
        for m in range(2,chart_size+1):
            [p0,p1,p2] = rpl.get_probs(m,m,probs)
            chart[m,m] = p0*chart[m,m-2] + p1*chart[m-1,m-1] + p2*chart[m-2,m]
            for i in range(m+1,chart_size+1):
                [p0,p1,p2] = rpl.get_probs(i,m,probs)
                chart[i,m] = p0*chart[i,m-2] + p1*chart[i-1,m-1] + p2*chart[i-2,m]
                [p0,p1,p2] = rpl.get_probs(m,i,probs)
                chart[m,i] = p0*chart[m,i-2] + p1*chart[m-1,i-1] + p2*chart[m-2,i]
        
        return chart

    def compute_battle_outcome_distribution(num_att, num_def, probs, memo=None):
        """
        Analytically compute the probability distribution of battle outcomes.
        Uses recursion with memoization based on pre-computed round probabilities.
        
        Returns: (final_att_probs, final_def_probs)
        - final_att_probs[k] = probability that attackers win with k armies remaining
        - final_def_probs[k] = probability that defenders win with k armies remaining
        """
        if memo is None:
            memo = {}
        
        # Base cases
        if num_att == 0:
            final_def_probs = np.zeros(num_def + 1)
            final_def_probs[num_def] = 1.0
            final_att_probs = np.zeros(num_att + 1)
            return final_att_probs, final_def_probs
        
        if num_def == 0:
            final_att_probs = np.zeros(num_att + 1)
            final_att_probs[num_att] = 1.0
            final_def_probs = np.zeros(num_def + 1)
            return final_att_probs, final_def_probs
        
        # Check memo
        state = (num_att, num_def)
        if state in memo:
            return memo[state]
        
        # Get round probabilities
        [att_dice_idx, def_dice_idx] = rpl.select_dice_index(num_att, num_def)
        att_dice = att_dice_idx + 1
        def_dice = def_dice_idx + 1
        num_comparisons = min(att_dice, def_dice)
        
        round_probs = probs[att_dice_idx, def_dice_idx]
        outcome_probs = round_probs[:num_comparisons + 1]
        
        # Initialize result arrays
        final_att_probs = np.zeros(num_att + 1)
        final_def_probs = np.zeros(num_def + 1)
        
        # For each possible outcome of this round
        for att_losses in range(num_comparisons + 1):
            def_losses = num_comparisons - att_losses
            prob_this_outcome = outcome_probs[att_losses]
            
            # Recursively get probabilities from the resulting state
            next_att = num_att - att_losses
            next_def = num_def - def_losses
            next_att_probs, next_def_probs = compute_battle_outcome_distribution(next_att, next_def, probs, memo)
            
            # Add this outcome's contribution to the final distribution
            # next_att_probs has length (next_att + 1), so we add it to the relevant slice
            final_att_probs[:next_att + 1] += prob_this_outcome * next_att_probs
            final_def_probs[:next_def + 1] += prob_this_outcome * next_def_probs
        
        # Store in memo
        memo[state] = (final_att_probs, final_def_probs)
        return final_att_probs, final_def_probs

    @render.plot
    def plot_probs():
        # logic that was here is now in update_chart_data
        chart_size = input.chart_size_slider()
        chart = prob_chart()

        ch = plt.imshow(chart[1:chart_size+1,1:chart_size+1], cmap='Reds',origin='lower',extent=(0.5,chart_size+0.5,0.5,chart_size+0.5))
        ticks = [i for i in range(1,chart_size+1)]
        plt.xticks(ticks)
        plt.yticks(ticks)
        plt.xlabel('Defending Army Size')
        plt.ylabel('Attacking Army Size')

        # Is there a way to refine this based on window size?
        annotate_plot = True
        if chart_size <= 11:
            font_size_str = 'small'
        elif chart_size <= 14:
            font_size_str = 'x-small'
        elif chart_size <= 18:
            font_size_str = 'xx-small'
        else:
            annotate_plot = False
        
        if annotate_plot:
            for i in range(1,chart_size+1):
                for j in range(1,chart_size+1):
                    p = chart[i,j]
                    if p >= 0.995:
                        p_str = '>.99'
                    elif p< 0.005:
                        p_str = '<.01'
                    else:
                        p_str = f'{p:.2f}'
                    if p>0.5:
                        c_str = 'white'
                    else:
                        c_str = 'black'
                    plt.annotate(p_str, xy=(j,i), ha='center', va='center', color=c_str, fontsize = font_size_str)
    
    @render.text
    def selected_probability():
        chart = prob_chart()
        if input.num_att_slider() == 1:
            attacker_str = 'attacker'
        else:
            attacker_str = 'attackers'
        if input.num_def_slider() == 1:
            defender_str = 'defender'
        else:
            defender_str = 'defenders'
        p = chart[input.num_att_slider(),input.num_def_slider()]
        if p>0.99995:
            p_str = '>99.99%'
        elif p<0.00005:
            p_str = '<0.01%'
        else:
            p_str = f'{p:.2%}'
        return f'Chance of {input.num_att_slider()} {attacker_str} defeating {input.num_def_slider()} {defender_str}: {p_str}'

    @render.plot
    def plot_dist():
        die_size = int(input.die_size_dist())
        probs = rgp.generate_probabilities(die=die_size, filename='', save_file=False)
        
        num_att = input.num_att_dist_slider()
        num_def = input.num_def_dist_slider()
        
        # Compute the full battle outcomes analytically
        final_att_probs, final_def_probs = compute_battle_outcome_distribution(num_att, num_def, probs)
        
        # Prepare data for attackers who won vs defenders who won
        att_won_idx = final_att_probs > 0
        def_won_idx = final_def_probs > 0
        
        att_remaining = np.arange(len(final_att_probs))[att_won_idx]
        att_probs = final_att_probs[att_won_idx]
        
        def_remaining = np.arange(len(final_def_probs))[def_won_idx]
        def_probs = final_def_probs[def_won_idx]
        
        # Create side-by-side bar charts
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Attacker victories (green)
        bars1 = ax1.bar(att_remaining, att_probs, color='#2ecc71', alpha=0.7, edgecolor='black', linewidth=1.5)
        for bar, val in zip(bars1, att_probs):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1%}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax1.set_xlabel('Attackers Remaining', fontsize=11)
        ax1.set_ylabel('Probability', fontsize=11)
        ax1.set_title('Attacker Victories', fontsize=12, fontweight='bold')
        ax1.set_xticks(att_remaining)
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_ylim(0, max(att_probs) * 1.15 if len(att_probs) > 0 else 1)
        
        # Defender victories (red)
        bars2 = ax2.bar(def_remaining, def_probs, color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=1.5)
        for bar, val in zip(bars2, def_probs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1%}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax2.set_xlabel('Defenders Remaining', fontsize=11)
        ax2.set_ylabel('Probability', fontsize=11)
        ax2.set_title('Defender Victories', fontsize=12, fontweight='bold')
        ax2.set_xticks(def_remaining)
        ax2.grid(axis='y', alpha=0.3)
        ax2.set_ylim(0, max(def_probs) * 1.15 if len(def_probs) > 0 else 1)
        
        plt.tight_layout()
    
    @render.text
    def dist_summary():
        die_size = int(input.die_size_dist())
        probs = rgp.generate_probabilities(die=die_size, filename='', save_file=False)
        
        num_att = input.num_att_dist_slider()
        num_def = input.num_def_dist_slider()
        
        final_att_probs, final_def_probs = compute_battle_outcome_distribution(num_att, num_def, probs)
        
        prob_attacker_wins = np.sum(final_att_probs)
        prob_defender_wins = np.sum(final_def_probs)
        
        # Expected remaining forces if they win
        att_remaining = np.arange(len(final_att_probs))
        def_remaining = np.arange(len(final_def_probs))
        
        exp_att_if_win = np.sum(att_remaining * final_att_probs) / prob_attacker_wins if prob_attacker_wins > 0 else 0
        exp_def_if_win = np.sum(def_remaining * final_def_probs) / prob_defender_wins if prob_defender_wins > 0 else 0
        
        summary_text = f'Starting with {num_att} attackers vs {num_def} defenders:\n'
        summary_text += f'Attacker victory: {prob_attacker_wins:.2%}'
        if prob_attacker_wins > 0:
            summary_text += f' (avg {exp_att_if_win:.1f} armies remaining)'
        summary_text += f'\nDefender victory: {prob_defender_wins:.2%}'
        if prob_defender_wins > 0:
            summary_text += f' (avg {exp_def_if_win:.1f} armies remaining)'
        
        return summary_text

app = App(app_ui, server)