import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

navbar = dbc.NavbarSimple(
    children=[], brand="Example Dashboard", brand_href="#", sticky="top"
)

graph_1 = dcc.Graph(
    id="example-graph-1",
    figure={
        "data": [
            {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
            {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": u"Montréal"},
        ],
        "layout": {"title": "Dash Data Visualization"},
    },
)

tab1_content = dbc.Card(dbc.CardBody([dbc.CardText("This is tab 1!"), graph_1]))

graph_2 = dcc.Graph(
    id="example-graph-2",
    figure={
        "data": [
            {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
            {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": u"Montréal"},
        ],
        "layout": {"title": "Dash Data Visualization"},
    },
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    html.Label("Checkboxes"),
                    dcc.Checklist(
                        options=[
                            {"label": "New York City", "value": "NYC"},
                            {"label": u"Montréal", "value": "MTL"},
                            {"label": "San Francisco", "value": "SF"},
                        ],
                        values=["MTL", "SF"],
                    ),
                ]
            ),
            dbc.Row([graph_2]),
        ]
    )
)



body = dbc.Container(
    dbc.Tabs(
        [dbc.Tab(tab1_content, label="Tab 1"), dbc.Tab(tab2_content, label="Tab 2")]
    )
)

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
    ],
)

app.layout = html.Div([navbar, body])

if __name__ == "__main__":
    app.run_server()
