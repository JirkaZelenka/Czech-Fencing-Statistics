
# ! This one is functional minimal plotly on my fencing data

# Import packages
from dash import Dash, html, dash_table, dcc, callback_context
import pandas as pd
import sqlite3
import plotly.express as px

app = Dash(__name__)

server = app.server

source_file = f'./fencing_all.db'

conn = sqlite3.connect(source_file)
query = "SELECT * FROM fencers"
df = pd.read_sql_query(query, conn)
conn.close()

"""
df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
"""

# takto olabeluju jen ty existující. a pořád mi to stejně dělá dvojbiny.../
#bins = sorted(df['birthyear'].unique())
#labels = [str(binn) for binn in bins]  

bins = list(range(df['birthyear'].min(), df['birthyear'].max()+1))
labels = [str(binn) for binn in bins]  

fig = px.histogram(df, x='birthyear', color='sex', title='Histogram of Records Count by Year and Sex', nbins=len(bins))
fig.update_xaxes(tickvals=bins, ticktext=labels)

app.layout = html.Div([
    html.Div(children='My First App with Data'),
    #dash_table.DataTable(data=df.to_dict('records'), page_size=20),
    dcc.Graph(figure=px.histogram(df, x='birthyear',  color='club_id', nbins=len(df['birthyear'].unique()))),
    dcc.Graph(figure=fig),
    """
    html.Div(children='My Second App with Data'),
    dcc.Graph(figure=px.histogram(df2, x='continent', y='lifeExp', histfunc='avg')),
    dash_table.DataTable(data=df2.to_dict('records'), page_size=20),
    """
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port = 8051)