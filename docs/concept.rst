=======
Concept
=======

The idea behind dasher is to create auto-generated interactive `plotly dash`_ dashboards
as easy as using the `ipywidgets interact`_ decorator in jupyter notebooks. That is,
by decorating a user defined callback function! Here, the keyword arguments of the
decorator define the interactive widgets and the callback
function must return what you want to show in the content container in the dashboard.

Dasher automatically renders a layout consisting of a header with the dashboard's
title, a widget container providing the interactivity and the content container.
The only thing you need to do in the callback function is to process the input arguments
(which correspond to the widgets) and to return a list of the plotly dash components
that you want to appear in the content container!

The interactive widgets are automatically generated based on the type of the keyword
arguments of the decorator. For example, a string will result in an input field and
a list will become a dropdown box. Dasher supports the same widget abbreviations as
ipywidgets ``interact``, see their `widget abbreviations`_.

Since the layout and the widget connections to the callback are taken care of by
dasher, you can concentrate on what you to display on the dashboard. As a result,
generating a stunning interactive visualization becomes a matter of minutes!


Dasher API
==========
The functionality of the :class:`dasher.Dasher` class is built upon the dasher
:class:`dasher.Api` class. The latter implements the generation of widgets and callback
dependencies. It has convenience methods to generate widgets in unstyled
(basic dash components) and styled (as used in the dasher layout) versions. Hence, you
can use dasher to generate widgets quickly, while still using a fully custom dash
layout by using the :class:`dasher.Api` directly!

.. _`plotly dash`: https://dash.plot.ly/
.. _`ipywidgets interact`: https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html
.. _`widget abbreviations`: https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html#Widget-abbreviations
