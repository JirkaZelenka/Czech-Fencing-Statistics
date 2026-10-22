from dash import dcc, html
from dash import dash_table
import plotly.graph_objects as go

# Modern styling constants
MODERN_COLORS = {
    'primary': '#001f3f',
    'accent': '#ffdc00',
    'secondary': '#007BFF',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'white': '#ffffff',
    'gray_light': '#e9ecef',
    'gray_medium': '#6c757d',
    'gray_dark': '#495057'
}

# Modern table styling
def get_modern_table_style():
    return {
        'style_table': {
            'maxWidth': '100%',
            'margin': '20px auto',
            'border': 'none',
            'borderRadius': '12px',
            'overflowX': 'auto',
            'overflowY': 'auto',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)',
            'backgroundColor': MODERN_COLORS['white']
        },
        'style_header': {
            'backgroundColor': MODERN_COLORS['primary'],
            'color': MODERN_COLORS['white'],
            'fontWeight': '600',
            'textAlign': 'center',
            'borderBottom': f'3px solid {MODERN_COLORS["accent"]}',
            'padding': '15px',
            'fontSize': '14px',
            'textTransform': 'uppercase',
            'letterSpacing': '0.5px'
        },
        'style_cell': {
            'padding': '12px 15px',
            'textAlign': 'center',
            'border': 'none',
            'borderBottom': f'1px solid {MODERN_COLORS["gray_light"]}',
            'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
            'fontSize': '14px',
            'backgroundColor': MODERN_COLORS['white']
        },
        'style_data': {
            'backgroundColor': MODERN_COLORS['white'],
            'color': MODERN_COLORS['dark'],
        },
        'style_data_conditional': [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': '#e3f2fd',
                'border': f'1px solid {MODERN_COLORS["secondary"]}'
            }
        ]
    }

# Modern button styling
def get_modern_button_style():
    return {
        'padding': '12px 24px',
        'fontSize': '15px',
        'fontWeight': '600',
        'backgroundColor': MODERN_COLORS['secondary'],
        'color': MODERN_COLORS['white'],
        'border': 'none',
        'borderRadius': '8px',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'boxShadow': '0 2px 4px rgba(0, 123, 255, 0.3)',
        'textTransform': 'none',
        'letterSpacing': '0.3px'
    }

# Modern dropdown styling
def get_modern_dropdown_style():
    return {
        'borderRadius': '8px',
        'border': f'1px solid {MODERN_COLORS["gray_light"]}',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
    }

# Modern label styling
def get_modern_label_style():
    return {
        'fontWeight': '600',
        'fontSize': '14px',
        'color': MODERN_COLORS['dark'],
        'marginBottom': '8px',
        'textTransform': 'uppercase',
        'letterSpacing': '0.5px'
    }

# Modern card/container styling
def get_modern_card_style():
    return {
        'backgroundColor': MODERN_COLORS['white'],
        'borderRadius': '12px',
        'padding': '20px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)',
        'margin': '10px 0'
    }

def create_layout():
    nav_link_style = {
        'color': MODERN_COLORS['white'],
        'fontSize': '15px',
        'fontWeight': '500',
        'textDecoration': 'none',
        'padding': '8px 16px',
        'borderRadius': '6px',
        'transition': 'all 0.3s ease',
        'margin': '0 4px'
    }
    
    layout = html.Div([
        dcc.Location(id='url', refresh=False),

        dcc.Store(id='app-version', data='v1'),  # Store current version
        html.Div([
            html.Div([
                html.Img(
                    src=(
                        "https://s3.eu-west-1.amazonaws.com/assets-test.designeo.cz/"
                        "css-cms/dev/2023-06-08/"
                        "36ef7c20-b52b-4adb-a83e-ecea3b121072_20230608191442.png"
                    ),
                    style={
                        'height': '45px',
                        'margin-right': '20px',
                        'vertical-align': 'middle',
                        'filter': 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))'
                    }
                ),
                html.Div([
                    html.Button('V1 (DB)', id='version-v1-btn', n_clicks=0, style={
                        **get_modern_button_style(),
                        'padding': '6px 12px',
                        'fontSize': '12px',
                        'marginRight': '5px',
                        'backgroundColor': MODERN_COLORS['secondary'],
                    }),
                    html.Button('V2 (Excel)', id='version-v2-btn', n_clicks=0, style={
                        **get_modern_button_style(),
                        'padding': '6px 12px',
                        'fontSize': '12px',
                        'backgroundColor': MODERN_COLORS['gray_medium'],
                    }),
                ], style={'marginRight': '20px', 'display': 'flex', 'alignItems': 'center'}),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Intro', href='/intro', id='nav-intro', style=nav_link_style),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('People', href='/people', id='nav-people', style={**nav_link_style, 'fontWeight': '600'}),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Medals', href='/medals', id='nav-medals', style=nav_link_style),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Clubs', href='/clubs', id='nav-clubs', style={**nav_link_style, 'fontWeight': '600'}),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Eliminations', href='/eliminations', id='nav-eliminations', style=nav_link_style),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Tournament Results', href='/tournament_results', id='nav-tournament-results', style={**nav_link_style, 'fontWeight': '600'}),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Tournaments', href='/tournaments', id='nav-tournaments', style={**nav_link_style, 'fontWeight': '600'}),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Duels', href='/duels', id='nav-duels', style={**nav_link_style, 'fontWeight': '600'}),
                html.Span(" | ", style={'color': 'rgba(255, 255, 255, 0.3)', 'margin': '0 8px'}),
                dcc.Link('Personal Stats', href='/personal_stats', id='nav-personal-stats', style=nav_link_style),
            ], style={
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
                'background': f'linear-gradient(135deg, {MODERN_COLORS["primary"]} 0%, #003d7a 100%)',
                'padding': '12px 20px',
                'position': 'fixed',
                'top': '0',
                'width': '100%',
                'borderBottom': f'3px solid {MODERN_COLORS["accent"]}',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
                'zIndex': '1000',
            }),
        ], style={'marginBottom': '70px'}),

        html.Div(id='page-content', style={
            'paddingTop': '20px',
            'paddingLeft': '20px',
            'paddingRight': '20px',
            'paddingBottom': '40px',
            'maxWidth': '1800px',
            'margin': '0 auto',
            'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
            'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            'minHeight': '100vh'
        })
    ], style={
        'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
        'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        'minHeight': '100vh'
    })

    return layout


def create_intro_layout():
    layout = html.Div([
        html.Div([
            html.H1("Introduction", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("Welcome", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '28px',
                'fontWeight': '600',
                'marginBottom': '20px'
            }),
        ], style={**get_modern_card_style(), 'maxWidth': '800px', 'margin': '0 auto'})
    ], style={'padding': '20px'})
    return layout


def create_people_layout():
    table_styles = get_modern_table_style()
    
    layout = html.Div([
        html.Div([
            html.H1("Fencers", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("Filters", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '24px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
            html.Div([
                html.Div([
                    html.Label("Fencers", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-fencers-name",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select fencers...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Clubs", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-fencers-club",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select clubs...",
                        style=get_modern_dropdown_style()
                    ),
                ], style={**get_modern_card_style(), "width": "22%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div([
                    html.Label("Country", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-fencers-country",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select countries...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Div(id="filter-fencers-gender-container", children=[
                        html.Label("Gender", style={**get_modern_label_style(), 'marginTop': '15px'}),
                        dcc.Dropdown(
                            id="filter-fencers-gender",
                            options=[],
                            multi=True,
                            searchable=True,
                            placeholder="Select genders...",
                            style=get_modern_dropdown_style()
                        )
                    ])
                ], style={**get_modern_card_style(), "width": "22%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div([
                    html.Div(id="filter-fencers-birthyear-container", children=[
                        html.Label("Birthyear", style=get_modern_label_style()),
                        dcc.Dropdown(
                            id="filter-fencers-birthyear",
                            options=[],
                            multi=True,
                            searchable=True,
                            placeholder="Select birthyears...",
                            style=get_modern_dropdown_style()
                        )
                    ])
                ], style={**get_modern_card_style(), "width": "22%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),
                
                html.Div([
                    html.Button(
                        "Reset Filters",
                        id="reset-fencers-filters-button",
                        n_clicks=0,
                        style={
                            **get_modern_button_style(),
                            'backgroundColor': MODERN_COLORS['gray_medium'],
                            'marginBottom': '15px',
                            'width': '100%'
                        }
                    ),
                    
                    html.H4("Number of Fencers", style={
                        "marginBottom": "8px",
                        "color": MODERN_COLORS['primary'],
                        "fontSize": "16px",
                        "fontWeight": "600"
                    }),
                    
                    html.Div(
                        id='output-fencers-filtered-number',
                        style={
                            "fontSize": "24px",
                            "fontWeight": "700",
                            "color": MODERN_COLORS['secondary'],
                            "backgroundColor": MODERN_COLORS['light'],
                            "borderRadius": "12px",
                            "padding": "15px",
                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                            "textAlign": "center",
                            "border": f"3px solid {MODERN_COLORS['accent']}"
                        }
                    ),
                ], style={**get_modern_card_style(), "width": "28%", "display": "inline-block", "verticalAlign": "top", "flexShrink": "0"})
                
            ], style={"display": "flex", "flexWrap": "nowrap", "marginBottom": "30px", "gap": "2%"}),
        ]),
        
        html.Div([
            dash_table.DataTable(
                id='fencers-table',
                columns=[],  # Will be set dynamically based on version
                **table_styles,
                page_size=20,
                sort_action='native',
                style_as_list_view=True,
                export_format='csv'
            )       
        ], style={'marginTop': '20px', 'textAlign': 'center'}),
    ], style={'padding': '20px'})
    return layout


def create_medals_layout():
    layout = html.Div([
        html.Div([
            html.H1("Medals", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("Medal Statistics", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '28px',
                'fontWeight': '600',
                'marginBottom': '20px'
            }),
        ], style={**get_modern_card_style(), 'maxWidth': '800px', 'margin': '0 auto'})
    ], style={'padding': '20px'})
    return layout


def create_clubs_layout():
    table_styles = get_modern_table_style()
    
    layout = html.Div([
        html.Div([
            html.H1("Clubs", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("Filters", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '24px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
            html.Div([
                html.Div([
                    html.Label("Club", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-clubs-name",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select clubs...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Div(id="filter-clubs-city-container", children=[
                        html.Label("City", style={**get_modern_label_style(), 'marginTop': '15px'}),
                        dcc.Dropdown(
                            id="filter-clubs-city",
                            options=[],
                            multi=True,
                            searchable=True,
                            placeholder="Select cities...",
                            style=get_modern_dropdown_style()
                        )
                    ])
                ], style={**get_modern_card_style(), "width": "30%", "display": "inline-block", "marginRight": "3%", "verticalAlign": "top"}),

                html.Div([
                    html.Button(
                        "Reset Filters",
                        id="reset-clubs-filters-button",
                        n_clicks=0,
                        style={
                            **get_modern_button_style(),
                            'backgroundColor': MODERN_COLORS['gray_medium'],
                            'marginBottom': '15px',
                            'width': '100%'
                        }
                    ),
                    
                    html.H4("Number of Clubs", style={
                        "marginBottom": "8px",
                        "color": MODERN_COLORS['primary'],
                        "fontSize": "16px",
                        "fontWeight": "600"
                    }),
                    
                    html.Div(
                        id='output-clubs-filtered-number',
                        style={
                            "fontSize": "24px",
                            "fontWeight": "700",
                            "color": MODERN_COLORS['secondary'],
                            "backgroundColor": MODERN_COLORS['light'],
                            "borderRadius": "12px",
                            "padding": "15px",
                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                            "textAlign": "center",
                            "border": f"3px solid {MODERN_COLORS['accent']}"
                        }
                    ),
                ], style={**get_modern_card_style(), "width": "31%", "display": "inline-block", "verticalAlign": "top", "flexShrink": "0"})   
                
            ], style={"display": "flex", "flexWrap": "nowrap", "marginBottom": "30px", "gap": "3%"}),
        ]),
        
        html.Div([
            dash_table.DataTable(
                id='clubs-table',
                columns=[],  # Will be set dynamically based on version
                **table_styles,
                page_size=20,
                sort_action='native',
                style_as_list_view=True,
                export_format='csv'
            )       
        ], style={'marginTop': '20px'}),
    ], style={'padding': '20px'})
    return layout


def create_duels_layout():
    table_styles = get_modern_table_style()
    
    layout = html.Div([
        html.Div([
            html.H1("Duels", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("Filters", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '24px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
            html.Div([
                html.Div([
                    html.Label("Tournament", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-duels-tournament",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select tournaments...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Date", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-duels-date",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select dates...",
                        style=get_modern_dropdown_style()
                    ),
                ], style={**get_modern_card_style(), "width": "18%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div([
                    html.Label("Winner", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-duels-winner",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select winners...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Winner's Club", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-duels-winner-club",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select winner clubs...",
                        style=get_modern_dropdown_style()
                    )
                ], style={**get_modern_card_style(), "width": "18%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div([
                    html.Label("Loser", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-duels-loser",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select losers...",
                        style=get_modern_dropdown_style()
                    ),           
                    html.Label("Loser's Club", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-duels-loser-club",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select loser clubs...",
                        style=get_modern_dropdown_style()
                    )
                ], style={**get_modern_card_style(), "width": "18%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),
                
                html.Div([
                    html.Label("Fight Level", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-duels-fight-lvl",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select Fight Level...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Div(id="filter-duels-gender-container", children=[
                        html.Label("Gender", style={**get_modern_label_style(), 'marginTop': '15px'}),
                        dcc.Dropdown(
                            id="filter-duels-gender",
                            options=[],
                            multi=True,
                            searchable=True,
                            placeholder="Select Gender...",
                            style=get_modern_dropdown_style()
                        )
                    ])
                ], style={**get_modern_card_style(), "width": "18%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div([
                    html.Button(
                        "Reset Filters",
                        id="reset-duels-filters-button",
                        n_clicks=0,
                        style={
                            **get_modern_button_style(),
                            'backgroundColor': MODERN_COLORS['gray_medium'],
                            'marginBottom': '15px',
                            'width': '100%'
                        }
                    ),
                    
                    html.H4("Number of Duels", style={
                        "marginBottom": "8px",
                        "color": MODERN_COLORS['primary'],
                        "fontSize": "16px",
                        "fontWeight": "600"
                    }),
                    
                    html.Div(
                        id='output-duels-filtered-number',
                        style={
                            "fontSize": "24px",
                            "fontWeight": "700",
                            "color": MODERN_COLORS['secondary'],
                            "backgroundColor": MODERN_COLORS['light'],
                            "borderRadius": "12px",
                            "padding": "15px",
                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                            "textAlign": "center",
                            "border": f"3px solid {MODERN_COLORS['accent']}"
                        }
                    ),
                ], style={**get_modern_card_style(), "width": "20%", "display": "inline-block", "verticalAlign": "top", "flexShrink": "0"})   
                
            ], style={"display": "flex", "flexWrap": "nowrap", "marginBottom": "30px", "gap": "2%"}),
        ]),
        
        html.Div([
            dash_table.DataTable(
                id='duels-table',
                columns=[],  # Will be set dynamically based on version
                **table_styles,
                page_size=20,
                sort_action='native',
                style_as_list_view=True,
                export_format='csv'
            )       
        ], style={'marginTop': '20px'}),
    ], style={'padding': '20px'})
    
    return layout
    

def layout_for_eliminations(df_duels):
    coords = {}
    level_counts = {}

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

    for _, row in df_duels.iterrows():
        level = row['type']
        winner = row['winner_name']
        loser = row['loser_name']
        score = row['total_score']
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
            marker_color = 'red' if highlight_player == player else 'blue'
            fig.add_trace(go.Scatter(
                x=[x], y=[center_y], text=[player],
                mode='markers+text', textposition="middle right",
                marker=dict(color=marker_color, size=12),
                hoverinfo='text', customdata=[player], showlegend=False
            ))
        if (player, level) in score_annotations:
            x, y = coords[(player, level)]
            fig.add_trace(go.Scatter(
                x=[x], y=[y - 0.3],
                text=[score_annotations[(player, level)]],
                mode='text', textposition="bottom center",
                showlegend=False, hoverinfo='skip'
            ))

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
    df_duels["total_score"] = (
        df_duels["winner_score"].astype(str) + ":" +
        df_duels["loser_score"].astype(str)
    )
    
    df_duels["winner_name"] = df_duels["winner_name"].fillna("999")
    df_duels["loser_name"] = df_duels["loser_name"].fillna("999")
    
    #TODO: potřebuju oboje loser i winner name,
    # páč pracuji jen s Winning zápasy
    all_players = sorted(set(df_duels["winner_name"].tolist() + df_duels["loser_name"].tolist()))
    
    layout = html.Div([
        html.Div([
            html.H1("Eliminations Bracket", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.Div([
                html.Label("Search Player", style={
                    **get_modern_label_style(),
                    'marginBottom': '10px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='player-search',
                    options=[{'label': p, 'value': p} for p in all_players],
                    placeholder='Search player...',
                    searchable=True,
                    style={
                        **get_modern_dropdown_style(),
                        'width': '100%',
                        'maxWidth': '400px'
                    }
                ),
            ], style={**get_modern_card_style(), 'width': 'fit-content', 'margin': '0 auto 30px'}),
            
            html.Div([
                dcc.Graph(
                    id='bracket-graph',
                    figure=eliminations_figure(df_duels),
                    style={
                        'backgroundColor': MODERN_COLORS['white'],
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                        'padding': '20px'
                    }
                )
            ], style={'marginTop': '20px'})
        ])
    ], style={'padding': '20px'})
    
    return layout
        

def create_tournament_results_layout():
    table_styles = get_modern_table_style()
    
    layout = html.Div([
        html.Div([
            html.H1("Tournament Results", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("Filters", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '24px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
            html.Div([
                html.Div([
                    html.Label("Tournament", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-tournament-results-name",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select tournament...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Date", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-tournament-results-date",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select dates...",
                        style=get_modern_dropdown_style()
                    ),
                ], style={**get_modern_card_style(), "width": "18%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div([
                    html.Label("Fencer Name", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-tournament-results-fencer",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select fencer...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Club", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-tournament-results-club",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select clubs...",
                        style=get_modern_dropdown_style()
                    )
                ], style={**get_modern_card_style(), "width": "18%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),
                
                html.Div([
                    html.Label("Final Rank", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-tournament-results-final-rank",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select final ranks...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Percentile", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-tournament-results-percentile",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select percentiles...",
                        style=get_modern_dropdown_style()
                    )
                ], style={**get_modern_card_style(), "width": "18%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div([
                    html.Button(
                        "Reset Filters",
                        id="reset-tournament-results-filters-button",
                        n_clicks=0,
                        style={
                            **get_modern_button_style(),
                            'backgroundColor': MODERN_COLORS['gray_medium'],
                            'marginBottom': '15px',
                            'width': '100%'
                        }
                    ),

                    html.H4(
                        "Number of Tournament Results",
                        style={
                            "marginBottom": "8px",
                            "color": MODERN_COLORS['primary'],
                            "fontSize": "16px",
                            "fontWeight": "600"
                        }
                    ),

                    html.Div(
                        id='output-tournament-results-filtered-number',
                        style={
                            "fontSize": "24px",
                            "fontWeight": "700",
                            "color": MODERN_COLORS['secondary'],
                            "backgroundColor": MODERN_COLORS['light'],
                            "borderRadius": "12px",
                            "padding": "15px",
                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                            "textAlign": "center",
                            "border": f"3px solid {MODERN_COLORS['accent']}"
                        }
                    ),
                ], style={**get_modern_card_style(), "width": "38%", "display": "inline-block", "verticalAlign": "top", "flexShrink": "0"})   
                
            ], style={"display": "flex", "flexWrap": "nowrap", "marginBottom": "30px", "gap": "2%"}),
        ]),
        
        html.Div([
            dash_table.DataTable(
                id='tournament-results-table',
                columns=[
                    {"name": "Tournament", "id": "tournament_url", "presentation":"markdown"},
                    {"name": "Date", "id": "date"},
                    {"name": "Fencer Name", "id": "fencer_name_to_check"},
                    {"name": "Club", "id": "club_name_to_check", "presentation":"markdown"},
                    {"name": "Final rank", "id": "final_rank"},
                    {"name": "Percentile", "id": "percentile"},
                    {"name": "Victories", "id": "victories"},
                    {"name": "Victories perc", "id": "victories_perc"},
                    {"name": "TS", "id": "ts"},
                    {"name": "TR", "id": "tr"},
                    {"name": "Score Index", "id": "score_index"},
                ],
                **table_styles,
                page_size=20,
                sort_action='native',
                style_as_list_view=True,
                export_format='csv'
            )       
        ], style={'marginTop': '20px'}),
    ], style={'padding': '20px'})
    
    return layout

 #TODO: nějak donacpat někam ten callback, a upravit appku,
# a ideálně ted zzůstane starý foirmát + nová page s tabolkama !!


def create_tournaments_layout():
    table_styles = get_modern_table_style()
    
    layout = html.Div([
        html.Div([
            html.H1("Tournaments", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("Filters", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '24px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
            html.Div([
                html.Div([
                    html.Label("Name", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-tournaments-name",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select name...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Date", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-tournaments-date",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select dates...",
                        style=get_modern_dropdown_style()
                    ),
                ], style={**get_modern_card_style(), "width": "22%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div(id="filter-tournaments-discipline-type-container", children=[
                    html.Label("Discipline", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-tournaments-discipline",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select disciplines...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Type", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-tournaments-type",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select types...",
                        style=get_modern_dropdown_style()
                    )
                ], style={**get_modern_card_style(), "width": "22%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),

                html.Div(id="filter-tournaments-gender-age-container", children=[
                    html.Label("Gender", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-tournaments-gender",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select genders...",
                        style=get_modern_dropdown_style()
                    ),
                    html.Label("Age category", style={**get_modern_label_style(), 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="filter-tournaments-age-category",
                        options=[],
                        multi=True,
                        searchable=True,
                        placeholder="Select age categories...",
                        style=get_modern_dropdown_style()
                    )
                ], style={**get_modern_card_style(), "width": "22%", "display": "inline-block", "marginRight": "2%", "verticalAlign": "top"}),
                
                html.Div([
                    html.Button(
                        "Reset Filters",
                        id="reset-tournaments-filters-button",
                        n_clicks=0,
                        style={
                            **get_modern_button_style(),
                            'backgroundColor': MODERN_COLORS['gray_medium'],
                            'marginBottom': '15px',
                            'width': '100%'
                        }
                    ),

                    html.H4("Number of Tournaments", style={
                        "marginBottom": "8px",
                        "color": MODERN_COLORS['primary'],
                        "fontSize": "16px",
                        "fontWeight": "600"
                    }),

                    html.Div(
                        id='output-tournaments-filtered-number',
                        style={
                            "fontSize": "24px",
                            "fontWeight": "700",
                            "color": MODERN_COLORS['secondary'],
                            "backgroundColor": MODERN_COLORS['light'],
                            "borderRadius": "12px",
                            "padding": "15px",
                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                            "textAlign": "center",
                            "border": f"3px solid {MODERN_COLORS['accent']}"
                        }
                    ),
                ], style={**get_modern_card_style(), "width": "28%", "display": "inline-block", "verticalAlign": "top", "flexShrink": "0"})   
                
            ], style={"display": "flex", "flexWrap": "nowrap", "marginBottom": "30px", "gap": "2%"}),
        ]),
        
        html.Div([
            dash_table.DataTable(
                id='tournaments-table',
                columns=[],  # Will be set dynamically based on version
                **table_styles,
                page_size=20,
                sort_action='native',
                style_as_list_view=True,
                export_format='csv'
            )       
        ], style={'marginTop': '20px'}),
    ], style={'padding': '20px'})
    
    return layout


def create_personal_stats_layout(df_duels_prep):
    # Create a copy to avoid mutating the original dataframe
    df_copy = df_duels_prep.copy()
    df_copy["name_fencer_winner"].fillna("UNKNOWN", inplace=True)
    df_copy["name_fencer_loser"].fillna("UNKNOWN", inplace=True)
    
    all_players = sorted(set(
        df_copy["name_fencer_winner"].tolist() +
        df_copy["name_fencer_loser"].tolist()
    ))
    
    table_styles = get_modern_table_style()
    stats_table_style = {
        "borderCollapse": "separate",
        "borderSpacing": "0",
        "margin": "30px auto",
        "width": "90%",
        "textAlign": "center",
        "fontSize": "15px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "borderRadius": "12px",
        "overflow": "hidden"
    }
    
    layout = html.Div([
        html.Div([
            html.H1("Personal Statistics", style={
                'color': MODERN_COLORS['primary'],
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textAlign': 'center',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }),
            html.Hr(style={'border': f'2px solid {MODERN_COLORS["accent"]}', 'width': '100px', 'margin': '0 auto 30px'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.H2("First Fencer", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '28px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
            html.Div([
                html.Div([
                    html.Label("Name", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-fencer-name-first",
                        options=[{'label': p, 'value': p} for p in all_players],
                        multi=False,
                        searchable=True,
                        placeholder=all_players[0] if all_players else "No players available",
                        style=get_modern_dropdown_style()
                    ),
                ])
            ], style={**get_modern_card_style(), "width": "300px", "marginBottom": "20px"}),
        
            html.Table([
                html.Tr([
                    html.Th("Statistic", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600',
                        'textAlign': 'left'
                    }),
                    html.Th("Pool Fights", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600'
                    }),
                    html.Th("Eliminations", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600'
                    }),
                    html.Th("Total", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600'
                    }),
                ]),
                html.Tr([
                    html.Td("Total Duels", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-total-duels-pool-first", style={'padding': '12px'}),
                    html.Td(id="stat-total-duels-elim-first", style={'padding': '12px'}),
                    html.Td(id="stat-total-duels-total-first", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Wins", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-wins-pool-first", style={'padding': '12px'}),
                    html.Td(id="stat-wins-elim-first", style={'padding': '12px'}),
                    html.Td(id="stat-wins-total-first", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Losses", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-losses-pool-first", style={'padding': '12px'}),
                    html.Td(id="stat-losses-elim-first", style={'padding': '12px'}),
                    html.Td(id="stat-losses-total-first", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Win Rate (%)", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-winrate-pool-first", style={'padding': '12px'}),
                    html.Td(id="stat-winrate-elim-first", style={'padding': '12px'}),
                    html.Td(id="stat-winrate-total-first", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Avg Score", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-avg-score-pool-first", style={'padding': '12px'}),
                    html.Td(id="stat-avg-score-elim-first", style={'padding': '12px'}),
                    html.Td(id="stat-avg-score-total-first", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Tournaments", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-tournaments-pool-first", style={'padding': '12px'}),
                    html.Td(id="stat-tournaments-elim-first", style={'padding': '12px'}),
                    html.Td(id="stat-tournaments-total-first", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
            ], style=stats_table_style),
        ], style={'marginBottom': '50px'}),
        
        html.Hr(style={'border': f'2px solid {MODERN_COLORS["gray_light"]}', 'margin': '40px 0'}),
        
        html.Div([
            html.H2("Second Fencer", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '28px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
            html.Div([
                html.Div([
                    html.Label("Name", style=get_modern_label_style()),
                    dcc.Dropdown(
                        id="filter-fencer-name-second",
                        options=[{'label': p, 'value': p} for p in all_players],
                        multi=False,
                        searchable=True,
                        placeholder=all_players[0] if all_players else "No players available",
                        style=get_modern_dropdown_style()
                    ),
                ])
            ], style={**get_modern_card_style(), "width": "300px", "marginBottom": "20px"}),
        
            html.Table([
                html.Tr([
                    html.Th("Statistic", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600',
                        'textAlign': 'left'
                    }),
                    html.Th("Pool Fights", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600'
                    }),
                    html.Th("Eliminations", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600'
                    }),
                    html.Th("Total", style={
                        'backgroundColor': MODERN_COLORS['primary'],
                        'color': MODERN_COLORS['white'],
                        'padding': '15px',
                        'fontWeight': '600'
                    }),
                ]),
                html.Tr([
                    html.Td("Total Duels", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-total-duels-pool-second", style={'padding': '12px'}),
                    html.Td(id="stat-total-duels-elim-second", style={'padding': '12px'}),
                    html.Td(id="stat-total-duels-total-second", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Wins", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-wins-pool-second", style={'padding': '12px'}),
                    html.Td(id="stat-wins-elim-second", style={'padding': '12px'}),
                    html.Td(id="stat-wins-total-second", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Losses", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-losses-pool-second", style={'padding': '12px'}),
                    html.Td(id="stat-losses-elim-second", style={'padding': '12px'}),
                    html.Td(id="stat-losses-total-second", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Win Rate (%)", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-winrate-pool-second", style={'padding': '12px'}),
                    html.Td(id="stat-winrate-elim-second", style={'padding': '12px'}),
                    html.Td(id="stat-winrate-total-second", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Avg Score", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-avg-score-pool-second", style={'padding': '12px'}),
                    html.Td(id="stat-avg-score-elim-second", style={'padding': '12px'}),
                    html.Td(id="stat-avg-score-total-second", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
                html.Tr([
                    html.Td("Tournaments", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                    html.Td(id="stat-tournaments-pool-second", style={'padding': '12px'}),
                    html.Td(id="stat-tournaments-elim-second", style={'padding': '12px'}),
                    html.Td(id="stat-tournaments-total-second", style={'padding': '12px', 'fontWeight': '600', 'backgroundColor': MODERN_COLORS['light']}),
                ]),
            ], style=stats_table_style),
        ], style={'marginBottom': '50px'}),
        
        html.Div([
            html.H2("Common Duels", style={
                'color': MODERN_COLORS['dark'],
                'fontSize': '28px',
                'fontWeight': '600',
                'marginBottom': '20px',
                'paddingBottom': '10px',
                'borderBottom': f'2px solid {MODERN_COLORS["gray_light"]}'
            }),
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
                **table_styles,
                page_size=20,
                sort_action='native',
                style_as_list_view=True,
                export_format='csv'
            )       
        ], style={'marginTop': '30px'}),

    ], style={'padding': '20px'})

    return layout