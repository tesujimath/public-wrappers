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
import sys

from .ConfigError import ConfigError

def configure_conda_wrappers(args, config, wrappers):
    for name, env in config.iter('conda'):
        wrapperdir = env.getValueOrDie('wrapperdir')
        if config.getValueOrNone('globally-unique-wrappers'):
            wrapperkey = 'global'
        else:
            wrapperkey = wrapperdir

        envdir = env.getValueOrDie('envdir')
        envbindir = os.path.join(envdir, 'bin')
        if not os.path.isdir(envbindir):
            env.error('bin not found in filesystem at %s' % envbindir)

        public = {program: True for program in env.getValueOrDie('public')}
        programs = {}

        # ensure wrapperdir exists
        if not os.path.isdir(wrapperdir):
            os.makedirs(wrapperdir)

        # delete any unwanted programs
        for program in os.listdir(wrapperdir):
            if program not in public and program != 'run-in':
                path = os.path.join(wrapperdir, program)
                sys.stderr.write('rm %s\n' % path)
                os.remove(path)
            else:
                programs[program] = True

        # create wrappers
        for program in public:
            cmd = ['create-wrappers',
                   '-t', 'conda',
                   '--conda-env-dir', envdir,
                   '-b', envbindir,
                   '-d', wrapperdir,
                   '-f', program]
            if program not in programs or args.force:
                sys.stderr.write('%s\n' % ' '.join(cmd))
                subprocess.check_call(cmd)
