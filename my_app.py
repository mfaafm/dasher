from dasher import Dasher
import dash_html_components as html
import dash_core_components as dcc

app = Dasher(__name__)

@app.callback(
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

@app.callback(
    a=True,
    b=["apple", "orange", "lemon", "banana"],
)
def my_second_function(*args):
    text = " ".join(
        ["{}: {} ({})".format(i, v, str(type(v))) for i, v in enumerate(args)]
    )
    return [html.Label(text)]

# app.callback(
#     my_function,
#     a=True,
#     b="Test",
#     c=["apple", "orange", "lemon", "banana"],
#     d={"One": 1, "Two": 2},
#     e=10,
#     g=(10, 20),
#     h=(10, 20, 2),
#     i=2.2,
#     j=(1.134, 3.125),
#     k=(0.0, 1.0, 0.01)
# )

if __name__ == "__main__":
    app.run_server(debug=True)
