#!/usr/bin/env python
#
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

import argparse
import os.path
import pytoml as toml
import sys

from public_wrappers.conda import configure_conda_wrappers
from public_wrappers.ConfigError import ConfigError
from public_wrappers.config import read_config_file

def main():
    parser = argparse.ArgumentParser(description='Configure public wrappers for conda applications.')
    parser.add_argument('-c', '--config', dest='config', metavar='FILE', help='configuration file')
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='configuration file')
    args = parser.parse_args()

    config = read_config_file(args)
    wrappers = {}
    try:
        configure_conda_wrappers(args, config, wrappers)
    except ConfigError as e:
        sys.stderr.write('%s\n' % e)

if __name__ == '__main__':
    main()
