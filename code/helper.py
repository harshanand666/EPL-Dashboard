import plotly.graph_objs as go
from dash import html

#-----------------Helper functions-----------------#


def graph_layout(title,x_title,y_title,legend=False):
    """ Returns the layout for all graphs"""

    return go.Layout(
            title=dict(text=title, font=dict(size=30,color='white')),
            xaxis={'title':x_title,
                    'titlefont' : dict(
                            family = 'Arial, sans-serif',
                            size = 20,
                            color = 'white'
                            ),
                    'zeroline':True,
                    'tickfont' : dict(
                            size = 16,
                            color='white'
                            ),
                    'showgrid':False,
                    'type':'category',
                    'zerolinecolor':'white'

                },
            yaxis = {'title':y_title,
                    'titlefont' : dict(
                            family = 'Arial, sans-serif',
                            size = 20,
                            color = 'white'
                            ),
                    'zeroline':True,
                    'tickfont' : dict(
                            size = 16,
                            color='white'
                            ),
                    'showgrid':False
                    },
            paper_bgcolor = '#111111',
            plot_bgcolor = '#111111',
            bargap=0.5,
            showlegend=legend,
            legend=dict(
                font=dict(
                    size=18,
                    color="white"
                )
            ),
            hoverlabel=dict(
                bgcolor="grey",
                font_size=26,
                font_color='black'
            )
        )


def get_tab_styles():
    ''' Returns styles for tabs '''

    tabs_styles = {
    'height': '88px'
    }

    tab_style = {
        'borderBottom': '1px solid #000000',
        'padding': '6px',
        'fontWeight': 'bold',
        'backgroundColor': '#5B5858',
        'fontSize':30
    }

    tab_selected_style = {
        'borderTop': '1px solid #000000',
        'borderBottom': '1px solid #000000',
        'backgroundColor': '#5DE9F7',
        'color': 'black',
        'fontWeight': 'bold',
        'padding': '6px',
        'fontSize':30
    }

    return tabs_styles,tab_style,tab_selected_style



def text_out(name,var):
    ''' Helper function to output text in specific format '''
    return html.H1(f'{name} : {var} ', style = {'textAlign':'center','color':'white','white-space':'pre','fontSize':35})
    
