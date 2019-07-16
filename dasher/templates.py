import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dasher.base import DasherBaseTemplate


class DasherStandardTemplate(DasherBaseTemplate):
    """ Default template of dasher.

    Parameters
    ----------
    title: str
        Title of the dashboard. Shown in the header (navbar).
    widget_columns: int, default: 2
        Number of columns used to arrange the interactive widgets of the dashboard.
    """

    navbar_id = "dasher-navbar"
    tabs_id = "dasher-tabs"
    body_id = "dasher-body"
    main_name = "dasher-main"
    tab_base = "dasher-tab"
    output_base = "dasher-output"

    def __init__(self, title="Dasher dashboard", widget_columns=2, credits=True):
        self.__title = title
        if widget_columns < 1:
            raise ValueError("widget_columns must be >= 1")
        self.widget_columns = widget_columns

        self.external_stylesheets = [dbc.themes.BOOTSTRAP]
        self.tabs = None
        self.credits = credits
        self.navbar, self.body = self._create_base_layout()

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title
        self.navbar.brand = title

    @staticmethod
    def _get_div_name(base, _id):
        return "{}-{}".format(base, _id)

    def _create_base_layout(self):
        navbar = dbc.NavbarSimple(
            brand=self.title,
            dark=True,
            color="primary",
            sticky="top",
            id=self.navbar_id,
            style={"marginBottom": "1em"},
        )
        if self.credits:
            credit = dbc.NavLink(
                "created with dasher",
                className="small",
                href="https://github.com/mfaafm/dasher",
                external_link=True,
            )
            navbar.children = [credit]

        body = dbc.Container([], id=self.body_id)
        return navbar, body

    @staticmethod
    def _create_form_group(widget):
        return dbc.FormGroup(
            [
                dbc.Label(widget.label, html_for=widget.dash_component.id),
                widget.dash_component,
            ]
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

    def _create_form(self, callback):
        cols = [dbc.Col(self._create_form_group(w)) for w in callback.widget_list]
        rows = [dbc.Row(row) for row in self._chunks(cols, self.widget_columns)]
        return dbc.Form(rows)

    def _create_output(self, callback):
        output_id = self._get_div_name(self.output_base, callback.id)
        return html.Div(id=output_id)

    def _create_card(self, callback):
        form = self._create_form(callback)
        output = self._create_output(callback)

        card_header = dbc.CardHeader(callback.name)
        card_body = dbc.CardBody([form, output])
        card = dbc.Card([card_header, card_body])

        if callback.description is not None:
            card_title = html.H4(callback.description, className="card-title")
            card_body.children.insert(0, card_title)
        return card

    def _create_tab(self, callback, card):
        tab_id = self._get_div_name(self.tab_base, callback.id)
        return dbc.Tab(card, id=tab_id, label=callback.name)

    def update_layout(self, layout, callback_list):
        n_callbacks = len(callback_list)
        callback = callback_list[-1]

        if n_callbacks == 1:
            card = self._create_card(callback)
            self.body.children.extend([card])
            return html.Div([self.navbar, self.body], id=self.main_name)
        elif n_callbacks == 2:
            tab_0 = self._create_tab(callback_list[-2], self.body.children)
            tab_1 = self._create_tab(callback, self._create_card(callback))
            self.tabs = dbc.Tabs([tab_0, tab_1], id=self.tabs_id)
            self.body.children = self.tabs
            return layout
        else:
            card = self._create_card(callback)
            self.tabs.children.append(self._create_tab(callback, card))
            return layout

    def generate_connections(self, callback):
        input_list = [
            Input(component_id=w.name, component_property="value")
            for w in callback.widget_list
        ]
        output = Output(
            component_id=self._get_div_name(self.output_base, callback.id),
            component_property="children",
        )
        return output, input_list
