from collections import OrderedDict
from collections.abc import Sequence, Mapping
from dash.dependencies import Input, Output
from dasher.base import DasherWidget


class DasherApi(object):
    def __init__(self, components="bootstrap"):
        self.components = self._load_components(components)

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

    def generate_component(self, name, x):
        for type_spec, component_cls in self.components.items():
            if isinstance(x, type_spec):
                return component_cls(name, x).generate()
        raise NotImplementedError(
            f"No component specification found for {name} of type {type(x)}"
        )

    def generate_widget(self, name, x, label=None):
        component = self.generate_component(name, x)
        return DasherWidget(name=name, component=component, label=label)

    @staticmethod
    def _create_labels_dict(labels, d):
        if labels is None:
            return {k: k for k in d.keys()}
        elif isinstance(labels, Sequence):
            if len(labels) != len(d):
                raise ValueError("labels must be of same length as d")
            return {k: l for k, l in zip(d.keys(), labels)}
        elif isinstance(labels, Mapping):
            return {k: labels.get(k, k) for k in d.keys()}
        else:
            return TypeError("labels must be list-like, dict-like or None")

    def generate_widgets(self, d, labels=None, group=None):
        labels = self._create_labels_dict(labels, d)
        return [
            self.generate_widget(
                name if group is None else f"{name}-{group}", x, labels[name]
            )
            for name, x in d.items()
        ]

    @staticmethod
    def generate_dependencies(widgets, output_id):
        input_list = [Input(w.name, "value") for w in widgets]
        output = Output(output_id, "children")
        return output, input_list

    @staticmethod
    def register_callback(app, callback):
        return app.callback(callback.outputs, callback.inputs)(callback.f)
