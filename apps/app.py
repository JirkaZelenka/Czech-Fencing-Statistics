from dash import Dash, html, dcc
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

bins = list(range(df['birthyear'].min(), df['birthyear'].max()+1))
labels = [str(binn) for binn in bins]  

fig = px.histogram(df, x='birthyear', color='sex', title='TEST Histogram of Records Count by Year and Sex', nbins=len(bins))
fig.update_xaxes(tickvals=bins, ticktext=labels)

app.layout = html.Div([
    html.Div(children='TEST My First App with Data'),
    dcc.Graph(figure=px.histogram(df, x='birthyear',  color='club_id', nbins=len(df['birthyear'].unique()))),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True, port = 8051)
