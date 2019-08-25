import dash_core_components as dcc
import dash_bootstrap_components as dbc
from collections.abc import Iterable, Mapping
from numbers import Real, Integral
from collections import OrderedDict
from dash.development.base_component import Component
from dasher.base import DasherComponent
from dasher.components import DashComponent
from .min_max_value import get_min_max_value


class BoolComponent(DasherComponent):
    @property
    def layout(self):
        return dbc.RadioItems(
            id=self.name,
            options=[
                {"label": "True", "value": True},
                {"label": "False", "value": False},
            ],
            value=self.x,
        )


class StringComponent(DasherComponent):
    @property
    def layout(self):
        return dbc.Input(id=self.name, type="text", value=self.x)


class IterableComponent(DasherComponent):
    @property
    def layout(self):
        if isinstance(self.x, Mapping):
            options = [{"label": k, "value": v} for k, v in self.x.items()]
        else:
            options = [{"label": x, "value": x} for x in self.x]

        if len(options) > 0:
            return dcc.Dropdown(
                id=self.name,
                options=options,
                clearable=False,
                value=options[0]["value"],
            )
        else:
            return None


class TupleComponent(DasherComponent):
    def __init__(self, name, x, slider_max_marks=8, slider_float_steps=60):
        super().__init__(name, x)
        self.slider_max_marks = slider_max_marks
        self.slider_float_steps = slider_float_steps

    @property
    def layout(self):
        step = None

        if len(self.x) == 1:
            minimum, maximum, value = get_min_max_value(None, None, value=self.x[0])
        elif len(self.x) == 2:
            minimum, maximum, value = get_min_max_value(self.x[0], self.x[1])
        elif len(self.x) == 3:
            step = self.x[2]
            if step < 0:
                raise ValueError("step must be >= 0")
            minimum, maximum, value = get_min_max_value(self.x[0], self.x[1], step=step)
        else:
            raise ValueError("tuple must be (value, ), (min, max) or (min, max, step)")

        if all(isinstance(i, Integral) for i in self.x):
            if step is None:
                step = 1
            max_mark_step = (maximum - minimum) // self.slider_max_marks
            ticks = list(range(minimum, maximum + 1, max(step, max_mark_step)))
            marks = {i: str(i) for i in ticks}
        else:
            if step is None:
                step = (maximum - minimum) / (self.slider_float_steps - 1)

            ticks = list(
                minimum + step * i for i in range(0, int((maximum - minimum) / step))
            )
            ticks = ticks[:: max(1, len(ticks) // self.slider_max_marks)] + [maximum]
            marks = {int(i) if i % 1 == 0 else i: "{:.3g}".format(i) for i in ticks}

        return dcc.Slider(
            id=self.name, min=minimum, max=maximum, step=step, value=value, marks=marks
        )


class NumberComponent(TupleComponent):
    def __init__(self, name, x):
        super().__init__(name, (x,))


COMPONENTS = OrderedDict(
    [
        (Component, DashComponent),
        (bool, BoolComponent),
        (str, StringComponent),
        ((Real, Integral), NumberComponent),
        (tuple, TupleComponent),
        (Iterable, IterableComponent),
    ]
)
