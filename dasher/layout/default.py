import dash_bootstrap_components as dbc
import dash_html_components as html
from dasher.base import DasherLayout
from dash.dependencies import Input, Output


class DefaultLayout(DasherLayout):
    navbar_id = "dasher-navbar"
    body_id = "dasher-body"
    tabs_id = "dasher-tabs"
    tabs_content_id = "dasher-tabs-content"
    tab_base = "dasher-tab"
    widgets_base = "dasher-widgets"
    output_base = "dasher-output"

    def __init__(self, title, credits=True, include_stylesheets=True, widget_cols=2):
        super().__init__(title, credits)

        if widget_cols < 1:
            raise ValueError("widget_cols must be >= 1")
        self.widget_cols = widget_cols
        if include_stylesheets:
            self.external_stylesheets = [dbc.themes.BOOTSTRAP]
        self.navbar, self.body = self.render_base_layout()
        self.layout = html.Div([self.navbar, self.body])
        self.tabs = None
        self.tabs_content = None
        self.callbacks = {}

    def render_base_layout(self):
        navbar = dbc.NavbarSimple(
            brand=self.title,
            dark=True,
            color="primary",
            sticky="top",
            id=self.navbar_id,
            style={"marginBottom": "1em"},
        )

        body = dbc.Container([], id=self.body_id)

        if self.credits:
            credit = dbc.NavLink(
                "created with dasher",
                className="small",
                href="https://github.com/mfaafm/dasher",
                external_link=True,
            )
            navbar.children = [credit]
        return navbar, body

    @staticmethod
    def render_component(label, component):
        return dbc.FormGroup(
            [dbc.Label(label, html_for=component.name), component.layout]
        )

    @staticmethod
    def _chunks(l, n):
        """ Yield successive n-sized chunks from l.

        Parameters
        ----------
        l: iterable
            Iterable to slice into chunks.
        n: int
            Maximum size of each chunk.
        """
        for i in range(0, len(l), n):
            yield l[i : i + n]

    def render_card(self, callback, **kwargs):
        widget_cols = kwargs.get("widget_cols", self.widget_cols)

        cols = [dbc.Col(w.layout) for w in callback.widgets]
        rows = [dbc.Row(row) for row in self._chunks(cols, widget_cols)]
        widgets_form = dbc.Form(rows, id=f"{self.widgets_base}-{callback.name}")

        output = dbc.Container(
            id=f"{self.output_base}-{callback.name}", style={"marginTop": "1em"}
        )

        card_header = dbc.CardHeader(callback.name)
        card_body = dbc.CardBody([widgets_form, output])
        if callback.description is not None:
            card_title = html.H4(callback.description, className="card-title")
            card_body.children.insert(0, card_title)
        return dbc.Card([card_header, card_body])

    def add_callback(self, callback, app, layout_kw=None):
        if layout_kw is None:
            layout_kw = {}

        tab = dbc.Tab(label=callback.name, tab_id=callback.name)

        if len(self.callbacks) == 0:
            self.tabs = dbc.Tabs(
                children=[],
                id=self.tabs_id,
                active_tab=tab.tab_id,
                style={"display": "none"},
            )
            self.tabs_content = html.Div(id=self.tabs_content_id)
            self.body.children.extend((self.tabs, self.tabs_content))
            app.callback(
                Output(self.tabs_content.id, "children"),
                [Input(self.tabs.id, "active_tab")],
            )(self.render_callback)
        elif len(self.callbacks) == 1:
            del self.tabs.style["display"]

        self.tabs.children.append(tab)

        content = self.render_card(callback, **layout_kw)

        self.callbacks[callback.name] = callback
        callback.layout = content

    def render_callback(self, name):
        return self.callbacks[name].layout
