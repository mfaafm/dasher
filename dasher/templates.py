from abc import ABC, abstractmethod
import dash_html_components as html
from dash.dependencies import Input, Output


class DasherBaseTemplate(ABC):
    @classmethod
    @abstractmethod
    def generate_layout(cls, widget_list):
        pass

    @classmethod
    @abstractmethod
    def generate_connections(cls, kw):
        pass


class DasherSimpleTemplate(DasherBaseTemplate):
    widget_div_name = "dasher-widget-div"
    output_div_name = "dasher-output-div"

    @classmethod
    def generate_layout(cls, widget_list):
        widget_div = html.Div(
            widget_list, id=cls.widget_div_name, style={"marginBottom": 50}
        )
        output_div = html.Div(id=cls.output_div_name)
        return html.Div([widget_div, output_div])

    @classmethod
    def generate_connections(cls, kw):
        input_list = [
            Input(component_id=name, component_property="value") for name in kw.keys()
        ]
        output = Output(
            component_id=cls.output_div_name, component_property="children"
        )
        return output, input_list
