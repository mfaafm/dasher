import dash
from copy import deepcopy
from .base import Callback
from .api import Api


class Dasher(object):
    """ Dasher app.
    Allows building of simple, interactive dash apps with minimal effort.
    A tab is created by decorating a callback function, which returns the content layout
    in the form of a list of dash components. Interactive widgets to control the
    arguments of the callback function are generated automatically. The type of
    widgets are determined based on the types of the keyword arguments (compatible to
    the ``ipywidgets.interact`` decorator).

    Parameters
    ----------
    name: str
        Name of the app, typically `__name__`.
    title: str, optional
        Title of the app.
    layout: str or DasherLayout subclass, optional
        Name of a built-in layout or custom layout (DasherLayout subclass)
    layout_kw: dict, optional
        Dictionary of keyword arguments passed to the `layout` class.
    dash_kw: dict, optional
        Dictionary of keyword arguments passed to the dash app.

    Attributes
    ----------
    api: dasher.Api
        The ``dasher.Api`` instance used for generating the app.
    app: dash.Dash
        The dash app.
    callbacks: dict of Callback
        Dictionary containing the registered callbacks.
    """

    def __init__(
        self, name, title=None, layout="bootstrap", layout_kw=None, dash_kw=None
    ):
        self.api = Api(title, layout, layout_kw)

        if dash_kw is None:
            dash_kw = {}
        dash_kw = self._update_external_stylesheets(dash_kw)
        self.app = dash.Dash(name, suppress_callback_exceptions=True, **dash_kw)

        self.app.layout = self.api.layout.layout
        self.callbacks = {}

    def _update_external_stylesheets(self, dash_kw):
        kw = deepcopy(dash_kw)
        layout_sheets = getattr(self.api.layout, "external_stylesheets", [])
        kw["external_stylesheets"] = layout_sheets + kw.get("external_stylesheets", [])
        return kw

    def callback(self, _name, _desc=None, _labels=None, _layout_kw=None, **kwargs):
        """ Decorator, which defines a callback function.
        Each callback function results in a tab in the app. The keywords arguments
        are the input arguments of the callback function. Simultaneously, the types of
        each keyword defines which interactive widgets are generated for the tab.

        The decorated callback function must return a list of dash components. It
        defines the content of the tab, which is controlled by the generated interactive
        widgets.

        Supported widget types are determined by the layouts' widget specification. The
        built-in widget specifications are compatible with ``ipywidgets.interact``
        and support the following types, which generate the corresponding widgets:

        * ``bool``: Boolean choice / Radio Items
        * ``str``: Input field
        * ``int``: Slider, integer
        * ``float``: Slider, floats
        * ``tuple``: Slider
          Can be (min, max) or (min, max, step). The type of all the tuple entries
          must either be ``int`` or ``float``, which determines whether an integer or
          float slider will be generated.
        * ``collections.Iterable``: Dropdown menu
          Typically a ``list`` or anything iterable.
        * ``collections.Mapping``: Dropdown menu
          Typically a ``dict``. A mapping will use the keys as labels shown in the
          dropdown menu, while the values will be used as arguments to the callback
          function.
        * ``dash.development.base_component.Component``: custom dash component
          Any dash component will be used as-is. This allows full customization of a
          widget if desired. The components ``value`` will be used as argument to
          the callback function.

        Parameters
        ----------
        _name: str
            Name of the callback.
        _desc: str, optional
            Optional description of the callback.
        _labels: list or dict, optional
            Labels for the widgets. May be either a list of labels for the keywords
            `**kwargs` in the order of appearance or a dictionary mapping keywords to
            the desired labels. If ``None``, the keywords are used for the labels
            directly.
        _layout_kw: dict, optional
            Dictionary of keyword arguments passed to the ``add_callback`` method of the
            layout, which may be used to override layout defaults for individual
            callbacks.
        kwargs
            Keyword arguments that are the input arguments to the callback function,
            which also define the widgets that are generated for the dashboard.
            Obviously, reserved keywords are `_name`, `_desc`, `_labels` and `_layout`.

        Returns
        -------
        function_wrapper: callable
            Wrapped function that generates a dashboard tab.

        See Also
        --------
        layout.bootstrap.widgets.WIDGET_SPEC: Bootstrap widget specification
        layout.bootstrap.layout.BootstrapLayout: Bootstrap layout

        """

        def function_wrapper(f):
            layout = _layout_kw if _layout_kw is not None else {}

            widgets = self.api.generate_widgets(kwargs, _labels, _name)
            outputs, inputs = self.api.generate_dependencies(
                widgets, f"{self.api.layout.output_base}-{_name}"
            )

            callback = Callback(
                name=_name,
                description=_desc,
                f=f,
                kw=kwargs,
                labels=_labels,
                widgets=widgets,
                outputs=outputs,
                inputs=inputs,
                layout_kw=_layout_kw,
            )
            self.callbacks[callback.name] = callback

            self.api.layout.add_callback(callback, self.app, **layout)
            return self.api.register_callback(self.app, callback)

        return function_wrapper

    def get_flask_server(self):
        """ Returns the flask app object. """
        return self.app.server

    def run_server(self, *args, **kw):
        """ Runs the dasher app server by calling the underlying ``dash.Dash.run_server``
        method. Refer to the documentation of ``dash.Dash.run_server`` for details.

        Parameters
        ----------
        args
            Positional arguments passed to ``dash.Dash.run_server``.
        kw
            Keyword arguments passed to ``dash.Dash.run_server``.
        """
        return self.app.run_server(*args, **kw)
