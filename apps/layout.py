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
                    src="https://s3.eu-west-1.amazonaws.com/assets-test.designeo.cz/css-cms/dev/2023-06-08/36ef7c20-b52b-4adb-a83e-ecea3b121072_20230608191442.png",
                    style={
                        'height': '40px',
                        'margin-right': '15px',
                        'vertical-align': 'middle'
                    }
                ),
                dcc.Link('Intro', href='/intro', className='nav-link'),
                dcc.Link('People', href='/people', className='nav-link'),
                dcc.Link('Medals', href='/medals', className='nav-link'),
                dcc.Link('Clubs', href='/clubs', className='nav-link'),
                dcc.Link('Duels', href='/duels', className='nav-link'),
                dcc.Link('Predictions', href='/predictions', className='nav-link'),  
                dcc.Link('Tournaments', href='/tournaments', className='nav-link'),  
            ], style={
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'background-color': '#001f3f',  # Dark blue background
                    'padding': '10px 20px',
                    'position': 'fixed',  # Fix navbar at the top
                    'top': '0',
                    'width': '100%',
                    'border-bottom': '2px solid #ffdc00',  # Yellow bottom border for contrast
                    'font-family': 'Arial, sans-serif',  # Font style
                    'z-index': '1000',  # Ensure navbar is above other elements
                }),
        ], style={'margin-bottom': '60px'}), 

        html.Div(id='page-content')
    ])

    return layout

def create_intro_layout():
    layout = html.Div([
        
        html.H1("Intro"),
        
        html.H2("Here I want "),
        
    ])
    return layout

def create_people_layout():
    layout = html.Div([
        
        html.H1("People"),
        
        html.H2("Here I want "),
        
        html.Div([
            html.Button("Get Number of Fencers", 
                        id='refresh-fencers-button', 
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
        
        html.Div(id='output-number_fencers', 
                style={'margin-top': '20px'}),
        
        html.Div([      
            dash_table.DataTable(
            id='fencers-table',
            columns=[
                {"name": "Name", "id": "name_url", "presentation":"markdown"},
                {"name": "Club ID", "id": "club_id"},
                {"name": "Country", "id": "country"},
                {"name": "Sex", "id": "sex"},
                {"name": "Birthdate", "id": "birthdate"},
                {"name": "Birthyear", "id": "birthyear"},
                ],
            
            style_table={
            'maxWidth': '800px',
            'margin': 'auto',
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'overflowY': 'auto'
            },
            style_header={
                'backgroundColor': '#f4f4f4',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'borderBottom': '2px solid #e5e5e5',
                'color': '#333'
            },
            style_cell={
                'padding': '10px',
                'textAlign': 'center',
                'border': '1px solid #e5e5e5',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
            },
            style_data={
                'backgroundColor': '#ffffff',
                'color': '#000',
            },
            page_size=20,
            sort_action='native',
            style_as_list_view=True,
            #filter_action='native',
            export_format='csv'
            )       
        ]),
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
        
        html.Div([
            html.Button("Get Number of Clubs", 
                        id='refresh-clubs-button', 
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
        
        html.Div(id='output-number_clubs', 
                style={'margin-top': '20px'}),
        
        html.Div([      
            dash_table.DataTable(
            id='clubs-table',
            columns=[
                {"name": "Name", "id": "name_url", "presentation":"markdown"},
                {"name": "City", "id": "city"},
                ],
            
            style_table={
            'maxWidth': '800px',
            'margin': 'auto',
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'overflowY': 'auto'
            },
            style_header={
                'backgroundColor': '#f4f4f4',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'borderBottom': '2px solid #e5e5e5',
                'color': '#333'
            },
            style_cell={
                'padding': '10px',
                'textAlign': 'center',
                'border': '1px solid #e5e5e5',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
            },
            style_data={
                'backgroundColor': '#ffffff',
                'color': '#000',
            },
            page_size=20,
            sort_action='native',
            style_as_list_view=True,
            #filter_action='native',
            export_format='csv'
            )       
        ]),
    ])
    return layout

def create_duels_layout():
    layout = html.Div([
        
        html.H1("Duels"),
        
        html.H2("Here I want "),
        
        html.Div([
            html.Button("Get Number of Duels", 
                        id='refresh-duels-button', 
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
        
        html.Div(id='output-number_duels', 
                style={'margin-top': '20px'}),
        
        html.Div([      
            dash_table.DataTable(
            id='duels-table',
            columns=[
                {"name": "Tournament Id", "id": "tournament_id"},
                {"name": "Fencer Id", "id": "fencer_id_url", "presentation":"markdown"},
                {"name": "Opponent Id", "id": "opponent_id"},
                {"name": "Fight LVL", "id": "fight_lvl"},
                {"name": "Result", "id": "result"},
                {"name": "TS", "id": "ts"},
                {"name": "TR", "id": "tr"},
                ],
            
            style_table={
            'maxWidth': '800px',
            'margin': 'auto',
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'overflowY': 'auto'
            },
            style_header={
                'backgroundColor': '#f4f4f4',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'borderBottom': '2px solid #e5e5e5',
                'color': '#333'
            },
            style_cell={
                'padding': '10px',
                'textAlign': 'center',
                'border': '1px solid #e5e5e5',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
            },
            style_data={
                'backgroundColor': '#ffffff',
                'color': '#000',
            },
            page_size=20,
            sort_action='native',
            style_as_list_view=True,
            #filter_action='native',
            export_format='csv'
            )       
        ]),
    ])
    
    return layout

def create_predictions_layout():
    layout = html.Div([
        
        html.H1("Predictions"),
        
        html.H2("Here I want "),
        
        html.Div([
            html.Button("Get Number of tournament results", 
                        id='refresh-tournaments_results-button', 
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
        
        html.Div(id='output-number_tournaments_results', 
                style={'margin-top': '20px'}),
        
        html.Div([      
            dash_table.DataTable(
            id='tournaments_results-table',
            columns=[
                {"name": "Tournament Id", "id": "tournament_id_url", "presentation":"markdown"},
                {"name": "Fencer Id", "id": "fencer_id_url", "presentation":"markdown"},
                {"name": "Status", "id": "status"},
                {"name": "Type", "id": "first_rank"},
                {"name": "Final rank", "id": "final_rank"},
                {"name": "Percentile", "id": "percentile"},
                {"name": "Victories", "id": "victories"},
                {"name": "Victories perc", "id": "victories_perc"},
                {"name": "TS", "id": "ts"},
                {"name": "TR", "id": "tr"},
                {"name": "Score Index", "id": "score_index"},
                ],
            
            style_table={
            'maxWidth': '800px',
            'margin': 'auto',
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'overflowY': 'auto'
            },
            style_header={
                'backgroundColor': '#f4f4f4',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'borderBottom': '2px solid #e5e5e5',
                'color': '#333'
            },
            style_cell={
                'padding': '10px',
                'textAlign': 'center',
                'border': '1px solid #e5e5e5',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
            },
            style_data={
                'backgroundColor': '#ffffff',
                'color': '#000',
            },
            page_size=20,
            sort_action='native',
            style_as_list_view=True,
            #filter_action='native',
            export_format='csv'
            )       
        ]),
    ])
    
    return layout

def create_tournaments_layout():
    layout = html.Div([
        
        html.H1("Tournaments"),
        
        html.H2("Here I want "),
        
        html.Div([
            html.Button("Get Number of tournaments", 
                        id='refresh-tournaments-button', 
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
        
        html.Div([      
            dash_table.DataTable(
            id='tournaments-table',
            columns=[
                {"name": "Name", "id": "name_url", "presentation":"markdown"},
                {"name": "Date", "id": "date"},
                {"name": "Type", "id": "type"},
                ],
            
            style_table={
            'maxWidth': '800px',
            'margin': 'auto',
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'overflowX': 'auto',
            'overflowY': 'auto'
            },
            style_header={
                'backgroundColor': '#f4f4f4',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'borderBottom': '2px solid #e5e5e5',
                'color': '#333'
            },
            style_cell={
                'padding': '10px',
                'textAlign': 'center',
                'border': '1px solid #e5e5e5',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
            },
            style_data={
                'backgroundColor': '#ffffff',
                'color': '#000',
            },
            page_size=20,
            sort_action='native',
            style_as_list_view=True,
            #filter_action='native',
            export_format='csv'
            )       
        ]),
    ])
    
    return layout