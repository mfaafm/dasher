import dash
import functools
import dash_html_components as html
from dash.dependencies import Input, Output
from widgets import Widgets


class Dasher(object):
    def __init__(self, name, **kw):
        self.app = dash.Dash(name, **kw)
        self.widgets = Widgets
        self.widget_div_name = "dasher-widget-div"
        self.output_div_name = "dasher-output-div"

    def _generate_widgets(self, kw):
        widgets = []
        for name, value in kw.items():
            label = html.Label(name)
            widget = self.widgets.choose_widget(name, value)
            if widget is None:
                raise ValueError(
                    "Cannot find suitable widget for keyword {}".format(name)
                )
            widgets.extend((label, widget))
        return widgets

    def _create_layout(self, widgets):
        widget_div = html.Div(
            widgets, id=self.widget_div_name, style={"marginBottom": 50}
        )
        output_div = html.Div(id=self.output_div_name)
        self.app.layout = html.Div([widget_div, output_div])

    # def callback(self, f, **kw):
    #
    #     widgets = self._generate_widgets(kw)
    #     self._create_layout(widgets)
    #
    #     input_list = [
    #         Input(component_id=name, component_property="value") for name in kw.keys()
    #     ]
    #     output = Output(
    #         component_id=self.output_div_name, component_property="children"
    #     )
    #     return self.app.callback(output, input_list)(f)

    def callback(self, **kw):
        def function_wrapper(f):
            widgets = self._generate_widgets(kw)
            self._create_layout(widgets)

            input_list = [
                Input(component_id=name, component_property="value") for name in kw.keys()
            ]
            output = Output(
                component_id=self.output_div_name, component_property="children"
            )
            return self.app.callback(output, input_list)(f)
        return function_wrapper

    def run_server(self, *args, **kw):
        return self.app.run_server(*args, **kw)
