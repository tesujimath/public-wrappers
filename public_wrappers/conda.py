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

import os
import os.path
import subprocess

from .ConfigError import ConfigError

def configure_conda_wrappers(envs):
    for name in envs:
        env = envs[name]

        if 'wrapperdir' not in env:
            raise ConfigError('conda env %s missing wrapperdir' % name)
        wrapperdir = env['wrapperdir']

        if 'envdir' not in env:
            raise ConfigError('conda env %s missing envdir' % name)
        envdir = env['envdir']
        if not os.path.isdir(envdir):
            raise ConfigError('conda env %s not found in filesystem at' % (name, envdir))
        envbindir = os.path.join(envdir, 'bin')
        if not os.path.isdir(envbindir):
            raise ConfigError('conda env %s bin not found in filesystem at' % (name, envbindir))

        if 'public' not in env:
            raise ConfigError('conda env %s missing public' % name)
        public = {program: True for program in env['public']}

        # ensure wrapperdir exists
        if not os.path.isdir(wrapperdir):
            os.makedirs(wrapperdir)

        # delete any unwanted programs
        for program in os.listdir(wrapperdir):
            if program not in public:
                os.remove(os.path.join(wrapperdir, program))

        # create wrappers
        for program in public:
            subprocess.check_call(['create-wrappers',
                                   '-t', 'conda',
                                   '--conda-env-dir', envdir,
                                   '-b', envbindir,
                                   '-d', wrapperdir,
                                   '-f', program])
