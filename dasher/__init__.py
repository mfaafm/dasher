import dash
from dasher.base import DasherBaseTemplate, DasherBaseWidgetFactory, DasherCallback
from dasher.widgets import DasherWidgetFactory
from dasher.templates import DasherStandardTemplate


class Dasher(object):
    def __init__(
        self,
        name,
        title=None,
        template=DasherStandardTemplate(),
        widget_factory=DasherWidgetFactory(),
        **kw
    ):
        if not isinstance(template, DasherBaseTemplate):
            raise ValueError("template must be an instance of DasherBaseTemplate")
        self.template = template
        if title is not None:
            self.template.title = title
        if not isinstance(widget_factory, DasherBaseWidgetFactory):
            raise ValueError("widgets must be an instance of DasherBaseWidgetFactory")
        self.widget_factory = widget_factory
        self.callback_list = []

        ext_stylesheets = kw.get("external_stylesheets", [])
        kw["external_stylesheets"] = self._update_stylesheets(ext_stylesheets)
        self.app = dash.Dash(name, **kw)

    def _update_stylesheets(self, *args):
        ext_stylesheets = self.template.external_stylesheets.copy()
        ext_stylesheets.extend(args)
        return ext_stylesheets

    @staticmethod
    def get_widget_name(key, _id):
        return "{}-{}".format(key, _id)

    def generate_widgets(self, _id, kw):
        widget_list = []
        for key, value in kw.items():
            name = self.get_widget_name(key, _id)
            widget = self.widget_factory.create_widget(name, key, value)
            if widget is None:
                raise ValueError("Cannot generate a widget for keyword {}".format(key))
            widget_list.append(widget)
        return widget_list

    def callback(self, _name, _desc=None, **kw):
        def function_wrapper(f):
            callback_id = len(self.callback_list)
            widget_list = self.generate_widgets(callback_id, kw)
            new_callback = DasherCallback(callback_id, _name, _desc, kw, widget_list)
            self.callback_list.append(new_callback)
            self.app.layout = self.template.update_layout(
                self.app.layout, self.callback_list
            )
            output, input_list = self.template.generate_connections(new_callback)
            return self.app.callback(output, input_list)(f)

        return function_wrapper

    def run_server(self, *args, **kw):
        return self.app.run_server(*args, **kw)
