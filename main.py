# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("data/sp_ratings.csv")
df1 = pd.read_csv("data/sp_lines.csv")

table_dataframe = pd.DataFrame(data = {'Season Number': df['season_number'],
                                       'Episode Number': df['episode_number'],
                                       'Episode Name': df1['episode_name'].unique(), # chave primária do dataframe
                                       'Character with most lines': ['Nobody']*len(df1['episode_name'].unique())})

# Populando a coluna 'Character with most lines'
table_dataframe_row = 0
for season_number in range(1, np.max(df1['season_number']) + 1):
        df_season = df1[df1['season_number'] == season_number]
        for episode_number in range(1, np.max(df_season['episode_number']) + 1):
            df_episode = df_season[df_season['episode_number'] == episode_number]
            table_dataframe.loc[table_dataframe_row, 'Character with most lines'] = df_episode['character'].value_counts().idxmax()
            table_dataframe_row += 1

# creating a new column to hold average ratings for season (yes, duplicated values)
df['avg_season_rating'] = [0]*len(df)

# Populating the 'avg_season_rating' column
for i in range(np.max(df['season_number'])):
    season_subset = df[df['season_number'] == i + 1]
    season_ratings = season_subset['rating']
    average_season_rating = np.mean(season_ratings)
    df.loc[df['season_number'] == i + 1, 'avg_season_rating'] = average_season_rating

# This only has 21 elements whereas df['avg_season_rating'] has 200+ elements
avg_ratings = df['avg_season_rating'].unique()

# Creating the bar chart to be displayed with dcc in the layout
x_range = range(1,22)
fig = px.bar(df, x=x_range, 
                 y=avg_ratings, 
                 barmode="group", 
                 labels={"x" : "Season", "y" : "Average Rating"}, 
                 color=x_range)

fig1 = px.line(df, x=df['season_number'].unique(), y=df.groupby(['season_number'])['season_number'].count(), title = "Episode Count per Season")

min_table_range = 0
max_table_range = len(df[df['season_number'] == 1]) - 1
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='South Park Data Visualization'),
        html.H3(children='This app shows ratings for each season of South Park (from the 1st to 21st).'),
        dcc.Graph(
            id='season-ratings-bar-chart',
            figure=fig
        )
    ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div(children=[
        html.Label('Select a Season:'),
        dcc.Dropdown(options = df['season_number'].unique(), value = 1, id = 'season_dropdown'),
        html.Table(children = [
            html.Thead(
                html.Tr([html.Th(col) for col in table_dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(table_dataframe.iloc[i][col]) for col in table_dataframe.columns
                ]) for i in range(min_table_range, max_table_range)
            ])
        ], id = 'season_table')
    ], style={'width': '49%', 'display': 'inline-block'}),
    dcc.Graph(
        id='season-episode-quantity',
        figure=fig1
    )
])

# updates the table
@app.callback(
    Output(component_id='season_table', component_property='children'),
    Input(component_id='season_dropdown', component_property='value')
)
def update_output_div(input_value):
    first_index = df[df['season_number'] == input_value].index[0]
    return html.Table(children = [
        html.Thead(
            html.Tr([html.Th(col) for col in table_dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(table_dataframe.iloc[i][col]) for col in table_dataframe.columns
            ]) for i in range(first_index, first_index + len(df[df['season_number'] == input_value]))
        ])
    ], id = 'season_table')

if __name__ == '__main__':
    app.run_server(debug=True)
