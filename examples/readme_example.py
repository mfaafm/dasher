from dasher import Dasher
import dash_html_components as html

app = Dasher(__name__, title="My first dashboard")


@app.callback("My first callback", "Type something...!", text="Hello World!")
def my_callback(text):
    return [html.H1(text)]


if __name__ == '__main__':
    app.run_server(debug=True)
