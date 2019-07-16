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


class DasherWidget(object):
    def __init__(self, name, label, dash_component):
        self.name = name
        self.label = label
        self.dash_component = dash_component


class DasherCallback(object):
    def __init__(self, _id, name, description, kw, widget_list, labels):
        self.id = _id
        self.name = name
        self.description = description
        self.kw = kw
        self.widget_list = widget_list
        self.labels = labels
