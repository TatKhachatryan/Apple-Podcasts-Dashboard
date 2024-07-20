import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import HTML

import dash
from dash import dash_table
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

df = pd.read_csv('https://raw.githubusercontent.com/TatKhachatryan/Apple-Podcasts-Dashboard/main/applepodcasts.csv')
df.columns = ['podcast_id', 'Link', 'Title', 'Avg Rating', 'Ratings Count', 'Author', 'Main Category']

def make_clickable(val):
    return f'[Click here to listen to the podcast]({val})'

colors = ['#001219', '#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#ee9b00', '#ca6702', '#bb3e03', '#ae2012', '#9b2226', '#606c38', '#283618', '#fefae0', '#dda15e', '#bc6c25', '#2c6e49', '#4c956c', '#fefee3', '#ffc9b9', '#d68c45']

def top_10_by_category(category):
    """This function returns top 10 podcasts by category
    input: genre name
    return: df of top 10 podcasts (Title, Link)"""
    
    top10 = df[df['Main Category']==category].sort_values(by=['Avg Rating', 'Ratings Count'], ascending=False)[:10][['Title', 'Link']].reset_index(drop=True)
    top10.columns = ['Title', 'Link']
    top10['Link'] = top10['Link'].apply(make_clickable)
    return top10
def directories_by_category(category):
    """This function returns list of podcasts in alp order by given category
    input: category name
    return: list of podcasts, link and avg rating """
    
    directory = df[df['Main Category']==category].sort_values(by='Title', ascending=True)[['Title', 'Link', 'Avg Rating']].reset_index(drop=True)
    directory.columns = ['Title', 'Link', 'Avg Rating']
    directory['Link'] = directory['Link'].apply(make_clickable)
    return directory

directories_by_category('Sports')
categories = df['Main Category'].value_counts()

figure1 = px.bar(categories, x=categories.values,
             y=categories.index, color=categories.index, 
             color_discrete_sequence=colors)
figure1.update_layout(title='Number of Podcasts by Categories', height=500,showlegend=False, title_x=0.5, xaxis_title="Count")

external_stylesheets = [dbc.themes.JOURNAL]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server
app.title = 'Apple Podcasts Dashboard'

card_content1 = [
    dbc.CardHeader("Data Source: https://www.kaggle.com/datasets/thoughtvector/podcastreviews"),
    dbc.CardBody([
        html.P("""This data contains approx. 76,500 podcasts hosting on Apple Podcasts.""", className="card-text"),
    ]),
]

card_content2 = [
    dbc.CardHeader("Podcast Categories."),
    dbc.CardBody([
        html.P("""There are 19 main categories in data. The proportion is shown below.""", className="card-text"),
    ]),
]

app.layout = html.Div([
    html.H1("Apple Podcasts Dashboard", style={"text-align": "center"}),

    html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(card_content1, color="light")),
            dbc.Col(dbc.Card(card_content2, color="light")),
        ]),
    ]),

    html.Div(children=[
        dcc.Graph(id="graph-1", figure=figure1, style={'display': 'flex'}),
        html.Div(style={
            'borderBottom': '2px solid #000',
            'margin': '20px 0'
        }),


        html.Div([
            html.P('Select a category:', style={'textAlign': 'left', 'marginLeft': 30, 'width': '40%'}),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': cat, 'value': cat} for cat in df['Main Category'].unique()],
                value='Sports',
                style={'textAlign': 'left', 'margin': 10, 'width': '40%'}
            )
        ]),
        html.H5(children="The table below shows the Top 10 podcasts for the chosen category:", style={'textAlign': 'center', 'marginLeft': 10, "font-weight": "bold"}),


        html.Div(children=[
            dash_table.DataTable(
                id='top-10-table',
                columns=[{"name": i, "id": i, "presentation": "markdown"} for i in ['Title', 'Link']],
                data=[],
                sort_action='native',
                page_size=10,
                style_table={'margin-bottom': '40px', 'height': '300px', 'overflowY': 'auto'},
                style_cell={'fontSize': 15, 'font-family': 'sans-serif'},
                style_header={
                    'backgroundColor': '#e9d8a6',
                    'fontWeight': 'bold'},
            ),
            html.Div([
                html.Button("Click to Download Top 10 Table", id="download-top-10", n_clicks=0,
                            style={
                                'background-color': 'white',
                                'color': 'black',
                                'border-radius': '20px',
                                'border-color': '#0a9396'
                            }),
            ], style={
                'display': 'flex',
                'justify-content': 'center',
                'margin-top': '20px'
            }),
            dcc.Download(id="download-top-10-excel")
        ], style={'margin-top': '50px'}),

        html.Div(style={
            'borderBottom': '2px solid #000',
            'margin': '20px 0'
        }),

        html.H5(children="The table below shows the directory of podcasts for the chosen category:", style={'textAlign': 'center', 'marginLeft': 10, "font-weight": "bold"}),

        html.Div(children=[
            dash_table.DataTable(
                id='directory-table',
                columns=[{"name": i, "id": i, "presentation": "markdown"} for i in ['Title', 'Link', 'Avg Rating']],
                data=[],
                sort_action='native',
                page_size=15,
                style_table={'margin': 'auto', 'height': '300px', 'overflowY': 'auto'},
                style_cell={'fontSize': 15, 'font-family': 'sans-serif'},
                style_header={
                    'backgroundColor': '#0a9396',
                    'fontWeight': 'bold',
                    'color': 'white'},
            ),
            html.Div([
                html.Button("Click to Download Directory Table", id="download-directory", n_clicks=0,
                            style={
                                'background-color': 'white',
                                'color': 'black',
                                'border-radius': '20px',
                                'border-color': '#0a9396'
                            }),
            ], style={
                'display': 'flex',
                'justify-content': 'center',
                'margin-top': '20px'
            }),
            dcc.Download(id="download-directory-excel")
        ], style={'margin-top': '20px'})
    ]),
    html.Div(style={
            'borderBottom': '2px solid #000',
            'margin': '20px 0'
        }),
    html.H5(children="Thank you for your time. Any feedback is much appreciated. Let's connect👇 ",
            style={'textAlign': 'center', 'marginLeft': 10, "font-weight": "bold"}),
    html.Div([
        html.A("LinkedIn", href="https://www.linkedin.com/in/tatevik-khachatryan-/", target="_blank", style={'margin': '10px'}),
        html.A("GitHub", href="https://github.com/TatKhachatryan/Apple-Podcasts-Dashboard", target="_blank", style={'margin': '10px'})
    ], style={'text-align': 'center', 'margin-top': '20px'}),

])

@app.callback(
    [Output('top-10-table', 'data'),
     Output('directory-table', 'data')],
    [Input('category-dropdown', 'value')]
)
def update_tables(category):
    top10 = top_10_by_category(category)
    directory = directories_by_category(category)
    return top10.to_dict('records'), directory.to_dict('records')

@app.callback(
    Output("download-top-10-excel", "data"),
    [Input("download-top-10", "n_clicks")],
    [dash.dependencies.State('top-10-table', 'data')]
)
def download_top_10(n_clicks, data):
    if n_clicks > 0:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_excel, "top_10_podcasts.xlsx", index=False)

@app.callback(
    Output("download-directory-excel", "data"),
    [Input("download-directory", "n_clicks")],
    [dash.dependencies.State('directory-table', 'data')]
)
def download_directory(n_clicks, data):
    if n_clicks > 0:
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_excel, "directory_podcasts.xlsx", index=False)

if __name__ == '__main__':
    app.run_server(debug=False)
