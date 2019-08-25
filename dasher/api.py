from collections import OrderedDict
from collections.abc import Sequence, Mapping
from dash.dependencies import Input, Output
from dasher.base import DasherWidget, DasherLayout


class DasherApi(object):
    def __init__(
        self, title=None, components="bootstrap", layout="default", layout_kw=None
    ):
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
                "components must be either a named layout specification or an "
                "OrderedDict containing a layout specification. "
                "Named layout specifications are: bootstrap"
            )
            raise ValueError(msg)

    @staticmethod
    def _load_layout(layout):
        if layout == "default":
            from dasher.layout.default import DefaultLayout

            return DefaultLayout
        elif issubclass(layout, DasherLayout):
            return layout
        else:
            msg = "layout must be either a named layout or a subclass of DasherLayout"
            raise ValueError(msg)

    def generate_component(self, name, x):
        for type_spec, component_cls in self.components.items():
            if isinstance(x, type_spec):
                return component_cls(name, x)
        raise NotImplementedError(
            f"No layout specification found for {name} of type {type(x)}"
        )

    def generate_widget(self, name, x, label):
        component = self.generate_component(name, x)
        layout = self.layout.render_component(label, component)
        return DasherWidget(component=component, label=label, layout=layout)

    def get_component(self, name, x):
        return self.generate_component(name, x).layout

    def get_widget(self, name, x, label):
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
        labels = self._create_labels_dict(labels, kw)
        return [
            self.generate_widget(
                name if group is None else f"{name}-{group}", x, labels[name]
            )
            for name, x in kw.items()
        ]

    @staticmethod
    def generate_dependencies(widgets, output_id):
        input_list = [Input(w.component.name, "value") for w in widgets]
        output = Output(output_id, "children")
        return output, input_list

    @staticmethod
    def connect_callback(app, callback):
        return app.callback(callback.outputs, callback.inputs)(callback.f)
