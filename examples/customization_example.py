import dash_bootstrap_components as dbc
import dash_html_components as html

from dasher import CustomWidget
from dasher import Dasher

# use three columns for the widgets, turn credits off
app = Dasher(
    __name__,
    title="Customization example",
    layout_kw={"widget_cols": 3, "credits": False},
)

# custom component
creatures = dbc.Checklist(
    options=[
        {"label": "Dragon", "value": "a Dragon"},
        {"label": "Orc", "value": "an Orc"},
        {"label": "Ogre", "value": "an Ogre"},
        {"label": "Troll", "value": "a Troll"},
        {"label": "Necromancer", "value": "a Necromancer"},
    ],
    value=[],
    switch=True,
)

# custom component with custom dependency
heros = CustomWidget(
    dbc.Button("Add a hero", block=True, color="primary", n_clicks=2),
    dependency="n_clicks",
)


@app.callback(
    _name="My custom fantasy story",
    _labels=["Story format", "Number of heros", "The creatures to fight"],
    fmt=["Tale", "Book", "Song"],
    heros=heros,
    creatures=creatures,
)
def my_story(fmt, heros, creatures):
    story = f"A {fmt} about {heros} heros fighting "

    if len(creatures) == 0:
        suffix = "a mouse."
    elif len(creatures) == 1:
        suffix = f" {creatures[0]}."
    else:
        suffix = ", ".join(creatures[:-1]) + f" and {creatures[-1]}."

    return [html.P(story + suffix)]


# local layout override to have two widget columns
@app.callback(
    _name="My custom tab",
    _layout_kw={"widget_cols": 2},
    one="local",
    two="layout",
    three="override",
)
def my_custom_tab(one, two, three):
    return [html.P(f"one: {one}, two: {two}, three: {three}")]


# add a custom icon into the navbar
app.api.layout.navbar.children = [
    dbc.NavItem(
        html.Img(
            src="https://www.python.org/static/community_logos/python-powered-w.svg",
            style={"float": "right", "height": "50px"},
        )
    )
]

if __name__ == "__main__":
    app.run_server(debug=True)
