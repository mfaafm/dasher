from collections import OrderedDict
from collections.abc import Sequence, Mapping
from dash.dependencies import Input, Output
from dasher.base import DasherWidget, DasherLayout


class DasherApi(object):
    """ Dasher api.
    The api allows generation of components, widgets and dash dependencies (for
    ``DasherCallback``s). It is used by ``Dasher`` to generate interactive apps.
    """

    def __init__(
        self, title=None, components="bootstrap", layout="bootstrap", layout_kw=None
    ):
        """
        Parameters
        ----------
        title: str, optional
            Title of the app.
        components: str or OrderedDict, optional
            Name of a built-in component specification or an OrderedDict containing
            a component specification.
        layout: str or DasherLayout subclass, optional
            Name of a built-in layout or custom layout (DasherLayout subclass)
        layout_kw: dict, optional
            Dictionary of keyword arguments passed to the `layout` class.
        """
        self.components = self._load_components(components)

        if layout_kw is None:
            layout_kw = {}
        self.layout = self._load_layout(layout)(title, **layout_kw)

    @staticmethod
    def _load_components(components):
        if isinstance(components, OrderedDict):
            return components
        elif components == "bootstrap":
            from dasher.components.bootstrap import COMPONENTS

            return COMPONENTS
        else:
            msg = (
                "components must be either a named component specification or an "
                "OrderedDict containing a component specification. "
                "Named component specifications are: bootstrap"
            )
            raise ValueError(msg)

    @staticmethod
    def _load_layout(layout):
        if layout == "bootstrap":
            from dasher.layout.bootstrap import BootstrapLayout

            return BootstrapLayout
        elif issubclass(layout, DasherLayout):
            return layout
        else:
            msg = "layout must be either a named layout or a subclass of DasherLayout"
            raise ValueError(msg)

    def generate_component(self, name, x):
        """ Generate a dasher component.
        The type of the interactive component is determined
        based on the type of `x` using the selected component specification.

        Parameters
        ----------
        name: str
            Name of the component.
        x: object of supported type
            Object used to determine which interactive component is returned.

        Returns
        -------
        DasherComponent
            Generated dasher component.

        See Also
        --------
        get_component: Generates component and returns a dash component.
        """
        for type_spec, component_cls in self.components.items():
            if isinstance(x, type_spec):
                return component_cls(name, x)
        raise NotImplementedError(
            f"No layout specification found for {name} of type {type(x)}"
        )

    def generate_widget(self, name, x, label):
        """ Generate a dasher widget, which is a styled and labeled version of a
        dasher component.

        First, a component is generated using the
        `generate_component` method. Then, a `DasherWidget` is created by combining
        the generated component and the `label` using the selected layout class.

        Parameters
        ----------
        name: str
            Name of the component.
        x: object of supported type
            Object used to determine which interactive component is returned.
        label: str
            Label of the component.

        Returns
        -------
        DasherWidget
            Generated dasher widget.

        See Also
        --------
        get_widget: Generates widget and returns a dash component.
        """
        component = self.generate_component(name, x)
        layout = self.layout.render_component(label, component)
        return DasherWidget(component=component, label=label, layout=layout)

    def get_component(self, name, x):
        """ Generate an interactive dash component. This is a convenience method, which
        first calls the ``generate_component`` method and then directly returns a dash
        component.

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
        return self.generate_component(name, x).layout

    def get_widget(self, name, x, label):
        """ Generate a labeled and styled interactive dash component. This is a convenience
        method, which first calls the ``generate_widget`` method and then directly
        returns a dash component.

        Parameters
        ----------
        name: str
            Name of the component.
        x: object of supported type
            Object used to determine which interactive component is returned.
        label: str
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
        list of DasherWidget
            List of generated dasher widgets.
        """
        labels = self._create_labels_dict(labels, kw)
        return [
            self.generate_widget(
                name if group is None else f"{name}-{group}", x, labels[name]
            )
            for name, x in kw.items()
        ]

    @staticmethod
    def generate_dependencies(widgets, output_id):
        """ Generate input and output dependencies for a list of widgets.
        It generates an ``dash.dependencies.Input`` for each widgets' underlying dash
        component using the ``value`` property. An ``dash.dependencies.Output`` is
        generated for `output_id` using the ``children`` property.

        Parameters
        ----------
        widgets: list of DasherWidget
            List of dasher widgets to generate dependencies for.
        output_id: str
            Id of the output.

        Returns
        -------
        output: dash.dependencies.Output
            Generated output dependency.
        input_list: list of dash.dependencies.Input
            List of generated input dependencies.
        """
        input_list = [Input(w.component.name, "value") for w in widgets]
        output = Output(output_id, "children")
        return output, input_list

    @staticmethod
    def register_callback(app, callback):
        """ Register a dasher callback with dependencies to the dash app.

        Parameters
        ----------
        app: dash.Dash
            The dash app
        callback: DasherCallback
            The dasher callback to register
        """
        return app.callback(callback.outputs, callback.inputs)(callback.f)
