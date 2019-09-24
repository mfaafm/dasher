""" Module containing the component specification and implementation of the interactive
dasher components based on ``dash_bootstrap_components``.

The component specification supports the following types and generates the corresponding
interactive components:

* ``bool``: Radio Items
* ``str``: Input field
* ``int``: Slider, integer
* ``float``: Slider, floats
* ``tuple``: Slider
  Can be (min, max) or (min, max, step). The type of all the tuple entries
  must either be ``int`` or ``float``, which determines whether an integer or
  float slider will be generated.
* ``collections.Iterable``: Dropdown menu
  Typically a ``list`` or anything iterable.
* ``collections.Mapping``: Dropdown menu
  Typically a ``dict``. A mapping will use the keys as labels shown in the
  dropdown menu, while the values will be used as arguments to the callback
  function.
* ``dash.development.base_component.Component``: custom dash component
  Any dash component will be used as-is. This allows full customization of a
  component if desired. The components ``value`` will be used as argument to
  the callback function.

"""

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
    """ RadioItems component used for booleans. """
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
    """ Input field component used for for strings. """
    @property
    def layout(self):
        return dbc.Input(id=self.name, type="text", value=self.x)


class IterableComponent(DasherComponent):
    """ Dropdown component used for iterables and mappings. """
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
    """ Slider components used for tuples of numbers. """
    def __init__(self, name, x, slider_max_ticks=8, slider_float_steps=60):
        """
        Parameters
        ----------
        name: str
            Name of the component.
        x: tuple of int or float
            Tuple used to configure the slider.
        slider_max_ticks: int, default 8
            Maximum number of ticks to draw for the slider.
        slider_float_steps: int, default 60
            Number of float steps to use if step is not defined explicity.
        """
        super().__init__(name, x)
        self.slider_max_marks = slider_max_ticks
        self.slider_float_steps = slider_float_steps

    @property
    def layout(self):
        step = None

        if len(self.x) == 1:
            minimum, maximum, value = get_min_max_value(None, None, x=self.x[0])
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
    """ Component used for numbers. """
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
""" Component specification. """
