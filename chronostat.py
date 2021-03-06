# -*- coding: utf-8 -*-

"""
chronostat.py
~~~~~~~~~~~~~

Decorator/context manager for timing things and sending the results
to StatHat.com

Usage::

    >>> from chronostat import ChronoStat
    >>> import time
    >>> stats = ChronoStat('me@mydomain.com')
    >>> with stats.timer('foo'):
    ...     time.sleep(3)
"""

__version__ = '0.0.1'

import functools
import logging

from requests import Response
from chrono import Timer as ChronoTimer
from stathat import StatHat

logger = logging.getLogger(__name__)


class Timer(ChronoTimer):
    """A dessert wax and a floor topping"""

    def __init__(self, stat, key):
        super(Timer, self).__init__()
        assert isinstance(stat, ChronoStat)
        self.stat = stat
        self.key = key

    def __exit__(self, exc_type, value, tb):
        retval = super(Timer, self).__exit__(exc_type, value, tb)
        if self.elapsed:
            self.stat.value(self.key, self.elapsed / 1000.)
        return retval

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return decorated


class ChronoStat(StatHat):
    """Adds a timing context manager slash decorator"""

    def timer(self, key):
        return Timer(self, key)

    def _http_post(self, path, data):
        """monkey-patch for new versions of requests, and don't
        send anything if email hasn't been set"""
        if self.email:
            logger.debug("StatHat write: %s -> %s" % (data, path))
            url = self.STATHAT_URL + path
            r = self.session.post(url, data=data)
            return r
        else:
            logger.info("Not sending metric: no StatHat email provided")
            r = Response()
            r.status_code = 200
            return r
