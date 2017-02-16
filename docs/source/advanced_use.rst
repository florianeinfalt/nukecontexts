Advanced Use
============

Logging
-------

``nukecontexts`` creates it's own logger on import that is used by all context
managers to indicate when contexts are entered and exited. The standard logger
logs to ``stdout``.

Should your pipeline have more advanced logging needs, simply pass your custom
logger to each context manager, using the ``log`` keyword argument.
