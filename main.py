# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("data/sp_ratings.csv")

# creating a new column to hold average ratings for season (yes, duplicated values)
df['avg_season_rating'] = [0]*len(df)

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

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(children=[
    html.H1(children='South Park Data Visualization',style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(children='''
        This app shows ratings for each season of South Park (from the 1st to 21st).
    ''', style={ 'textAlign': 'center', 'color': colors['text']}),

    dcc.Graph(
        id='season-ratings-bar-chart',
        figure=fig
    )
], style={'background-color': colors['background']})

if __name__ == '__main__':
    app.run_server(debug=True)
