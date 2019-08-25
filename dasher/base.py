from abc import ABC, abstractmethod
from dash.development.base_component import Component


class DasherComponent(ABC):
    def __init__(self, name, x):
        self.name = name
        self.x = x

    @property
    @abstractmethod
    def layout(self):
        pass


class DasherWidget(object):
    def __init__(self, component, label, layout):
        self.component = component
        self.label = label
        if not isinstance(layout, Component):
            raise TypeError("widget must be a dash Component")
        self.layout = layout


class DasherLayout(ABC):
    def __init__(self, title, credits=True):
        if title is None:
            self.title = "Dasher app"
        else:
            self.title = title
        self.credits = credits

    @staticmethod
    @abstractmethod
    def render_component(label, component):
        pass

    @abstractmethod
    def add_callback(self, callback, app):
        pass


class DasherCallback(object):
    def __init__(self, name, description, f, kw, labels, widgets, outputs, inputs):
        self.name = name
        self.description = description
        self.f = f
        self.kw = kw
        self.labels = labels
        self.widgets = widgets
        self.outputs = outputs
        self.inputs = inputs
        self.layout = None
