from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from helper import graph_layout, text_out


#--------------- Club stats tab layout --------------#



def text_stats(df):
    ''' Function for text stats '''

    num_seasons = len(df)
    best_finish = min(df.pos)
    best_season_latest = df[df.pos==best_finish]['season'].values
    wins = len(df[df.pos==1])
    top_4 = len(df[df.pos<=4])
    relegs = len(df[df.pos>=18])

    text_layout = html.Div(style={'backgroundColor': '#111111'}, children=[

        text_out("Number of seasons",num_seasons),
        text_out("Best finish",best_finish),
        text_out("Most recent best season",best_season_latest[-1]),
        text_out("Number of wins",wins),
        text_out("Number of top 4 finish",top_4),
        text_out("Number of relegations",relegs)
    ])
    
    return text_layout



def layout_club_stats(df,club):
    ''' Main function to return all graphs '''

    if club==None:
        return html.Div(children=[],style={'backgroundColor':'#111111','id':'club_stats_div'})      ## No club chosen

    club_df = df[df.team==club]

    ## Position per season

    posData = go.Scatter(
        x=club_df.season,
        y=club_df.pos,
        name="Season vs Position",
        mode="lines",
        line = dict(color='cyan', width=4)
    )
    
    layout_pos = graph_layout('Position per season','Season','Position')
    pos_graph = dcc.Graph(figure = go.Figure(data = posData,layout = layout_pos).update_layout(yaxis=dict(autorange='reversed')))


    ## Points per season

    ptsData = go.Scatter(
        x=club_df.season,
        y=club_df.Pts,
        name="Season vs Points",
        mode="lines",
        line = dict(color='cyan', width=4)
    )
    

    layout_pts = graph_layout('Points per season','Season','Points')
    pts_graph = dcc.Graph(figure = go.Figure(data = ptsData,layout = layout_pts))


    ## Wins per season

    winData = go.Scatter(
        x=club_df.season,
        y=club_df.w,
        name="Season vs Wins",
        mode="lines",
        line = dict(color='cyan', width=4)
    )

    win_barData = go.Bar(
        x=club_df.season,
        y=club_df.w,
        name="Season vs Wins Bar",
        marker_color='pink',

    )

    layout_win = graph_layout('Wins per season','Season','Wins')
    win_graph = dcc.Graph(figure = go.Figure(data = [winData,win_barData],layout = layout_win))

    # Goals per seaon

    goalData = go.Scatter(
        x=club_df.season,
        y=club_df.gf,
        name="Season vs Goals",
        mode="lines",
        line = dict(color='cyan', width=4)
    )

    goal_barData = go.Bar(
        x=club_df.season,
        y=club_df.gf,
        name="Season vs Goals Bar",
        marker_color='pink',

    )

    layout_goals = graph_layout('Goals per season','Season','Goals')
    goal_graph = dcc.Graph(figure = go.Figure(data = [goalData,goal_barData],layout = layout_goals))

    # GD per seaon

    gdData = go.Scatter(
        x=club_df.season,
        y=club_df.gd,
        name="Season vs GD",
        mode="lines",
        line = dict(color='cyan', width=4)
    )

    gd_barData = go.Bar(
        x=club_df.season,
        y=club_df.gd,
        name="Season vs GD Bar",
        marker_color='pink',

    )

    layout_gd = graph_layout('GD per season','Season','GD')
    gd_graph = dcc.Graph(figure = go.Figure(data = [gdData,gd_barData],layout = layout_gd))

    
    # Return entire layout with text and graphs

    club_layout = html.Div(style={'backgroundColor': '#111111'},id='club_stats_div', children= [
        html.H1(f'{club}', style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50}),
        html.Br(),
        text_stats(club_df),
        html.Br(),
        html.Br(),
        html.Br(),
        pos_graph,
        html.Br(),
        html.Br(),
        pts_graph,
        html.Br(),
        html.Br(),
        win_graph,
        html.Br(),
        html.Br(),
        goal_graph,
        html.Br(),
        html.Br(),
        gd_graph,

    ])

    return club_layout

