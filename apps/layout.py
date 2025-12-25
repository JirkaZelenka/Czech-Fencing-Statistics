from dash import dcc, html, Input, Output, State
import datetime as dt
from dash import dash_table
#import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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
                dcc.Link('Intro', href='/intro', style={'color': 'white', 'fontSize': '16px'}),
                html.Span(" | ", className='separator'),
                dcc.Link('People', href='/people', className='nav-link',  style={'color': 'white', 'fontSize': '22px', 'fontWeight': 'bold'}),
                html.Span(" | ", className='separator'),
                dcc.Link('Medals', href='/medals', className='nav-link', style={'color': 'white', 'fontSize': '16px'}),
                html.Span(" | ", className='separator'),
                dcc.Link('Clubs', href='/clubs', className='nav-link', style={'color': 'white', 'fontSize': '22px', 'fontWeight': 'bold'}),
                html.Span(" | ", className='separator'),
                dcc.Link('Eliminations', href='/eliminations', className='nav-link', style={'color': 'white', 'fontSize': '16px'}),
                html.Span(" | ", className='separator'),
                dcc.Link('Tournament Results', href='/tournament_results', className='nav-link', style={'color': 'white', 'fontSize': '22px', 'fontWeight': 'bold'}),
                html.Span(" | ", className='separator'),
                dcc.Link('Tournaments', href='/tournaments', className='nav-link', style={'color': 'white', 'fontSize': '22px', 'fontWeight': 'bold'}),
                html.Span(" | ", className='separator'),
                dcc.Link('Duels', href='/duels', className='nav-link', style={'color': 'white', 'fontSize': '22px', 'fontWeight': 'bold'}),
                html.Span(" | ", className='separator'),
                dcc.Link('Personal Stats', href='/personal_stats', className='nav-link', style={'color': 'white', 'fontSize': '16px'}),
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
        
        html.H1("Fencers"),
        
        html.H2("Here I want "),
        
        html.H2("Filters"),
        html.Div([
            html.Div([
                html.Label("Fencers"),
                dcc.Dropdown(
                    id="filter-fencers-name",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select fencers..."
                ),
            html.Label("Clubs"),
                dcc.Dropdown(
                    id="filter-fencers-club",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select clubs..."
                ),
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("Country"),
                dcc.Dropdown(
                    id="filter-fencers-country",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select countries..."
                ),
                html.Label("Gender"),
                dcc.Dropdown(
                    id="filter-fencers-gender",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select genders..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("Birthyear"),
                dcc.Dropdown(
                    id="filter-fencers-birthyear",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select birthyears..."
                )
                
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),
            
            html.Div([
                html.Button(
                    "Reset Filters",
                    id="reset-fencers-filters-button",
                    n_clicks=0,
                    style={
                        'padding': '10px 20px',
                        'fontSize': '16px',
                        'backgroundColor': '#6c757d',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'marginLeft': '10px',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)'
                    }
                ),
                
                html.H4("Number of Fencers", style={"margin-bottom": "5px", "color": "#001f3f"}),
                
                html.Div(
                    id='output-fencers-filtered-number',
                    style={
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "color": "#007BFF",
                    "backgroundColor": "#f4f4f4",
                    "borderRadius": "12px",
                    "padding": "20px 20px",
                    "boxShadow": "0px 4px 16px rgba(0,0,0,0.10)",
                    "textAlign": "center",
                    "margin": "auto",
                    "width": "fit-content",
                    "border": "2px solid #ffdc00"
                    }
                ),
                ],
                style={
                "display": "flex",
                "flexDirection": "column",
                #? Tyto 3 jsem zakomentoval a pak se mi to hezky zarovnalo...
                #"alignItems": "center",
                #"justifyContent": "center",
                #"margin": "30px 0"
                }
            )   
            
        ], style={"display": "flex", "flexWrap": "wrap"}),
        
        html.Div([      
            dash_table.DataTable(
            id='fencers-table',
            columns=[
                #? bohužel neexistuje link na fencera, jen na klub (vlastní URL)   
                {"name": "Name", "id": "name"},
                {"name": "Club", "id": "name_url", "presentation":"markdown"},
                {"name": "Country", "id": "country"},
                {"name": "Sex", "id": "gender"},
                {"name": "Birthyear", "id": "birthyear"},
                ],
            
            style_table={
            'maxWidth': '1000px',
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
        
        html.H2("Filters"),
        html.Div([
            html.Div([
                html.Label("Club"),
                dcc.Dropdown(
                    id="filter-clubs-name",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select clubs..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("City"),
                dcc.Dropdown(
                    id="filter-clubs-city",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select cities..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Button(
                    "Reset Filters",
                    id="reset-clubs-filters-button",
                    n_clicks=0,
                    style={
                        'padding': '10px 20px',
                        'fontSize': '16px',
                        'backgroundColor': '#6c757d',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'marginLeft': '10px',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)'
                    }
                ),
                
                html.H4("Number of Clubs", style={"margin-bottom": "5px", "color": "#001f3f"}),
                
                html.Div(
                    id='output-clubs-filtered-number',
                    style={
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "color": "#007BFF",
                    "backgroundColor": "#f4f4f4",
                    "borderRadius": "12px",
                    "padding": "20px 20px",
                    "boxShadow": "0px 4px 16px rgba(0,0,0,0.10)",
                    "textAlign": "center",
                    "margin": "auto",
                    "width": "fit-content",
                    "border": "2px solid #ffdc00"
                    }
                ),
                ],
                style={
                "display": "flex",
                "flexDirection": "column",
                #? Tyto 3 jsem zakomentoval a pak se mi to hezky zarovnalo...
                #"alignItems": "center",
                #"justifyContent": "center",
                #"margin": "30px 0"
                }
            )   
            
        ], style={"display": "flex", "flexWrap": "wrap"}),
        
        html.Div([      
            dash_table.DataTable(
            id='clubs-table',
            columns=[
                {"name": "Name", "id": "name_url", "presentation":"markdown"},
                {"name": "City", "id": "city"},
                {"name": "Registration number", "id": "registration_number"},
                #{"name": "Contact person", "id": "contact_person"},
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
        
        html.H2("Filters"),
        html.Div([
            html.Div([
                html.Label("Tournament"),
                dcc.Dropdown(
                    id="filter-duels-tournament",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select tournaments..."
                ),
            html.Label("Date"),
                dcc.Dropdown(
                    id="filter-duels-date",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select dates..."
                ),
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("Winner"),
                dcc.Dropdown(
                    id="filter-duels-winner",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select winners..."
                ),
                html.Label("Winner's Club"),
                dcc.Dropdown(
                    id="filter-duels-winner-club",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select winners..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("Loser"),
                dcc.Dropdown(
                    id="filter-duels-loser",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select losers..."
                ),           
                html.Label("Loser's Club"),
                dcc.Dropdown(
                    id="filter-duels-loser-club",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select losers..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),
            
            html.Div([
                html.Label("Fight Level"),
                dcc.Dropdown(
                    id="filter-duels-fight-lvl",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select Fight Level..."
                ),
                html.Label("Gender"),
                dcc.Dropdown(
                    id="filter-duels-gender",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select Gender..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            
            html.Div([
                html.Button(
                    "Reset Filters",
                    id="reset-duels-filters-button",
                    n_clicks=0,
                    style={
                        'padding': '10px 20px',
                        'fontSize': '16px',
                        'backgroundColor': '#6c757d',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'marginLeft': '10px',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)'
                    }
                ),
                
                html.H4("Number of Duels", style={"margin-bottom": "5px", "color": "#001f3f"}),
                
                html.Div(
                    id='output-duels-filtered-number',
                    style={
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "color": "#007BFF",
                    "backgroundColor": "#f4f4f4",
                    "borderRadius": "12px",
                    "padding": "20px 20px",
                    "boxShadow": "0px 4px 16px rgba(0,0,0,0.10)",
                    "textAlign": "center",
                    "margin": "auto",
                    "width": "fit-content",
                    "border": "2px solid #ffdc00"
                    }
                ),
                ],
                style={
                "display": "flex",
                "flexDirection": "column",
                #? Tyto 3 jsem zakomentoval a pak se mi to hezky zarovnalo...
                #"alignItems": "center",
                #"justifyContent": "center",
                #"margin": "30px 0"
                }
            )   
            
        ], style={"display": "flex", "flexWrap": "wrap"}),
        
        html.Div([      
            dash_table.DataTable(
            id='duels-table',
            columns=[
                {"name": "Tournament", "id": "tournament_url", "presentation":"markdown"},
                {"name": "Date", "id": "date"},
                {"name": "Winner", "id": "name_fencer_winner"},
                {"name": "Winner Club", "id": "name_club_winner"},
                {"name": "Loser", "id": "name_fencer_loser"},
                {"name": "Loser Club", "id": "name_club_loser"},
                {"name": "Fight LVL", "id": "type"},
                {"name": "Gender", "id": "gender"},
                {"name": "Winner Score", "id": "winner_score"},
                {"name": "Loser Score", "id": "loser_score"},
                ],
            
            style_table={
            'maxWidth': '1600px',
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
            #TODO: potential easy filtering
            # filter_action='native',
            style_as_list_view=True,
            #filter_action='native',
            export_format='csv'
            )       
        ]),
    ])
    
    return layout
    

def layout_for_eliminations(df_duels):
    coords = {}
    level_counts = {}
    import pandas as pd  # Ensure pandas is imported

    for _, row in df_duels.iterrows():
        level, winner, loser = row['type'], row['winner_name'], row['loser_name']
        level_counts.setdefault(level, 0)
        y = level_counts[level]
        x = level
        coords[(winner, level)] = (x, y * 2)
        coords[(loser, level)] = (x, y * 2 + 1)
        level_counts[level] += 1
    return coords


def eliminations_figure(df_duels, highlight_player=None):

    coords = layout_for_eliminations(df_duels)
    fig = go.Figure()

    score_annotations = {}
    
    max_y = 0
    
    print(df_duels.tail())

    for _, row in df_duels.iterrows():
        level, winner, loser, score = row['type'], row['winner_name'], row['loser_name'], row['total_score']
        x1, y1 = coords[(winner, level)]
        x2, y2 = coords[(loser, level)]

        next_level = level // 2
        x_mid = next_level
        y_mid = (y1 + y2) / 2

        coords[(winner, next_level)] = (x_mid, y_mid)
        score_annotations[(winner, next_level)] = score
        max_y = max(max_y, y1, y2, y_mid)


        line_color = 'red' if highlight_player in [winner, loser] else 'gray'

        if next_level >= 1:
            # Right angle connection from player to mid-point
            fig.add_trace(go.Scatter(x=[x1, x1, x_mid], y=[y1, y_mid, y_mid], mode='lines',
                                     line=dict(color=line_color), showlegend=False, hoverinfo='skip'))
            fig.add_trace(go.Scatter(x=[x2, x2, x_mid], y=[y2, y_mid, y_mid], mode='lines',
                                     line=dict(color=line_color), showlegend=False, hoverinfo='skip'))

        # Add player nodes
        for player, x, y in [(winner, x1, y1), (loser, x2, y2)]:
            fig.add_trace(go.Scatter(
                x=[x], y=[y], text=[player], mode='markers+text', textposition="middle right",
                marker=dict(color='red' if highlight_player == player else 'blue', size=10),
                hovertext=f"Score: {score}", hoverinfo='text',
                customdata=[player],
                showlegend=False
            ))

    # Center final winner vertically
    for (player, level), (x, y) in coords.items():
        if level == 2:
            center_y = max_y / 2
            coords[(player, level)] = (x, center_y)
            fig.add_trace(go.Scatter(x=[x], y=[center_y], text=[player], mode='markers+text', textposition="middle right",
                                     marker=dict(color='red' if highlight_player == player else 'blue', size=12),
                                     hoverinfo='text', customdata=[player], showlegend=False))
        if (player, level) in score_annotations:
            x, y = coords[(player, level)]
            fig.add_trace(go.Scatter(x=[x], y=[y - 0.3], text=[score_annotations[(player, level)]],
                                     mode='text', textposition="bottom center", showlegend=False, hoverinfo='skip'))

    # # Draw final edge from last match to the winner node (level 1)
    # final_winner = df_duels.loc[df_duels["type"]=="2", 'winner_name']
    # x_final, y_final = coords[(final_winner, 2)]
    # x_win, y_win = coords[(final_winner, 1)]

    # fig.add_trace(go.Scatter(
    #     x=[x_final, x_final, x_win],
    #     y=[y_final, y_win, y_win],
    #     mode='lines',
    #     line=dict(color='red' if highlight_player == final_winner else 'gray'),
    #     showlegend=False,
    #     hoverinfo='skip'
    # ))

    fig.update_layout(
        clickmode='event+select',
        xaxis=dict(title='Level', autorange='reversed'),
        yaxis=dict(showgrid=False, showticklabels=False),
        margin=dict(l=20, r=20, t=20, b=20), height=1200
    )
    return fig


def create_eliminations_layout(df_duels):
    
    df_duels = df_duels[df_duels["event_id"] == "e9dd48c4-40e2-4e1b-aa8f-9d22d72975f1" ]
    df_duels = df_duels[df_duels["type"] != "Pool"]
    df_duels["type"] = df_duels["type"].str.replace("Eliminace_", "").astype(int)
    df_duels["total_score"] = df_duels["winner_score"].astype(str) + ":" +  df_duels["loser_score"].astype(str)
    
    df_duels["winner_name"] = df_duels["winner_name"].fillna("999")
    df_duels["loser_name"] = df_duels["loser_name"].fillna("999")
    
    #TODO: potřebuju oboje loser i winner name, páč pracuji jen s Winning zápasy
    all_players = sorted(set(df_duels["winner_name"].tolist() + df_duels["loser_name"].tolist()))
    
    layout = html.Div([
        dcc.Dropdown(
            id='player-search',
            options=[{'label': p, 'value': p} for p in all_players],
            placeholder='Search player...',
            searchable=True,
            style={'width': '300px'}
        ),
        dcc.Graph(id='bracket-graph', figure=eliminations_figure(df_duels))
    ])
    
    return layout
        

def create_tournament_results_layout():
    layout = html.Div([
        
        html.H1("Tournament reuslts"),
        
        html.H2("Here I want "),
        
        html.H2("Filters"),
        html.Div([
            html.Div([
                html.Label("Tournament"),
                dcc.Dropdown(
                    id="filter-tournament-results-name",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select name..."
                ),
                html.Label("Date"),
                dcc.Dropdown(
                    id="filter-tournament-results-date",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select dates..."
                ),
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("Fencer Name"),
                dcc.Dropdown(
                    id="filter-tournament-results-fencer",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select fencer..."
                ),
                html.Label("Club"),
                dcc.Dropdown(
                    id="filter-tournament-results-club",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select clubs..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),
            
            html.Div([
                html.Label("Final Rank"),
                dcc.Dropdown(
                    id="filter-tournament-results-final-rank",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select final ranks..."
                ),
                html.Label("Percentile"),
                dcc.Dropdown(
                    id="filter-tournament-results-percentile",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select percentiles..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Button(
                    "Reset Filters",
                    id="reset-tournament-results-filters-button",
                    n_clicks=0,
                    style={
                        'padding': '10px 20px',
                        'fontSize': '16px',
                        'backgroundColor': '#6c757d',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'marginLeft': '10px',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)'
                    }
                ),

                html.H4("Number of Tournaments Results", style={"margin-bottom": "5px", "color": "#001f3f"}),

                html.Div(
                    id='output-tournament-results-filtered-number',
                    style={
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "color": "#007BFF",
                    "backgroundColor": "#f4f4f4",
                    "borderRadius": "12px",
                    "padding": "20px 20px",
                    "boxShadow": "0px 4px 16px rgba(0,0,0,0.10)",
                    "textAlign": "center",
                    "margin": "auto",
                    "width": "fit-content",
                    "border": "2px solid #ffdc00"
                    }
                ),
                ],
                style={
                "display": "flex",
                "flexDirection": "column",
                #? Tyto 3 jsem zakomentoval a pak se mi to hezky zarovnalo...
                #"alignItems": "center",
                #"justifyContent": "center",
                #"margin": "30px 0"
                }
            )   
            
        ], style={"display": "flex", "flexWrap": "wrap"}),
        
        html.Div([      
            dash_table.DataTable(
            id='tournament-results-table',
            columns=[
                {"name": "Tournament", "id": "tournament_url", "presentation":"markdown"},
                {"name": "Date", "id": "date"}, #? nemusím dátvat suffix, je to unikátní column name
                {"name": "Fencer Namer", "id": "fencer_name_to_check"},
                {"name": "Club", "id": "club_name_to_check", "presentation":"markdown"},
                #TODO:
                #{"name": "Status", "id": "status"},
                #{"name": "Type", "id": "first_rank"},
                {"name": "Final rank", "id": "final_rank"},
                {"name": "Percentile", "id": "percentile"},
                {"name": "Victories", "id": "victories"},
                {"name": "Victories perc", "id": "victories_perc"},
                {"name": "TS", "id": "ts"},
                {"name": "TR", "id": "tr"},
                {"name": "Score Index", "id": "score_index"},
                ],
            
            style_table={
            'maxWidth': '1600px',
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

 #TODO: nějak donacpat někam ten  callback, a upravit appku, a ideálně ted zzůstane starý foirmát + nová page s tabolkama !!


def create_tournaments_layout():
    layout = html.Div([
        
        html.H1("Tournaments"),
        
        html.H2("Here I want "),
        
        html.H2("Filters"),
        html.Div([
            html.Div([
                html.Label("Name"),
                dcc.Dropdown(
                    id="filter-tournaments-name",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select name..."
                ),
            html.Label("Date"),
                dcc.Dropdown(
                    id="filter-tournaments-date",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select dates..."
                ),
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("Discipline"),
                dcc.Dropdown(
                    id="filter-tournaments-discipline",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select disciplines..."
                ),
                html.Label("Type"),
                dcc.Dropdown(
                    id="filter-tournaments-type",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select types..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),

            html.Div([
                html.Label("Gender"),
                dcc.Dropdown(
                    id="filter-tournaments-gender",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select genders..."
                ),
                html.Label("Age category"),
                dcc.Dropdown(
                    id="filter-tournaments-age-category",
                    options=[],
                    multi=True,
                    searchable=True,
                    placeholder="Select age categories..."
                )
            ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),
            
            html.Div([
                html.Button(
                    "Reset Filters",
                    id="reset-tournaments-filters-button",
                    n_clicks=0,
                    style={
                        'padding': '10px 20px',
                        'fontSize': '16px',
                        'backgroundColor': '#6c757d',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'marginLeft': '10px',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)'
                    }
                ),

                html.H4("Number of Tournaments", style={"margin-bottom": "5px", "color": "#001f3f"}),

                html.Div(
                    id='output-tournaments-filtered-number',
                    style={
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "color": "#007BFF",
                    "backgroundColor": "#f4f4f4",
                    "borderRadius": "12px",
                    "padding": "20px 20px",
                    "boxShadow": "0px 4px 16px rgba(0,0,0,0.10)",
                    "textAlign": "center",
                    "margin": "auto",
                    "width": "fit-content",
                    "border": "2px solid #ffdc00"
                    }
                ),
                ],
                style={
                "display": "flex",
                "flexDirection": "column",
                #? Tyto 3 jsem zakomentoval a pak se mi to hezky zarovnalo...
                #"alignItems": "center",
                #"justifyContent": "center",
                #"margin": "30px 0"
                }
            )   
            
        ], style={"display": "flex", "flexWrap": "wrap"}),
        
        html.Div([      
            dash_table.DataTable(
            id='tournaments-table',
            columns=[
                {"name": "Name", "id": "name", "presentation":"markdown"},
                {"name": "Date", "id": "date"},
                {"name": "Discipline", "id": "discipline"},
                {"name": "Type", "id": "type_id"},
                {"name": "Gender", "id": "gender"},
                {"name": "Age category", "id": "age_category"}
                ],
            
            style_table={
            'maxWidth': '1000px',
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


def create_personal_stats_layout(df_duels_prep):
    
    df_duels_prep["name_fencer_winner"].fillna("UNKNOWN", inplace=True)
    df_duels_prep["name_fencer_loser"].fillna("UNKNOWN", inplace=True)
    
    all_players = sorted(set(df_duels_prep["name_fencer_winner"].tolist() + df_duels_prep["name_fencer_loser"].tolist()))
    
    layout = html.Div([
        
        html.H1("Stats"),
        
        html.H2("Here I want "),
        
        html.H3("TODO: select by club, country, birthyear - all dependent picklists"),
        html.H3("TODO: Once selected specific person, display all their 'card'"),
        html.H3("TODO: finish the mutual score, not only list of duels"),
        html.H3("TODO: Make all tables nicer, from list of duels remove some columns"),
        
        #TODO: multifilter also for club. ale musí to vždy končit jediným člověkem
        html.H2("First Fencer"),
        html.Div([
            html.Div([
                html.Label("Name"),
                dcc.Dropdown(
                    id="filter-fencer-name-first",
                    options=[{'label': p, 'value': p} for p in all_players],
                    multi=False,
                    searchable=True,
                    placeholder=all_players[0] if all_players else "No players available"
                ),
            ])
        ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),
    
        html.Table([
            # Header Row
            html.Tr([
                html.Th("Statistic"),
                html.Th("Pool Fights"),
                html.Th("Eliminations"),
                html.Th("Total"),
            ]),

            # Total Duels
            html.Tr([
                html.Td("Total Duels"),
                html.Td(id="stat-total-duels-pool-first"),
                html.Td(id="stat-total-duels-elim-first"),
                html.Td(id="stat-total-duels-total-first"),
            ]),

            # Wins
            html.Tr([
                html.Td("Wins"),
                html.Td(id="stat-wins-pool-first"),
                html.Td(id="stat-wins-elim-first"),
                html.Td(id="stat-wins-total-first"),
            ]),

            # Losses
            html.Tr([
                html.Td("Losses"),
                html.Td(id="stat-losses-pool-first"),
                html.Td(id="stat-losses-elim-first"),
                html.Td(id="stat-losses-total-first"),
            ]),

            # Win Rate
            html.Tr([
                html.Td("Win Rate (%)"),
                html.Td(id="stat-winrate-pool-first"),
                html.Td(id="stat-winrate-elim-first"),
                html.Td(id="stat-winrate-total-first"),
            ]),
            
            # Avg score 
            html.Tr([
                html.Td("Avg Score"),
                html.Td(id="stat-avg-score-pool-first"),
                html.Td(id="stat-avg-score-elim-first"),
                html.Td(id="stat-avg-score-total-first"),
            ]),

            # Tournaments
            html.Tr([
                html.Td("Tournaments"),
                html.Td(id="stat-tournaments-pool-first"),
                html.Td(id="stat-tournaments-elim-first"),
                html.Td(id="stat-tournaments-total-first"),
            ]),
        ],
        style={
            "borderCollapse": "collapse",
            "margin": "auto",
            "width": "80%",
            "textAlign": "center",
            "fontSize": "16px",
        }),
        
        html.Hr(),
        html.H2("Second Fencer"),
        html.Div([
            html.Div([
                html.Label("Name"),
                dcc.Dropdown(
                    id="filter-fencer-name-second",
                    options=[{'label': p, 'value': p} for p in all_players],
                    multi=False,
                    searchable=True,
                    placeholder=all_players[0] if all_players else "No players available"
                ),
            ])
        ], style={"width": "20%", "display": "inline-block", "padding": "5px"}),
    
        html.Table([
            # Header Row
            html.Tr([
                html.Th("Statistic"),
                html.Th("Pool Fights"),
                html.Th("Eliminations"),
                html.Th("Total"),
            ]),

            # Total Duels
            html.Tr([
                html.Td("Total Duels"),
                html.Td(id="stat-total-duels-pool-second"),
                html.Td(id="stat-total-duels-elim-second"),
                html.Td(id="stat-total-duels-total-second"),
            ]),

            # Wins
            html.Tr([
                html.Td("Wins"),
                html.Td(id="stat-wins-pool-second"),
                html.Td(id="stat-wins-elim-second"),
                html.Td(id="stat-wins-total-second"),
            ]),

            # Losses
            html.Tr([
                html.Td("Losses"),
                html.Td(id="stat-losses-pool-second"),
                html.Td(id="stat-losses-elim-second"),
                html.Td(id="stat-losses-total-second"),
            ]),

            # Win Rate
            html.Tr([
                html.Td("Win Rate (%)"),
                html.Td(id="stat-winrate-pool-second"),
                html.Td(id="stat-winrate-elim-second"),
                html.Td(id="stat-winrate-total-second"),
            ]),
            
            # Avg score 
            html.Tr([
                html.Td("Avg Score"),
                html.Td(id="stat-avg-score-pool-second"),
                html.Td(id="stat-avg-score-elim-second"),
                html.Td(id="stat-avg-score-total-second"),
            ]),

            # Tournaments
            html.Tr([
                html.Td("Tournaments"),
                html.Td(id="stat-tournaments-pool-second"),
                html.Td(id="stat-tournaments-elim-second"),
                html.Td(id="stat-tournaments-total-second"),
            ]),
        ],
        style={
            "borderCollapse": "collapse",
            "margin": "auto",
            "width": "80%",
            "textAlign": "center",
            "fontSize": "16px",
        }),
        
        html.Div([      
            dash_table.DataTable(
            id='duels-common-table',
            columns=[
                {"name": "Tournament", "id": "tournament_url", "presentation":"markdown"},
                {"name": "Date", "id": "date"},
                {"name": "Winner", "id": "name_fencer_winner"},
                {"name": "Winner Club", "id": "name_club_winner"},
                {"name": "Loser", "id": "name_fencer_loser"},
                {"name": "Loser Club", "id": "name_club_loser"},
                {"name": "Fight LVL", "id": "type"},
                {"name": "Gender", "id": "gender"},
                {"name": "Winner Score", "id": "winner_score"},
                {"name": "Loser Score", "id": "loser_score"},
                ],
            
            style_table={
            'maxWidth': '1600px',
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
            #TODO: potential easy filtering
            # filter_action='native',
            style_as_list_view=True,
            #filter_action='native',
            export_format='csv'
            )       
        ]),

    ])

    return layout