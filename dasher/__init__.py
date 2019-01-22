import dash
from dasher.widgets import DasherWidgets, DasherBaseWidgets
from dasher.templates import DasherSimpleTemplate, DasherBaseTemplate


class Dasher(object):
    def __init__(
        self, name, template=DasherSimpleTemplate, widget_factory=DasherWidgets, **kw
    ):
        self.app = dash.Dash(name, **kw)
        if not issubclass(template, DasherBaseTemplate):
            raise ValueError("template must be a subclass of DasherBaseTemplate")
        self.template = template
        if not issubclass(widget_factory, DasherBaseWidgets):
            raise ValueError("widgets must be a subclass of DasherBaseWidgets")
        self.widget_factory = widget_factory

    def generate_widgets(self, kw):
        widget_list = []
        for name, value in kw.items():
            widget = self.widget_factory.create_widget(name, value)
            if widget is None:
                raise ValueError("Cannot get a widget for keyword {}".format(name))
            widget_list.append(widget)
        return widget_list

    def callback(self, **kw):
        def function_wrapper(f):
            widget_list = self.generate_widgets(kw)
            self.app.layout = self.template.generate_layout(widget_list)
            output, input_list = self.template.generate_connections(kw)
            return self.app.callback(output, input_list)(f)
        return function_wrapper

    def run_server(self, *args, **kw):
        return self.app.run_server(*args, **kw)
