import pandas as pd
import numpy as np
from dasher import Dasher
import dash_core_components as dcc
import plotly.graph_objs as go

app = Dasher(__name__, title="Interactive plotting demo")


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


if __name__ == "__main__":
    app.run_server(debug=True)
