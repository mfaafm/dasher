import dash
from dasher.base import DasherBaseTemplate, DasherBaseWidgetFactory, DasherCallback
from dasher.widgets import DasherWidgetFactory
from dasher.templates import DasherStandardTemplate
from collections.abc import Sequence, Mapping

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

    @staticmethod
    def _validate_labels(_labels, kw):
        if isinstance(_labels, Sequence) and len(_labels) != len(kw):
            raise ValueError("_labels must be of same length as kw")

    @staticmethod
    def _create_labels(_labels, kw):
        if _labels is None:
            return {k: k for k in kw.keys()}
        elif isinstance(_labels, Sequence):
            if len(_labels) != len(kw):
                raise ValueError("_labels must be of same length as kw")
            return {k: l for k, l in zip(kw.keys(), _labels)}
        elif isinstance(_labels, Mapping):
            return {k: _labels.get(k, k) for k in kw.keys()}
        else:
            return ValueError("_labels must be list-like, dict-like or None")

    def _generate_widgets(self, _id, labels, kw):
        widget_list = []
        for key, value in kw.items():
            name = self._get_widget_name(key, _id)
            widget = self.widget_factory.create_widget(name, labels[key], value)
            if widget is None:
                raise ValueError("Cannot generate a widget for keyword {}".format(key))
            widget_list.append(widget)
        return widget_list

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
        labels = self._create_labels(_labels, kw)

        def function_wrapper(f):
            callback_id = len(self.callback_list)
            widget_list = self._generate_widgets(callback_id, labels, kw)
            new_callback = DasherCallback(
                callback_id, _name, _desc, kw, widget_list, labels
            )
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
