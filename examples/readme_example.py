from dasher import Dasher
import dash_html_components as html

app = Dasher(__name__, title="My first dashboard")


@app.callback(
    "My first callback",
    "Try out the widgets!",
    _labels = ["Greeting", "Place"],
    text="Hello",
    place=["World", "Universe"],
)
def my_callback(text, place):
    msg = "{} {}!".format(text, place)
    return [html.H1(msg)]


if __name__ == "__main__":
    app.run_server(debug=True)
