from collections.abc import Mapping
from collections.abc import Sequence

from dash.dependencies import Input
from dash.dependencies import Output

from dasher.base import BaseLayout
from dasher.base import generate_callback_id


class Api(object):
    """ Dasher api.
    The api allows generation of widgets and dash dependencies (for
    instances of ``DasherCallback``). It is used by ``Dasher`` to generate interactive
    apps.

    Parameters
    ----------
    title: str, optional
        Title of the app.
    layout: str or DasherLayout subclass, optional
        Name of a built-in layout or custom layout (DasherLayout subclass)
    layout_kw: dict, optional
        Dictionary of keyword arguments passed to the `layout` class.
    """

    def __init__(self, title=None, layout="bootstrap", layout_kw=None):
        if layout_kw is None:
            layout_kw = {}
        self.layout = self._load_layout(layout)(title, **layout_kw)

    @staticmethod
    def _load_layout(layout):
        if layout == "bootstrap":
            from dasher.layout.bootstrap import BootstrapLayout

            return BootstrapLayout
        elif issubclass(layout, BaseLayout):
            return layout
        else:
            msg = "layout must be either a named layout or a subclass of DasherLayout"
            raise ValueError(msg)

    def generate_widget(self, name, x, label=None):
        """ Generate a dasher widget, which is a styled and labeled interactive
        component.

        The type of the interactive component is determined
        based on the type of `x` using the selected widget specification of the layout.

        Parameters
        ----------
        name: str
            Name of the widget.
        x: object of supported type
            Object used to determine which interactive component is returned.
        label: str or None, optional
            Label of the component.

        Returns
        -------
        dasher.base.BaseWidget
            Generated dasher widget.

        See Also
        --------
        get_widget: Generates widget and returns the ``layout`` of the widget.
        get_component: Generates widget and returns the widgets' ``component``.
        """
        for type_spec, component_cls in self.layout.widget_spec.items():
            if isinstance(x, type_spec):
                return component_cls(name, x, label)
        raise NotImplementedError(
            f"No layout specification found for {name} of type {type(x)}"
        )

    def get_component(self, name, x):
        """ Generate an interactive dash component.
        This is a convenience method, which first calls the ``generate_widget`` method
        and then directly returns the un-styled and un-labeled ``component`` of the
        widget.

        Parameters
        ----------
        name: str
            Name of the component.
        x: object of supported type
            Object used to determine which interactive component is returned.

        Returns
        -------
        dash.development.base_component.Component
            Generated dash component.
        """
        return self.generate_widget(name, x, None).component

    def get_widget(self, name, x, label=None):
        """ Generate a styled and labeled interactive dash component.
        This is a convenience method, which first calls the ``generate_widget`` method
        and then directly returns the ``layout`` of the widget.

        Parameters
        ----------
        name: str
            Name of the component.
        x: object of supported type
            Object used to determine which interactive component is returned.
        label: str or None, optional
            Label of the component.

        Returns
        -------
        dash.development.base_component.Component
            Generated dash component.
        """
        return self.generate_widget(name, x, label).layout

    @staticmethod
    def _create_labels_dict(labels, kw):
        if labels is None:
            return {k: k for k in kw.keys()}
        elif isinstance(labels, Sequence):
            if len(labels) != len(kw):
                raise ValueError("labels must be of same length as kw")
            return {k: l for k, l in zip(kw.keys(), labels)}
        elif isinstance(labels, Mapping):
            return {k: labels.get(k, k) for k in kw.keys()}
        else:
            raise TypeError("labels must be list-like, dict-like or None")

    def generate_widgets(self, kw, labels=None, group=None):
        """ Generate dasher widgets based on a dictionary.

        Parameters
        ----------
        kw: dict
            The keys of the dictionary define the names of the widgets and the type of
            the values is used to determine the type of the interactive widgets based on
            the selected component specification.
        labels: list or dict, optional
            Labels for the widgets. May be either a list of labels for `kw` in the order
            of appearance or a dictionary mapping the keys of `kw` to the desired
            labels. If ``None``, the keys of `kw` are used for the labels directly.
        group: str, optional
            If not ``None``, `group` will be used as a suffix for each
            component / widget name in order to group widgets.

        Returns
        -------
        list of dasher.base.BaseWidget
            List of generated dasher widgets.

        See Also
        --------
        get_widgets: Generates widgets and returns the ``layout`` of the widgets.
        get_components: Generates widgets and returns the ``component`` of the widgets.
        """
        labels = self._create_labels_dict(labels, kw)
        return [
            self.generate_widget(
                name if group is None else f"{name}-{group}", x, labels[name]
            )
            for name, x in kw.items()
        ]

    def get_widgets(self, kw, labels=None, group=None):
        """ Generate interactive widgets based on a dictionary.
        This is a convenience method, which first calls the ``generate_widgets`` method
        and then directly returns a list containing the ``layout`` of the widgets.

        Parameters
        ----------
        kw: dict
            The keys of the dictionary define the names of the widgets and the type of
            the values is used to determine the type of the interactive widgets based on
            the selected component specification.
        labels: list or dict, optional
            Labels for the widgets. May be either a list of labels for `kw` in the order
            of appearance or a dictionary mapping the keys of `kw` to the desired
            labels. If ``None``, the keys of `kw` are used for the labels directly.
        group: str, optional
            If not ``None``, `group` will be used as a suffix for each
            component / widget name in order to group widgets.

        Returns
        -------
        list of dash.development.base_component.Component
            List of generated interactive components.
        """
        widgets = self.generate_widgets(kw, labels, group)
        return [w.layout for w in widgets]

    def get_components(self, kw, labels=None, group=None):
        """ Generate interactive components based on a dictionary.
        This is a convenience method, which first calls the ``generate_widgets`` method
        and then directly returns a list containing the un-styled and un-labeled
        ``component`` of the widgets.

        Parameters
        ----------
        kw: dict
            The keys of the dictionary define the names of the widgets and the type of
            the values is used to determine the type of the interactive widgets based on
            the selected component specification.
        labels: list or dict, optional
            Labels for the widgets. May be either a list of labels for `kw` in the order
            of appearance or a dictionary mapping the keys of `kw` to the desired
            labels. If ``None``, the keys of `kw` are used for the labels directly.
        group: str, optional
            If not ``None``, `group` will be used as a suffix for each
            component / widget name in order to group widgets.

        Returns
        -------
        list of dash.development.base_component.Component
            List of generated interactive components.

        """
        widgets = self.generate_widgets(kw, labels, group)
        return [w.component for w in widgets]

    @staticmethod
    def generate_dependencies(widgets, output_id, output_dependency="children"):
        """ Generate input and output dependencies for a list of widgets.
        It generates an ``dash.dependencies.Input`` for each widgets' underlying dash
        component using the ``value`` property. An ``dash.dependencies.Output`` is
        generated for `output_id` using the ``children`` property.

        Parameters
        ----------
        widgets: list of BaseWidget
            List of dasher widgets to generate dependencies for.
        output_id: str
            Id of the output.
        output_dependency: str, optional
            Property for the output dependency.

        Returns
        -------
        output: dash.dependencies.Output
            Generated output dependency.
        input_list: list of dash.dependencies.Input
            List of generated input dependencies.
        """
        input_list = [Input(w.name, w.dependency) for w in widgets]
        output = Output(output_id, output_dependency)
        return output, input_list

    @staticmethod
    def register_callback(app, callback):
        """ Register a dasher callback with dependencies in the dash app.

        Parameters
        ----------
        app: dash.Dash
            The dash app.
        callback: DasherCallback
            The dasher callback to register.
        """
        return app.callback(callback.outputs, callback.inputs)(callback.f)

    @staticmethod
    def generate_callback_id(name):
        """ Get callback id from ``name``.
        It is a lowercase version of ``name``, where all non-alphanumeric characters are
        replaced by underscores.

        Parameters
        ----------
        name: str
            The callback ``name`` to generate an id from.

        Returns
        -------
        str
            Lowercase version of ``name``, where all non-alphanumeric characters are
            replaced by underscores.
        """
        return generate_callback_id(name)
