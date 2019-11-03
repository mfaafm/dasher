import dash_html_components as html

from dasher import Dasher

app = Dasher(__name__, title="My first dashboard")


@app.callback(
    _name="My first callback",
    _desc="Try out the widgets!",
    _labels=["Greeting", "Place"],
    text="Hello",
    place=["World", "Universe"],
)
def my_callback(text, place):
    msg = "{} {}!".format(text, place)
    return [html.H1(msg)]


if __name__ == "__main__":
    app.run_server(debug=True)
