Advanced Use
============

Logging
-------

``nukecontexts`` creates it's own logger on import that is used by all context
managers to indicate when contexts are entered and exited. The standard logger
logs to ``stdout``.

Should your pipeline have more advanced logging needs, simply pass your custom
logger to each context manager, using the ``log`` keyword argument.

Sentry support
--------------

``nukecontexts`` offers optional support for the `Sentry <http://sentry.io/>`_
error tracking service. To use `Sentry <http://sentry.io/>`_ with
``nukecontexts``, install `Raven <https://pypi.python.org/pypi/raven>`_ into
your environment, set the ``SENTRY_DSN`` environment variable before importing
``nukecontexts`` and you're good to go.
