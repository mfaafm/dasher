from abc import ABC, abstractmethod
from collections import OrderedDict


class BaseWidget(ABC):
    """ Abstract base class of a dasher widget.
    A dasher widget is an interactive control, which consists of an interactive dash
    `component`, a `label` and a final `layout`.

    Attributes
    ----------
    name: str
        Name of the widget.
    x: object
        The object, whose type determines the type of the widget.
    component: DasherComponent
        The interactive dash component.
    label: str
        The label for the dash component.
    layout: dash.development.base_component.Component
        The `layout` is a styled and labeled version of `component`.
    dependency: str, optional
        The attribute used for the ``dash.dependencies.Input`` dependency.
        Default: "value".
    """
    def __init__(self, name, x, label=None, dependecy="value"):
        """

        Parameters
        ----------
        name
        x
        label
        dependecy
        """
        self.name = name
        self.x = x
        self.label = label if label is not None else name
        self.dependency = dependecy

    @property
    @abstractmethod
    def component(self):
        """ Abstract property. The implementation of the getter method in the child
        class must return the concrete component.

        Returns
        -------
        dash.development.base_component.Component
            Generated dash component.
        """
        pass

    @property
    @abstractmethod
    def layout(self):
        """ Abstract property. The implementation of the getter method in the child
        class must return the final layout of the widget.

        Returns
        -------
        dash.development.base_component.Component
            Generated dash component.
        """
        pass


class WidgetPassthroughMixin(BaseWidget, ABC):
    """ Passthrough mixin to support custom dash components. """

    @property
    def component(self):
        if getattr(self.x, "id", None) is None:
            self.x.id = self.name
        else:
            raise ValueError("Component id must be empty.")
        return self.x


class BaseLayout(ABC):
    """ Abtract base class of a dasher layout, which is responsible for creating the
    layout of the dasher app.

    The widget specification (`widget_spec`) is used to determine the types and the
    layout of the automatically generated interactive widgets.

    A layout class also handles the addition of callbacks via the `add_callback` method
    and creates a suitable form of separation between the callbacks in the app layout.
    The standard way to do this is to generate a separate tab for each callback.

    A child class must implement the abtract `add_callback` method and create the final
    app layout as its' ``layout`` attribute. If the layout needs external stylesheets,
    the child class must announce this by creating an `external_stylesheets` attribute
    containing the list of required external stylesheets.

    Attributes
    ----------
    title: str
        Title of the dash app.
    credits: bool
        If true, dasher / layout credits are shown in the app.
    layout: list of dash.development.base_component.Component
        The final app layout (is assigned to the ``layout`` property of the dash app).
    """

    output_base = "dasher-output"

    def __init__(self, title, widget_spec, credits=True):
        """
        Parameters
        ----------
        title: str
            Title of the dash app.
        widget_spec: OrderedDict
            Widget specification used to determine the types of the interactive widgets.
        credits: bool
            If true, dasher / layout credits are shown in the app.
        """
        if title is None:
            self.title = "Dasher app"
        else:
            self.title = title

        if not isinstance(widget_spec, OrderedDict):
            raise ValueError(
                "widget_spec must be an OrderedDict containing a widget specification."
            )
        self.widget_spec = widget_spec

        self.credits = credits

    @abstractmethod
    def add_callback(self, callback, app, **kwargs):
        """ The implementation must handle the addition of callbacks to the layout and
        provide a suitable form of separation between the callbacks in the app layout.
        The standard way to do this is to generate a separate tab for each callback.

        Parameters
        ----------
        callback: Callback
            The callback to add to the layout.
        app: dash.Dash
            The dash app.
        **kwargs:
           Keyword arguments to override default layout settings for a callback.
        """
        pass


class Callback(object):
    """ This class contains the specification of a callback.

    Attributes
    ----------
    name: str
        Name of the callback.
    description: str or None
        Additional description of the callback.
    f: callable
        The callback function itself.
    kw: dict
        The keyword arguments passed to the ``callback`` decorator.
    labels: list or dict or None
        Labels for the widgets.
    widgets: list of BaseWidget
        Generated dasher widgets for the callback.
    outputs: dash.dependencies.Output or list of dash.dependencies.Output
        Output dependencies for the callback.
    inputs: list of dash.dependencies.Input
        Input dependencies for the callback.
    layout_kw: dict or None
        Keyword arguments to override default layout settings for the callback.
    """

    def __init__(
        self, name, description, f, kw, labels, widgets, outputs, inputs, layout_kw
    ):
        """
        Parameters
        ----------
        name: str
            Name of the callback.
        description: str or None
            Additional description of the callback.
        f: callable
            The callback function itself.
        kw: dict
            The keyword arguments passed to the ``callback`` decorator.
        labels: list or dict or None
            Labels for the widgets.
        widgets: list of BaseWidget
            Generated dasher widgets for the callback.
        outputs: dash.dependencies.Output or list of dash.dependencies.Output
            Output dependencies for the callback
        inputs: list of dash.dependencies.Input
            Input dependencies for the callback
        layout_kw: dict or None
            Keyword arguments to override default layout settings for the callback.
        """
        self.name = name
        self.description = description
        self.f = f
        self.kw = kw
        self.labels = labels
        self.widgets = widgets
        self.outputs = outputs
        self.inputs = inputs
        self.layout_kw = layout_kw
