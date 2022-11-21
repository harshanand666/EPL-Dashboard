from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from helper import graph_layout, text_out


#-------------- Comparison tab layout --------------_#



def text_stats(club,df):
    """ Function to output text stats"""

    num_seasons = len(df)
    best_finish = min(df.pos)
    best_season_latest = df[df.pos==best_finish]['season'].values
    wins = len(df[df.pos==1])
    top_4 = len(df[df.pos<=4])
    relegs = len(df[df.pos>=18])

    text_layout = html.Div(style={'backgroundColor': '#111111'}, children=[
        html.H1(f'{club}', style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50}),
        html.Br(),
        text_out("Number of seasons",num_seasons),
        text_out("Best finish",best_finish),
        text_out("Most recent best season",best_season_latest[-1]),
        text_out("Number of wins",wins),
        text_out("Number of top 4 finish",top_4),
        text_out("Number of relegations",relegs)
    ])
    
    return text_layout


def layout_comparison(df,f_club,s_club):
    ''' Main function to return all graphs '''

    f_df = df[df.team==f_club]              
    s_df = df[df.team==s_club]
    if len(f_df)<len(s_df):
        club_order = [s_club,f_club]
    else:
        club_order = [f_club,s_club]
    

    colors = ['red','cyan']
    pos_plots = []
    pts_plots = []
    win_plots = []
    goal_plots = []

    for i,club in enumerate(club_order):                   ## For each club, get data for each graph
        club_df = df[df.team==club]
        club_df.sort_values('start_year',inplace=True)
        
        ## Position per season

        x = club_df.season
        y = club_df.pos

        lineData = go.Scatter(
                        x=x,
                        y=y,
                        name=f"{club}",
                        mode="lines",
                        line = dict(color=colors[i], width=4)
        )
        pos_plots.append(lineData)

        layout_pos = graph_layout('Position per season','Season','Position',True)          
        pos_graph = dcc.Graph(figure = go.Figure(data = pos_plots,layout = layout_pos).update_layout({'hovermode':'x unified'},yaxis=dict(autorange='reversed')))


        ## Points per season

        y = club_df.Pts

        barData = go.Bar(
                        x=x,
                        y=y,
                        name=f"{club}",
                        marker_color=colors[i]
        )
        pts_plots.append(barData)

        layout_pos = graph_layout('Points per season','Season','Points',True)             
        pts_graph = dcc.Graph(figure = go.Figure(data = pts_plots,layout = layout_pos))


        ## Wins per season

        y = club_df.w

        barData = go.Bar(
                        x=x,
                        y=y,
                        name=f"{club}",
                        marker_color=colors[i]
        )
        win_plots.append(barData)

        layout_pos = graph_layout('Wins per season','Season','Wins',True)                   
        win_graph = dcc.Graph(figure = go.Figure(data = win_plots,layout = layout_pos))


        ## Goals per season

        y = club_df.gf

        barData = go.Bar(
                        x=x,
                        y=y,
                        name=f"{club}",
                        marker_color=colors[i]
        )
        goal_plots.append(barData)

        layout_pos = graph_layout('Goals per season','Season','Goals',True)                
        goals_graph = dcc.Graph(figure = go.Figure(data = goal_plots,layout = layout_pos))


    ## Return entire layout with text stas and graphs

    comparison_layout = html.Div(style={'backgroundColor': '#111111'},id='comparison_stats_div', children= [
        
        ## Div for text stats for both clubs

        html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','display':'flex'}, children=[

            html.Div(children=[text_stats(f_club,f_df)], style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'30%',
                    'justifyContent':'center','paddingLeft':'10%'}),
            html.Div(children=[text_stats(s_club,s_df)], style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'30%',
                    'justifyContent':'center','paddingLeft':'20%'})

        ]),

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
        goals_graph
    ])

    return comparison_layout