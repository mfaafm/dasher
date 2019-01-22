import dash_core_components as dcc
import dash_html_components as html
from dash.development.base_component import Component
from numbers import Real, Integral
from collections import Iterable, Mapping
from abc import ABC, abstractmethod


class DasherBaseWidgets(ABC):
    @classmethod
    @abstractmethod
    def create_widget(cls, name, x):
        pass


class DasherWidgets(DasherBaseWidgets):
    slider_max_marks = 15
    slider_float_steps = 60

    @classmethod
    def create_widget(cls, name, x):
        widget = cls._create_widget(name, x)
        if widget is not None:
            widget = html.Div([html.Label(name), widget], id=name + "_div")
        return widget

    @classmethod
    def _create_widget(cls, name, x):
        if isinstance(x, Component):
            return cls.component_widget(name, x)
        elif isinstance(x, bool):
            return cls.boolean_widget(name, x)

        elif isinstance(x, str):
            return cls.string_widget(name, x)

        if isinstance(x, (Real, Integral)):
            x = (x,)

        if isinstance(x, tuple):
            return cls.tuple_widget(name, x)
        elif isinstance(x, Iterable):
            return cls.iterable_widget(name, x)
        else:
            return None

    @staticmethod
    def component_widget(name, x):
        if getattr(x, "id", None) is None:
            x.id = name
        elif x.id != name:
            raise ValueError("Component id must match keyword name or be empty.")
        return x

    @staticmethod
    def boolean_widget(name, x):
        return dcc.RadioItems(
            id=name,
            options=[
                {"label": "True", "value": True},
                {"label": "False", "value": False},
            ],
            value=x,
        )

    @staticmethod
    def string_widget(name, x):
        return dcc.Input(id=name, type="text", value=x)

    @staticmethod
    def iterable_widget(name, x):
        if isinstance(x, Mapping):
            options = [{"label": key, "value": value} for key, value in x.items()]
        else:
            options = [{"label": i, "value": i} for i in x]

        if len(options) > 0:
            return dcc.Dropdown(id=name, options=options, value=options[0]["value"])
        else:
            return None

    @classmethod
    def tuple_widget(cls, name, x):
        step = None

        if len(x) == 1:
            minimum, maximum, value = cls._get_min_max_value(None, None, value=x[0])
        elif len(x) == 2:
            minimum, maximum, value = cls._get_min_max_value(x[0], x[1])
        elif len(x) == 3:
            step = x[2]
            if step < 0:
                raise ValueError("step must be >= 0")
            minimum, maximum, value = cls._get_min_max_value(x[0], x[1], step=step)
        else:
            raise ValueError("tuple must be (value, ), (min, max) or (min, max, step)")

        if all(isinstance(i, Integral) for i in x):
            if step is None:
                step = 1
            max_mark_step = (maximum - minimum) // cls.slider_max_marks
            ticks = list(range(minimum, maximum + 1, max(step, max_mark_step)))
            marks = {i: str(i) for i in ticks}
        else:
            if step is None:
                step = (maximum - minimum) / (cls.slider_float_steps - 1)

            ticks = list(minimum + step * i for i in range(0, int((maximum - minimum) / step)))
            ticks = ticks[::max(1, len(ticks) // cls.slider_max_marks)] + [maximum]
            marks = {int(i) if i % 1 == 0 else i: "{:.3g}".format(i) for i in ticks}

        return dcc.Slider(
            id=name, min=minimum, max=maximum, step=step, value=value, marks=marks
        )

    @staticmethod
    def _get_min_max_value(minimum, maximum, value=None, step=None):
        """Return min, max, value given input values with possible None."""
        # Either min and max need to be given, or value needs to be given
        if value is None:
            if minimum is None or maximum is None:
                raise ValueError(
                    "unable to infer range, value from: ({0}, {1}, {2})".format(
                        minimum, maximum, value
                    )
                )
            diff = maximum - minimum
            value = minimum + (diff / 2)
            # Ensure that value has the same type as diff
            if not isinstance(value, type(diff)):
                value = minimum + (diff // 2)
        else:  # value is not None
            if not isinstance(value, Real):
                raise TypeError("expected a real number, got: %r" % value)
            # Infer min/max from value
            if value == 0:
                # This gives (0, 1) of the correct type
                vrange = (value, value + 1)
            elif value > 0:
                vrange = (-value, 3 * value)
            else:
                vrange = (3 * value, -value)
            if minimum is None:
                minimum = vrange[0]
            if maximum is None:
                maximum = vrange[1]
        if step is not None:
            # ensure value is on a step
            tick = int((value - minimum) / step)
            value = minimum + tick * step
        if not minimum <= value <= maximum:
            raise ValueError(
                "value must be between min and max (min={0}, value={1}, max={2})".format(
                    minimum, value, maximum
                )
            )
        return minimum, maximum, value
