Changelog
=========

0.3.0 (2019-12-15)
------------------
* Generate ``id`` property from ``name`` for every callback. The ``id`` is now used to
  identify the callback, while ``name`` is used in the layout for displaying.

0.2.0 (2019-11-03)
------------------
* Use cookiecutter to create a proper project structure.
* Refactor core functionality into ``dasher.Api``.
* Combine widget factory and template logic into unified layout implementation.
* Fix resizing bug when switching tabs by using callback-based tab switching.
* Add support of fully custom widgets.
* Add documentation.
* Add more examples.

0.1.2 (2019-07-16)
------------------
* Add ``_labels`` argument to the ``callback`` decorator to enable customization of
  widget labels.

0.1.1 (2019-06-10)
------------------
* Add ``credits`` argument to DasherStandardTemplate to toggle whether to show credits
  in the navbar.
* Update docstrings and documentation.
* Add margin to navbar.
