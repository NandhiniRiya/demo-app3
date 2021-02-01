import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv("Downloads\Reference_documents.csv")
LOCATION = df.LOCATION.unique()
Year = df.Year.unique()
data_table = dash_table.DataTable(
    id='data-table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
data_store = dcc.Store(id = 'data-store',
                      data = df.to_dict('records'))
heading = html.H1(children='Kaatumannar Kovil')
subheading = html.Div(children='''
       Choose The Location
    ''')
static_graph = dcc.Graph(
        id='example-graph',
        figure={}
    )
dropdown1=dcc.Dropdown(
        id='dropdown1',
        options=[{'label': x, 'value': x} for x in LOCATION],
        value=LOCATION[0],
        clearable=False,
    )
dropdown2=dcc.Dropdown(
        id='dropdown2',
        options=[{'label': x, 'value': x} for x in Year],
        value=Year[0],
        clearable=False,
    )
button_click = dbc.Button("Filter Graph", id = "go-button", color="primary")
dropdown_section = dbc.Row([
      dbc.Col([
        dropdown1
    ], width = 3),
    html.Br(),
    dbc.Col([
        dropdown2
    ], width = 3)
]
)
app.layout = html.Div(children=[
    heading,
    subheading,
    data_store,
    html.Br(),
    dropdown_section,
    html.Br(),
    button_click,
    dcc.Loading([static_graph,
    data_table]),
    html.Br(),
    html.Br(),
])
#Update table and graph
@app.callback([Output('data-table', 'data'),
              Output('example-graph', 'figure')],
             [Input('go-button', 'n_clicks')],
             [State('dropdown1', 'value'),
             State('dropdown2', 'value'),
             State('data-store', 'data')])
def update_data_table(n, LOCATION, Year, data_store):
    df = pd.DataFrame(data_store)
    df = df[(df.LOCATION == LOCATION)]
    df = df[(df.Year == Year)]
    fig = px.histogram(df, x='Alliance', y='Votes', color = 'Year', barmode="group")
    updated_data = df.to_dict('records')
    return updated_data, fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
