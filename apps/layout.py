from dash import dcc, html
import datetime as dt
from dash import dash_table
#import dash_bootstrap_components as dbc


def create_layout():
    layout = html.Div([
        dcc.Location(id='url', refresh=False),

        html.Div([
            html.Div([                
                html.Img(
                    src="https://www.sreality.cz/img/logo-sreality.svg",
                    style={
                        'height': '40px',
                        'margin-right': '15px',
                        'vertical-align': 'middle'
                    }
                ),
                dcc.Link('Intro', href='/intro', className='nav-link'),
                html.Span(" | ", className='separator'),
                dcc.Link('People', href='/people', className='nav-link'),
                html.Span(" | ", className='separator'),
                dcc.Link('Medals', href='/medals', className='nav-link'),
                html.Span(" | ", className='separator'),
                dcc.Link('Clubs', href='/clubs', className='nav-link'),
                html.Span(" | ", className='separator'),
                dcc.Link('Duels', href='/duels', className='nav-link'),
                html.Span(" | ", className='separator'),
                dcc.Link('Predictions', href='/predictions', className='nav-link'),  
                html.Span(" | ", className='separator'),
                dcc.Link('Tournaments', href='/tournaments', className='nav-link'),  
            ], style={
                'display': 'flex',
                'align-items': 'center',
                'background-color': '#000000',  # Dark blue background
                'padding': '10px 20px'
            }),
        ]),

        html.Div(id='page-content')
    ])

    return layout

def create_intro_layout():
    layout = html.Div([
        
        html.H1("Intro"),
        
        html.H2("Here I want "),
        
        html.Div([
            html.Button("Get Length of tournaments", 
                        id='refresh-data-button', 
                        n_clicks=0,
                        style={
                            'padding': '10px 20px',       
                            'fontSize': '18px',           
                            'backgroundColor': '#007BFF', 
                            'color': 'white',             
                            'border': 'none',             
                            'borderRadius': '8px',        
                            'cursor': 'pointer',          
                            'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)',  
                            'transition': 'background-color 0.3s ease' 
                        },
            )],
        style={'margin-top': '10px'}
        ),
        
        html.Div(id='output-number_tournaments', 
                style={'margin-top': '20px'}),
        
    ])
    return layout

def create_people_layout():
    layout = html.Div([
        
        html.H1("People"),
        
        html.H2("Here I want "),
    ])
    return layout

def create_medals_layout():
    layout = html.Div([
        
        html.H1("Medals"),
        
        html.H2("Here I want "),
    ])
    return layout

def create_clubs_layout():
    layout = html.Div([
        
        html.H1("Clubs"),
        
        html.H2("Here I want "),
    ])
    return layout

def create_duels_layout():
    layout = html.Div([
        
        html.H1("Duels"),
        
        html.H2("Here I want "),
    ])
    return layout

def create_predictions_layout():
    layout = html.Div([
        
        html.H1("Predictions"),
        
        html.H2("Here I want "),
    ])
    return layout

def create_tournaments_layout():
    layout = html.Div([
        
        html.H1("Tournaments"),
        
        html.H2("Here I want "),
    ])
    return layout