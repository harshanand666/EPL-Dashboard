import base64
import io
import warnings
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
from flask import Flask

from tabs.overview_tab import layout_overview
from tabs.club_tab import layout_club_stats
from tabs.comparison_tab import layout_comparison
from helper import get_tab_styles


warnings.filterwarnings("ignore")

server = Flask(__name__)

app = dash.Dash(f'EPL Dashboard',server=server)

## Styles for tabs

tabs_styles,tab_style,tab_selected_style = get_tab_styles()



#----------------------- Initial app layout ---------------------------#

app.layout = html.Div(style={'backgroundColor': '#111111'}, children=[

        ## Heading

        html.Br(),
        html.H1(f'English Premier League 2000-2022', style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':50}),
        html.Br(),

        ## Upload file div

        html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'20%',
        'justifyContent':'center','paddingLeft':'40%'}, children=[

             html.Label('Upload CSV file below',
             style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':40, 'margin': '20px'}),
             
             html.Br(),
             html.Br(),

             dcc.Upload(['Drag and Drop or ',
                html.A('Select a File')],id='upload-data-summary',
                style={
                    'height': '100px',
                    'lineHeight': '100px',
                    'borderWidth': '5px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'backgroundColor':'grey',
                    'color':'black',
                    'fontSize':30,
                    },
                multiple=False
                ),

        ]),        

        
        html.Br(),
        html.Br(),
        html.Br(),

        # Outer Div which contains 2 inner divs each cotaining a label and dropdown for start/end season

        html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','display':'flex'}, children=[

            html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'15%',
            'justifyContent':'center','paddingLeft':'17.5%'}, children=[

                html.Label('Select starting season',
                style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':40, 'margin': '20px'}),
                
                html.Br(),
                html.Br(),

                dcc.Dropdown(
                    id = 'dropdown_start',
                    options = [],              
                    multi=False,
                    searchable=False,
                    clearable=True,
                    optionHeight=70,
                    style = {
                    'height': '50px',
                    'borderWidth': '2px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'borderColor': 'grey',
                    'backgroundColor':'white',
                    'color':'black',
                    'fontSize':30,
                    },

                )

            ]),

            # Dropdown for end season

            html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'15%',
            'justifyContent':'center','paddingLeft':'35%'}, children=[

                html.Label('Select second model',
                style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':40, 'margin': '20px'}),
                
                html.Br(),
                html.Br(),

                dcc.Dropdown(
                    id = 'dropdown_end',
                    options = [],                  
                    multi=False,
                    searchable=False,
                    clearable=True,
                    optionHeight=70,
                    style = {
                    'height': '50px',
                    'borderWidth': '2px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'borderColor': 'grey',
                    'backgroundColor':'white',
                    'color':'black',
                    'fontSize':30,
                    },

                )

            ])
        
        ]),

        html.Br(),
        html.Br(),
        html.Br(),

        # Submit Button for generating graphs

        html.Div(
                    html.Button('Generate Graphs', 
                        id='submit', 
                        n_clicks=0, 
                        style = {'fontSize':30,'height':'50px','width':'300px'}),
                    style = {'display':'flex','justifyContent':'center'}
                ),
        
        html.Br(),
        html.Br(),

        # Container for output

        html.Div(id='output-data-upload',style = {
            'color':'black','height': '100vh'}),
        
    ])



#------------Preprocessing-------#

def preprocess_data(df):
    ''' Function to parse the uploaded csv and return dataframe '''

    # Rename columns

    df = df.rename(columns = {'Season':'season', 'Pos':'pos', 'Team':'team','Pld':'played',
    'W':'w', 'D':'d', 'L':'l', 'GF':'gf', 'GA':'ga', 'GD':'gd'})

    ## creating a datetime object column for easy sorting/filtering

    df['start_year'] = df['season'].apply(lambda x: x.split('-')[0])
    df['end_year'] = df['season'].apply(lambda x: "20"+x.split('-')[1])
    
    df['start_year'] = df['start_year'].astype('datetime64[ns]').dt.year
    df['end_year'] = df['end_year'].astype('datetime64[ns]').dt.year

    return df



def parse_contents(data):
    ''' Function that takes uploaded data, preprocesses it and returns the df '''
    
    _ , content_string = data.split(',')

    decoded = base64.b64decode(content_string)
    try:
 
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        df = preprocess_data(df)

    except Exception as e:
        print(f'Error with format {e}')
        return pd.DataFrame()

    return df



#----------------------- Main function to return entire output --------------------#


def generate_output(main_df, start_season, end_season):
    ''' Function that generates all output based on selected options '''

    start_year = int(start_season.split('-')[0])
    end_year = int(end_season.split('-')[0])

    chosen_df = main_df[(main_df.start_year>=start_year) & (main_df.start_year<=end_year)]
    
    #If no data in chosen dates
    if len(chosen_df)==0:
        return html.Div("NO DATA FOR CHOSEN DATES",style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50})

    clubs = list(chosen_df.team.unique())

    #-------------------- Layout of output --------------------#

    
    output_data = html.Div(style={'backgroundColor': '#111111'}, children=[

        html.Br(),
        html.Br(),

        # MAKING TABS 
        
        dcc.Tabs([

            # Overview Tab

            dcc.Tab(label='Overview Stats',style = tab_style, selected_style = tab_selected_style,children=[

                html.Br(),
                html.Br(),
                layout_overview(chosen_df)

                
            ]),

            # Clubwise Stats

            dcc.Tab(label = 'Club Stats', style = tab_style, selected_style = tab_selected_style, children = [

                html.Br(),
                html.Br(),

                # Dropdown to select club
                html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'15%',
                'justifyContent':'center','paddingLeft':'42.5%'}, children=[

                    html.Label('Select Club',
                    style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':40, 'margin': '20px'}),
                    
                    html.Br(),
                    html.Br(),

                    dcc.Dropdown(
                        id = 'dropdown_club',
                        options = [{'label': i, 'value': i} for i in sorted(clubs)],              # populate options from all clubs
                        multi=False,
                        searchable=True,
                        clearable=True,
                        optionHeight=70,
                        style = {
                        'height': '50px',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'borderColor': 'grey',
                        'backgroundColor':'white',
                        'color':'black',
                        'fontSize':30,
                        },
                    )

                ]),

                html.Br(),
                html.Br(),
                layout_club_stats(chosen_df,clubs[0])
                

            ]),

            # Comparison tab

            dcc.Tab(label = 'Comparison', style = tab_style, selected_style = tab_selected_style, children =[
                
                html.Br(),
                html.Br(),

                # Outer Div which contains 2 inner divs each cotaining a label and dropdown for both clubs

                html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','display':'flex'}, children=[

                    html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'15%',
                    'justifyContent':'center','paddingLeft':'17.5%'}, children=[

                        html.Label('Select first club',
                        style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':40, 'margin': '20px'}),
                        
                        html.Br(),
                        html.Br(),

                        # Dropdown for first club
                        dcc.Dropdown(
                            id = 'dropdown_first_club',
                            options = [{'label': i, 'value': i} for i in sorted(clubs)],              # populate options from all clubs
                            multi=False,
                            searchable=False,
                            clearable=True,
                            optionHeight=70,
                            style = {
                            'height': '50px',
                            'borderWidth': '2px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'borderColor': 'grey',
                            'backgroundColor':'white',
                            'color':'black',
                            'fontSize':30,
                            },

                        )

                    ]),

                    # Div for second club

                    html.Div(style={'backgroundColor': '#111111','horizontalAlign':'center','textAlign':'center','width':'15%',
                    'justifyContent':'center','paddingLeft':'35%'}, children=[

                        html.Label('Select second club',
                        style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':40, 'margin': '20px'}),
                        
                        html.Br(),
                        html.Br(),

                        # Dropdown for second club

                        dcc.Dropdown(
                            id = 'dropdown_second_club',
                            options = [{'label': i, 'value': i} for i in sorted(clubs)],                  # populate options from all clubs
                            multi=False,
                            searchable=False,
                            clearable=True,
                            optionHeight=70,
                            style = {
                            'height': '50px',
                            'borderWidth': '2px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'borderColor': 'grey',
                            'backgroundColor':'white',
                            'color':'black',
                            'fontSize':30,
                            },
                        )
                    ])
                ]),

                html.Br(),
                html.Br(),
                layout_comparison(chosen_df,clubs[0],clubs[1])
            ])
        ])
    ])

    return output_data


#------------------------ Callback functions ---------------------#


# Callback for updating dropdown for seasons

@app.callback([Output('dropdown_start','options'),
            Output('dropdown_start','value'),
            Output('dropdown_end','options'),
            Output('dropdown_end','value')],
            Input('upload-data-summary', 'contents'))
def update_dropdowns(contents):
    df = parse_contents(contents)
    if not df.empty:                                                ## If uploaded data is valid
        sorted_df = df.sort_values('start_year')
        start_season = list(sorted_df.season)[0]
        end_season = list(sorted_df.season)[-1]
        all_seasons = list(sorted_df.season.unique())
        return all_seasons,start_season,all_seasons,end_season      ## Return all seasons as options, and default values



# Callback for generating output on button press

@app.callback(Output('output-data-upload', 'children'),
            Input('submit','n_clicks'),
            [State('upload-data-summary', 'contents'),
            State('dropdown_start','value'),
            State('dropdown_end','value')]
            )
def update_output(clicks,contents,start_season,end_season):

    # Check what triggered render
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'

    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    #If submit button clicked, only then call function to render
    if button_id == 'submit':
        if contents is not None:                                        ## If something uploaded
            
            df = parse_contents(contents)
            if not df.empty:                                            ## If df is valid
                return generate_output(df,start_season,end_season)
            
            else:                                                       ## Otherwise wrong file uploaded
                return html.Div("WRONG FILE UPLOADED",style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50})



# Callback for club stats tab

@app.callback(Output('club_stats_div', 'children'),
            Input('dropdown_club','value'),
            [State('dropdown_start','value'),
            State('dropdown_end','value'),
            State('upload-data-summary', 'contents')]
            )
def update_clubwise(club,start_season,end_season,contents):

    if contents is not None and club is not None:               ## If data uploaded and club chosen
        df = parse_contents(contents)
        if not df.empty:
            start_year = int(start_season.split('-')[0])
            end_year = int(end_season.split('-')[0])            

            chosen_df = df[(df.start_year>=start_year) & (df.start_year<=end_year)]

            if len(chosen_df)==0:
                return html.Div("NO DATA FOR CHOSEN DATES",style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50})
            
            return layout_club_stats(chosen_df,club)
            
        else:
            return html.Div("WRONG FILE UPLOADED",style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50})


# Callback for comparison tab

@app.callback(Output('comparison_stats_div', 'children'),
            [Input('dropdown_first_club','value'),
            Input('dropdown_second_club','value')],
            [State('dropdown_start','value'),
            State('dropdown_end','value'),
            State('upload-data-summary', 'contents')]
            )
def update_clubwise(first_club,second_club,start_season,end_season,contents):

    if contents is not None and first_club is not None and second_club is not None:     ## If data uploaded and both clubs chosen
        df = parse_contents(contents)
        if not df.empty:
            start_year = int(start_season.split('-')[0])
            end_year = int(end_season.split('-')[0])            

            chosen_df = df[(df.start_year>=start_year) & (df.start_year<=end_year)]
            
            if len(chosen_df)==0:
                return html.Div("NO DATA FOR CHOSEN DATES",style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50})
            
            return layout_comparison(chosen_df,first_club,second_club)
            
        else:
            return html.Div("WRONG FILE UPLOADED",style = {'textAlign':'center','color':'cyan','white-space':'pre','fontSize':50})


## Run the app on port 8080 in debug mode

server.run(debug = True, port=8080)
