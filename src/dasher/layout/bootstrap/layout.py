import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from dasher.base import BaseLayout
from .widgets import WIDGET_SPEC


class BootstrapLayout(BaseLayout):
    """ Dasher boostrap layout.
    This layout utilizes ``dash_bootstrap_components`` to build the app layout.

    Parameters
    ----------
    title: str
        Title of the app.
    widget_spec: OrderedDict, optional
        Widget specification.
        Default: ``dasher.layout.bootstrap.widgets.WIDGET_SPEC``.
    credits: bool, optional
        If true, shows a link to dasher's github page in the navigation bar.
        Default: True.
    include_stylesheets: bool, optional
        If true, includes the standard bootstrap theme as external stylesheets. Set
        it to false to use a customized bootstrap theme. Default: True.
    widget_cols: int, optional
        Group the interactive components into ``widget_cols`` number of columns.
        Default: 2.

    Attributes
    ----------
    widget_cols: int
        Group the interactive components into ``widget_cols`` number of columns.
    include_stylesheets: bool
        If true, includes the standard bootstrap theme as external stylesheets.
    external_stylesheets: list of str, optional
        Only present of `include_stylesheets` is ``True``. It contains a list with
        the standard bootstrap theme as its' only value.
    navbar: dash_bootstrap_components.NavbarSimple
        Navigation bar of the layout.
    body: dash_bootstrap_components.Container
        Container for the body of the app, containing the tab control and the tab
        contents div.
    layout: dash_html_components.Div
        Layout of the app. The div contains `navbar` and `body`.
    tabs: dash_bootstrap_components.Tabs
        Tab control to separate the layout of the callbacks.
    tabs_content: dash_html_components.Div
        Content div used to render the selected tab.
    callbacks: dict of DasherCallback
        Dictionary containing the callbacks present in the layout.
    """

    navbar_id = "dasher-navbar"
    body_id = "dasher-body"
    tabs_id = "dasher-tabs"
    tabs_content_id = "dasher-tabs-content"
    tab_base = "dasher-tab"
    widgets_base = "dasher-widgets"

    def __init__(
        self,
        title,
        widget_spec=WIDGET_SPEC,
        credits=True,
        include_stylesheets=True,
        widget_cols=2,
    ):
        super().__init__(title, widget_spec, credits)

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
        """ Create base layout with navigation bar and body container. """
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
        """ Renders a card with the interactive components and the output container.

        Parameters
        ----------
        callback: dasher.base.Callback
            The callback to render the card for.

        **kwargs:
             Keyword arguments to override default layout settings.

        Returns
        -------
        dash_bootstrap_components.Card
            Layout of the card.
        """
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

    def add_callback(self, callback, app, **kwargs):
        """ Add callback to the layout.

        Parameters
        ----------
        callback: DasherCallback
            The dasher callback to add to the layout.
        app: dash.Dash
            The dash app.
        **kwargs:
           Keyword arguments to override default layout settings for a callback.
        """
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

        content = self.render_card(callback, **kwargs)

        self.callbacks[callback.name] = callback
        callback.layout = content

    def render_callback(self, name):
        """ Callback method to switch between tabs.

        Parameters
        ----------
        name: str
            Name of the callback to render.

        Returns
        -------
        dash.development.base_component.Component
            Layout of the callback.
        """
        return self.callbacks[name].layout
