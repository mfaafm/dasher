import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dasher import Api

# data for the plots
index = [1, 2, 3]
data = {"a": [1, 2, 3], "b": [2, -2, 6], "c": [10, 0, -10]}

# generate widget with dasher api
dapi = Api()
y_axis = dapi.get_component("y_axis_dropdown", data.keys())

# define custom dash layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

axis_form_group = dbc.FormGroup(
    [dbc.Label("y-axis", html_for="y_axis_dropdown"), y_axis]
)
form = dbc.Form([axis_form_group])

output_container = dbc.Container(id="output")
app.layout = html.Div([dbc.Row(dbc.Col(form)), dbc.Row(dbc.Col(output_container))])


@app.callback(Output("output", "children"), [Input("y_axis_dropdown", "value")])
def my_callback(y_axis):
    return [dcc.Graph(figure={"data": [{"x": index, "y": data[y_axis]}]})]


if __name__ == "__main__":
    app.run_server(debug=True)
