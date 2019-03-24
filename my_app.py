import pandas as pd
import numpy as np
from dasher import Dasher
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

app = Dasher(__name__, title="My fancy dashboard")


df = pd.DataFrame(
    {
        "x": np.arange(3),
        "a": np.arange(1, 4),
        "b": np.array([2, -2, 12]),
        "c": np.array([10, 0, -10]),
    }
)


@app.callback("Line plot", column=df.columns.drop("x"))
def line_plot(column):
    return [dcc.Graph(figure={"data": [{"x": df.x, "y": df[column]}]})]


@app.callback("Bar plot", column=df.columns.drop("x"))
def bar_plot(column):
    return [
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=df.x,
                        y=df[column],
                        name="bars",
                        marker=go.bar.Marker(color="rgb(55, 83, 109)"),
                    )
                ]
            )
        )
    ]


@app.callback(
    "All widgets",
    "Demo of all supported automatic widgets",
    a=True,
    b="Test",
    c=["apple", "orange", "lemon", "banana"],
    d={"One": 1, "Two": 2},
    e=10,
    g=(10, 20),
    h=(10, 20, 2),
    i=2.2,
    j=(1.134, 3.125),
    k=(0.0, 1.0, 0.01),
    m=dcc.RangeSlider(count=1, min=-5, max=10, step=0.5, value=[-3, 7]),
)
def my_function(*args):
    text = " ".join(
        ["{}: {} ({})".format(i, v, str(type(v))) for i, v in enumerate(args)]
    )
    return [html.Label(text)]


if __name__ == "__main__":
    app.run_server(debug=True)
