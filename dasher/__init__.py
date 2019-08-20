import dash
from dasher.base import DasherBaseTemplate, DasherBaseWidgetFactory, DasherCallback
from dasher.api import DasherApi
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

    def __init__(self, name, title=None, template=DasherStandardTemplate(), **kw):
        if not isinstance(template, DasherBaseTemplate):
            raise ValueError("template must be an instance of DasherBaseTemplate")
        self.template = template
        if title is not None:
            self.template.title = title
        self.api = DasherApi()
        self.callback_list = []

        ext_stylesheets = kw.get("external_stylesheets", [])
        kw["external_stylesheets"] = self._update_stylesheets(ext_stylesheets)
        self.app = dash.Dash(name, **kw)

    def _update_stylesheets(self, *args):
        ext_stylesheets = self.template.external_stylesheets.copy()
        ext_stylesheets.extend(args)
        return ext_stylesheets

    def callback(self, _name, _desc=None, _labels=None, **kw):
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
        _labels: list or dict, default: None
            Labels for the widgets. May be either a list of labels for the keywords
            ``**kw`` in the order of appearance or a dictionary mapping keywords to the
            desired labels. If ``None``, the keywords are used for the labels directly.
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
            widgets = self.api.generate_widgets(kw, _labels, _name)
            outputs, inputs = self.api.generate_dependencies(
                widgets, f"dasher-output-{_name}"
            )
            callback = DasherCallback(
                name=_name,
                description=_desc,
                f=f,
                kw=kw,
                labels=_labels,
                widgets=widgets,
                outputs=outputs,
                inputs=inputs,
            )
            self.callback_list.append(callback)
            self.app.layout = self.template.update_layout(
                self.app.layout, self.callback_list
            )
            return self.api.register_callback(self.app, callback)

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
