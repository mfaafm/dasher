import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.development.base_component import Component
from dasher.base import DasherWidget, DasherBaseWidgetFactory
from numbers import Real, Integral
from collections import Iterable, Mapping
from dasher.min_max_value import get_min_max_value


class DasherWidgetFactory(DasherBaseWidgetFactory):
    """ Default widget factory of dasher.

    Parameters
    ----------
    slider_max_marks: int, default: 8
        Maximum number of marks used for sliders
    slider_float_steps: int, default: 60
        Maximum number of steps used for float sliders
    """

    def __init__(self, slider_max_marks=8, slider_float_steps=60):
        self.slider_max_marks = slider_max_marks
        self.slider_float_steps = slider_float_steps

    def create_widget(self, name, label, x):
        """
        Create dasher widget.
        The type of ``x`` determines which widget will be generated.

        All supported types and their corresponding dash components are:
        * ``bool``: Radio item (``dash_bootstrap_components.RadioItem``)
        * ``str``: Input field (``dash_bootstrap_components.Input``)
        * ``int``: Slider, integers) (``dash_core_components.Slider``)
        * ``float``: Slider, floats (``dash_core_components.Slider``)
        * ``tuple``: Slider, (``dash_core_components.Slider``)
            Can be (min, max) or (min, max, step). The type of all the tuple entries
            must either be ``int`` or ``float``, which determines whether an integer or
            float slider will be generated.
        * ``collections.Iterable``: Dropdown menu (``dash_core_components.Dropdown``)
            Typically a ``list`` or anything iterable, which is not a ``tuple``.
        * ``collections.Mapping``: Dropdown menu (``dash_core_components.Dropdown``)
            Typically a ``dict``. A mapping will use the keys as labels shown in the
            dropdown menu, while the values will be used as arguments to the callback
            function.
        * ``dash.development.base_component.Component``: custom dash component
            Any dash component will be used as a widget as-is. This allows full
            customization of a widget if desired. The components ``value`` will be used
            as argument of the callback function.

        Parameters
        ----------
        name: str
            Unique name of the widget (serves as the dash components ``id``).
        label: str
            Label of the widget. This value will be used by the template.
        x
            Default value. The type of ``x`` determines which widget will be generated.

        Returns
        -------
        widget: DasherWidget
        """
        dash_component = self._create_dash_component(name, x)
        if dash_component is not None:
            return DasherWidget(name, label, dash_component)
        else:
            return None

    def _create_dash_component(self, name, x):
        if isinstance(x, Component):
            return self._component_widget(name, x)
        elif isinstance(x, bool):
            return self._boolean_widget(name, x)

        elif isinstance(x, str):
            return self._string_widget(name, x)

        if isinstance(x, (Real, Integral)):
            x = (x,)

        if isinstance(x, tuple):
            return self._tuple_widget(name, x)
        elif isinstance(x, Iterable):
            return self._iterable_widget(name, x)
        else:
            return None

    @staticmethod
    def _component_widget(name, x):
        if getattr(x, "id", None) is None:
            x.id = name
        else:
            raise ValueError("Component id must be empty.")
        return x

    @staticmethod
    def _boolean_widget(name, x):
        return dbc.RadioItems(
            id=name,
            options=[
                {"label": "True", "value": True},
                {"label": "False", "value": False},
            ],
            value=x,
        )

    @staticmethod
    def _string_widget(name, x):
        return dbc.Input(id=name, type="text", value=x)

    @staticmethod
    def _iterable_widget(name, x):
        if isinstance(x, Mapping):
            options = [{"label": key, "value": value} for key, value in x.items()]
        else:
            options = [{"label": i, "value": i} for i in x]

        if len(options) > 0:
            return dcc.Dropdown(
                id=name, options=options, clearable=False, value=options[0]["value"]
            )
        else:
            return None

    def _tuple_widget(self, name, x):
        step = None

        if len(x) == 1:
            minimum, maximum, value = get_min_max_value(None, None, value=x[0])
        elif len(x) == 2:
            minimum, maximum, value = get_min_max_value(x[0], x[1])
        elif len(x) == 3:
            step = x[2]
            if step < 0:
                raise ValueError("step must be >= 0")
            minimum, maximum, value = get_min_max_value(x[0], x[1], step=step)
        else:
            raise ValueError("tuple must be (value, ), (min, max) or (min, max, step)")

        if all(isinstance(i, Integral) for i in x):
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
            id=name, min=minimum, max=maximum, step=step, value=value, marks=marks
        )
