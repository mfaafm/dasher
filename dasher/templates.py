import dash_html_components as html
from dash.dependencies import Input, Output
from dasher.base import DasherBaseTemplate


class DasherSimpleTemplate(DasherBaseTemplate):
    main_div_name = "dasher-main-div"
    callback_div_base = "dasher-callback-div"
    widget_div_base = "dasher-widget-div"
    output_div_base = "dasher-output-div"

    @staticmethod
    def _get_div_name(base, id):
        return "{}-{}".format(base, id)

    @classmethod
    def update_layout(cls, layout, callback_list):
        callback = callback_list[-1]
        widget_div_name = cls._get_div_name(cls.widget_div_base, callback.id)
        output_div_name = cls._get_div_name(cls.output_div_base, callback.id)
        callback_div_name = cls._get_div_name(cls.callback_div_base, callback.id)
        dash_widgets = [w.dash_component for w in callback.widget_list]
        widget_div = html.Div(
            dash_widgets, id=widget_div_name, style={"marginBottom": 50}
        )
        output_div = html.Div(id=output_div_name)
        callback_div = html.Div([widget_div, output_div], id=callback_div_name)

        if callback.id == 0:
            main_div = html.Div([callback_div], id=cls.main_div_name)
            return main_div
        else:
            layout.children.append(callback_div)
            return layout

    @classmethod
    def generate_connections(cls, callback):
        input_list = [
            Input(component_id=w.name, component_property="value")
            for w in callback.widget_list
        ]
        output = Output(
            component_id=cls._get_div_name(cls.output_div_base, callback.id),
            component_property="children",
        )
        return output, input_list
