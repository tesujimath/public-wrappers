# Copyright (c) 2018 Simon Guest
#
# This file is part of public-wrappers.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from future.utils import viewitems
from past.builtins import basestring
import os.path
import pytoml as toml

from .ConfigError import ConfigError

def expand(s):
    return os.path.expanduser(os.path.expandvars(s))

class ConfigObject:
    def __init__(self, filename, context, obj):
        self.filename = filename
        self.context = context
        self.obj = obj

    def error(self, msg):
        raise ConfigError(self.filename, self.context, msg)

    def iter(self, key):
        """Iterate over values for key, which is allowed to not exist."""
        if key in self.obj:
            for subkey, subobj in viewitems(self.obj[key]):
                yield subkey, ConfigObject(self.filename, self.context + [key, subkey], subobj)

    def getConfigOrDie(self, key):
        """Return config at key, or raise a ConfigError."""
        if key in self.obj:
            return ConfigObject(self.filename, self.context + [key], self.obj[key])
        else:
            self.error('missing %s' % key)

    def _getValue(self, key):
        value = self.obj[key]
        if isinstance(value, basestring):
            return expand(value)
        else:
            return value

    def getValueOrDie(self, key):
        """Return value at key, or raise a ConfigError."""
        if key in self.obj:
            return self._getValue(key)
        else:
            self.error('missing %s' % key)

    def getValueOrNone(self, key):
        """Return value at key, or None."""
        if key in self.obj:
            return self._getValue(key)
        else:
            return None

def read_config_file(args):
    filename = None
    if args.config:
        filename = args.config
        if not os.path.exists(filename):
            raise ConfigError('%s' % filename, [], 'file not found')
    else:
        env_config = 'PUBLIC_WRAPPERS_CONFIG'
        attempt_files = ([os.environ[env_config]] if env_config in os.environ else []) + [
            os.path.expanduser('~/.public-wrappers.toml'),
            '/etc/public-wrappers.toml',
        ]
        for attempt in attempt_files:
            if os.path.exists(attempt):
                filename = attempt
                break
        if filename is None:
            raise ConfigError('', [], 'none of %s found' % ', '.join(attempt_files))

    with open(filename, 'rb') as f:
        try:
            obj = toml.load(f)
        except toml.TomlError as e:
            raise ConfigError(filename, [], 'TOML error at line %d' % e.line)
    return ConfigObject(filename, [], obj)
