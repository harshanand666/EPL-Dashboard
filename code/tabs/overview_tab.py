from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from helper import graph_layout

#---------------------- Overview Stats Tab Layout -----------------------#

def layout_overview(df):
    ''' Main function to return graphs '''

    # Getting data for the required graphs

    clubs = df.team.unique()
    win_df = pd.DataFrame()
    top_df = pd.DataFrame()
    rel_df = pd.DataFrame()

    for club in clubs:
        wins = len(df[(df.team==club)&(df.pos==1)])                                 ## Win data
        if wins>0:
            win_df = win_df.append({'club':club,'wins':wins}, ignore_index=True)
        
        tops = len(df[(df.team==club)&(df.pos<=4)])                                 ## Top 4 data
        if tops>0:
            top_df = top_df.append({'club':club,'tops':tops}, ignore_index=True)

        rels = len(df[(df.team==club)&(df.pos>=18)])                                ## Relegation data
        if rels>0:
            rel_df = rel_df.append({'club':club,'rels':rels}, ignore_index=True)

    rel_df.sort_values(by='rels',inplace=True,ascending=False)
    top_df.sort_values(by='tops',inplace=True,ascending=False)
    win_df.sort_values(by='wins',inplace=True,ascending=False)

    x = win_df.club

    ## Graph for wins

    y = win_df.wins
    lineData_wins = go.Bar(
        x = x,
        y = y,
        marker_color = 'cyan'
    )
    layout_wins = graph_layout('Total trophies','Club','Trophies')
    wins_graph = dcc.Graph(figure = go.Figure(data = lineData_wins,layout = layout_wins))


    # Graph for top 4

    y = top_df.tops
    lineData_top_4 = go.Bar(
        x = x,
        y = y,
        marker_color = 'cyan'
    )
    layout_top_4 = graph_layout('Total UCL Qualifications','Club','Qualifications')                                 
    top_4_graph = dcc.Graph(figure = go.Figure(data = lineData_top_4,layout = layout_top_4))


    # Graph for relegations

    y = rel_df.rels
    lineData_rel = go.Bar(
        x = x,
        y = y,
        marker_color = 'cyan'
    )
    layout_rel = graph_layout('Total Relegations','Club','Relegations')                         
    rel_graph = dcc.Graph(figure = go.Figure(data = lineData_rel,layout = layout_rel))


    # Top 6 teams line chart

    scatter_plots = []

    top_6 = ['Manchester United','Manchester City','Liverpool','Chelsea','Arsenal','Tottenham Hotspur']

    for club in top_6:
        club_df = df[df.team==club]
        club_df.sort_values('start_year',inplace=True)

        x = club_df.season
        y = club_df.pos

        lineData = go.Scatter(
                                x=x,
                                y=y,
                                name=f"{club}",
                                mode="lines",
                                line = dict(width=4),
        )
        scatter_plots.append(lineData)

    layout_pos = graph_layout('Top 6 standings','Season','Position',True)
    pos_graph = dcc.Graph(figure = go.Figure(data = scatter_plots,layout = layout_pos).update_layout({'hovermode':'x unified'},yaxis=dict(autorange='reversed')))


    ## Returning the complete layout with all graphs

    complete_layout = html.Div(style={'backgroundColor': '#111111'}, children= [
        wins_graph,
        html.Br(),
        html.Br(),
        top_4_graph,
        html.Br(),
        html.Br(),
        rel_graph,
        html.Br(),
        html.Br(),
        pos_graph,

    ])

    return complete_layout






