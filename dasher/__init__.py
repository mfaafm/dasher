import dash
from dasher.base import DasherBaseTemplate, DasherBaseWidgetFactory, DasherCallback
from dasher.widgets import DasherWidgetFactory
from dasher.templates import DasherStandardTemplate

# get version from versioneer
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


class Dasher(object):
    """ Dasher app.

    Parameters
    ----------
    name: str
        Name of the app, typically ``__name__``.
    title: str
        Title of the dashboard.
    template: DasherBaseTemplate, default: templates.DasherStandardTemplate()
        Instance of dashboard template. Must be inherited from
        ``DasherBaseTemplate``.
    widget_factory: DasherBaseWidgetFactory, default: widgets.DasherWidgetFactory()
        Instance of widget factory. Must be inherited from
        ``DasherBaseWidgetFactory``.
    kw
        Keyword arguments are passed to the ``dash.Dash`` app.
    """
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
    def _get_widget_name(key, _id):
        return "{}-{}".format(key, _id)

    def _generate_widgets(self, _id, kw):
        widget_list = []
        for key, value in kw.items():
            name = self._get_widget_name(key, _id)
            widget = self.widget_factory.create_widget(name, key, value)
            if widget is None:
                raise ValueError("Cannot generate a widget for keyword {}".format(key))
            widget_list.append(widget)
        return widget_list

    def callback(self, _name, _desc=None, **kw):
        """
        Decorator, which defines a callback function.
        Each callback function results in a tab in the dashboard. The keywords arguments
        are the input arguments of the callback function. Simultaneously, the types of
        each keyword defines which interactive widget is generated for the dashboard.

        The supported widget types is defined by the widget factory.

        Parameters
        ----------
        _name: str
            Name of the callback.
        _desc: str, default: None
            Optional description of the callback.
        kw
            Keyword arguments that are the input arguments to the callback function,
            which also define the widgets that are generated for the dashboard.
            Reserved keywords are ``_name`` and ``_desc``, which cannot be used.

        Returns
        -------
        function_wrapper: callable
            Wrapped function that generates a dashboard tab.

        See Also
        --------
        widgets.DasherWidgetFactory : Default widget factory

        """
        def function_wrapper(f):
            callback_id = len(self.callback_list)
            widget_list = self._generate_widgets(callback_id, kw)
            new_callback = DasherCallback(callback_id, _name, _desc, kw, widget_list)
            self.callback_list.append(new_callback)
            self.app.layout = self.template.update_layout(
                self.app.layout, self.callback_list
            )
            output, input_list = self.template.generate_connections(new_callback)
            return self.app.callback(output, input_list)(f)

        return function_wrapper

    def run_server(self, *args, **kw):
        """
        Runs the dasher app server by calling the underlying ``dash.Dash.run_server``
        method. Refer to the documentation of ``dash.Dash.run_server`` for details.

        Parameters
        ----------
        args
            Positional arguments passed to ``dash.Dash.run_server``.
        kw
            Keyword arguments passed to ``dash.Dash.run_server``.

        Returns
        -------

        """
        return self.app.run_server(*args, **kw)
