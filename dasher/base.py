from abc import ABC, abstractmethod


class DasherBaseWidgetFactory(ABC):
    @classmethod
    @abstractmethod
    def create_widget(cls, name, label, x):
        pass


class DasherBaseTemplate(ABC):
    @classmethod
    @abstractmethod
    def update_layout(cls, layout, callback_list):
        pass

    @classmethod
    @abstractmethod
    def generate_connections(cls, callback):
        pass


class DasherComponent(ABC):
    def __init__(self, name, x):
        self.name = name
        self.x = x

    @abstractmethod
    def generate(self):
        pass


class DasherWidget(object):
    def __init__(self, name, component, label=None):
        self.name = name
        self.component = component
        self.label = label if label is not None else name


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

