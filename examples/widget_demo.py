from dasher import Dasher
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

app = Dasher(__name__, title="Widget Demo")


@app.callback(
    "All widgets",
    "Demo of all supported automatic widgets and one custom component",
    boolean=True,
    string="Test",
    enum=["apple", "orange", "lemon", "banana"],
    mapping={"One": 1, "Two": 2},
    integer=10,
    tuple_int_2=(10, 20),
    tuple_int_3=(10, 20, 2),
    floating=2.2,
    tuple_float_2=(1.134, 3.125),
    tuple_float_3=(0.0, 1.0, 0.01),
    custom_component=dcc.RangeSlider(count=1, min=-5, max=10, step=0.5, value=[-3, 7]),
)
def my_function(*args):
    table_header = [
        html.Thead(html.Tr([html.Th("Argument"), html.Th("Type"), html.Th("Value")]))
    ]
    table_rows = [
        html.Tr([html.Td(str(i)), html.Td(str(type(v))), html.Td(repr(v))])
        for i, v in enumerate(args)
    ]
    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, bordered=True)
    return [table]


if __name__ == "__main__":
    app.run_server(debug=True)
