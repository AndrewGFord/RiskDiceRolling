# Shiny app for Risk board game probability data
from shiny import App, Inputs, Outputs, Session, reactive, render, ui

import numpy as np
import matplotlib.pyplot as plt
import RiskProbabilitiesLib as rpl
import RiskGenerateProbs as rgp

die_size = 6 # Number of sides on the die
probs = rgp.generate_probabilities(die=die_size, filename='', save_file=False)
# Move these to server logic later to allow users to change die size

app_ui = ui.page_fluid(
    ui.layout_columns(
        ui.card(
            ui.h3('Probability Grid'),
            # TODO: Adjust relative sizes using CSS
            ui.layout_columns(
                ui.input_slider('chart_size_slider', 'Chart Size', min=1, max=30, value=10),
                ui.input_numeric('chart_size_numeric', label = 'Chart Size', value=10, min=1, max=30, step=1),
            ),
            ui.input_selectize('die_size', 'Number of Faces on Die', choices=[4, 6, 8, 12, 20], selected=6),
            ui.output_plot('plot_probs'),
        ),
        ui.card(
            ui.h3('Single Battle Probability'),
            # TODO: Adjust relative sizes using CSS
            ui.layout_columns(
                ui.input_slider('num_att_slider', 'Number of Attackers', min=1, max=30, value=1),
                ui.input_numeric('num_att_numeric', label = 'Number of Attackers', value=1, min=1, max=30, step=1),
            ),
            ui.layout_columns(
                ui.input_slider('num_def_slider', 'Number of Defenders', min=1, max=30, value=1),
                ui.input_numeric('num_def_numeric', label = 'Number of Defenders', value=1, min=1, max=30, step=1),
            ),
            ui.output_text('selected_probability'),
        ),
    )
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

app = App(app_ui, server)