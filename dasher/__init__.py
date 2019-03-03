import dash
from dasher.base import DasherBaseTemplate, DasherBaseWidgetFactory, DasherCallback
from dasher.widgets import DasherWidgetFactory
from dasher.templates import DasherSimpleTemplate


class Dasher(object):
    def __init__(
        self,
        name,
        template=DasherSimpleTemplate,
        widget_factory=DasherWidgetFactory,
        **kw
    ):
        self.app = dash.Dash(name, **kw)
        if not issubclass(template, DasherBaseTemplate):
            raise ValueError("template must be a subclass of DasherBaseTemplate")
        self.template = template
        if not issubclass(widget_factory, DasherBaseWidgetFactory):
            raise ValueError("widgets must be a subclass of DasherBaseWidgetFactory")
        self.widget_factory = widget_factory
        self.callback_list = []

    @staticmethod
    def get_widget_name(key, id):
        return "{}-{}".format(key, id)

    def generate_widgets(self, id, kw):
        widget_list = []
        for key, value in kw.items():
            name = self.get_widget_name(key, id)
            widget = self.widget_factory.create_widget(name, key, value)
            if widget is None:
                raise ValueError("Cannot generate a widget for keyword {}".format(key))
            widget_list.append(widget)
        return widget_list

    def callback(self, **kw):
        def function_wrapper(f):
            id = len(self.callback_list)
            new_callback = DasherCallback(id, kw, self.generate_widgets(id, kw))
            self.callback_list.append(new_callback)
            self.app.layout = self.template.update_layout(
                self.app.layout, self.callback_list
            )
            output, input_list = self.template.generate_connections(new_callback)
            return self.app.callback(output, input_list)(f)

        return function_wrapper

    def run_server(self, *args, **kw):
        return self.app.run_server(*args, **kw)
