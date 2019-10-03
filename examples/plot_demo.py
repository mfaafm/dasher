from dasher import Dasher
import dash_core_components as dcc
import plotly.graph_objs as go

app = Dasher(__name__, title="Interactive plotting demo")

index = [1, 2, 3]
data = {"a": [1, 2, 3], "b": [2, -2, 6], "c": [10, 0, -10]}


@app.callback(
    "Line plot", _desc="Try it out!", _labels=["y-Axis column"], column=data.keys()
)
def line_plot(column):
    return [dcc.Graph(figure={"data": [{"x": index, "y": data[column]}]})]


@app.callback("Bar plot", column=data.keys())
def bar_plot(column):
    return [
        dcc.Graph(
            figure={
                "data": [
                    go.Bar(
                        x=index,
                        y=data[column],
                        name="bars",
                    )
                ]
            }
        )
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
