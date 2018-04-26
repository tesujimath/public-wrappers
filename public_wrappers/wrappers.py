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
import os
import os.path
import stat
import subprocess
import sys

from .ConfigError import ConfigError
from .config import read_config_file

def _envdir_tag(kind):
    if kind == 'conda':
        return '--conda-env-dir'
    elif kind == 'virtualenv':
        return '--virtual-env-dir'
    else:
        raise TypeError('unknown kind %s' % kind)

def _determine_wrappers(kind, config, wrappers_by_dir, envs_by_program):
    for env_name, env in config.iter(kind):
        wrapperdir = env.getValueOrDie('wrapperdir')
        envdir = env.getValueOrDie('envdir')
        bindir = os.path.join(envdir, 'bin')
        public = env.getValueOrDie('public')

        if wrapperdir not in wrappers_by_dir:
            wrappers_by_dir[wrapperdir] = {}
        wrappers_by_program = wrappers_by_dir[wrapperdir]

        for program in public:
            if program not in envs_by_program:
                envs_by_program[program] = []
            envs_by_program[program].append(env_name)

            wrapper = {
                '-t': kind,
                '-b': bindir,
                '-d': wrapperdir,
                '-f': program,
                _envdir_tag(kind): envdir,
            }
            if program in wrappers_by_program:
                env.error('duplicate program %s in %s' % (program, wrapperdir))

            wrappers_by_program[program] = wrapper

def _validate_wrappers(config, wrappers_by_dir, envs_by_program):
    if config.getValueOrNone('globally-unique-wrappers'):
        for program, env_names in viewitems(envs_by_program):
            if len(env_names) > 1:
                config.error('duplicate program %s, environments %s' % (program, ','.join(sorted(env_names))))

    for wrapperdir, wrappers in viewitems(wrappers_by_dir):
        # check programs exist
        for program, options in viewitems(wrappers):
            bindir = options['-b']
            if not os.path.isdir(bindir):
                config.error('missing bindir %s' % bindir)
            if not os.path.exists(os.path.join(bindir, program)):
                config.error('%s not found in %s' % (program, bindir))

def _create_wrappers(args, config, wrappers_by_dir):
    overlayfs = config.getValueOrNone('overlayfs')
    for wrapperdir, wrappers in viewitems(wrappers_by_dir):
        # ensure wrapperdir exists
        if not os.path.isdir(wrapperdir):
            os.makedirs(wrapperdir)

        existing_programs = {program: True for program in os.listdir(wrapperdir)}

        # delete any unwanted programs
        if args.purge:
            for program in existing_programs:
                if program not in wrappers and program != 'run-in':
                    path = os.path.join(wrapperdir, program)
                    sys.stderr.write('rm %s\n' % path)
                    os.remove(path)

        # create wrappers
        run_in_path = os.path.join(wrapperdir, 'run-in')
        for program, options in viewitems(wrappers):
            program_path = os.path.join(wrapperdir, program)
            cmd = ['create-wrappers']
            for k, v in viewitems(options):
                cmd.extend([k, v])
            if program not in existing_programs or args.force:
                sys.stderr.write('%s\n' % ' '.join(cmd))
                if overlayfs:
                    # work-around to broken permissions on overlayfs, which stop us overwriting existing files
                    if os.path.exists(program_path):
                        os.remove(program_path)
                    if os.path.exists(run_in_path):
                        os.remove(run_in_path)
                subprocess.check_call(cmd)

def configure_wrappers(args):
    envs_by_program = {}
    wrappers_by_dir = {}
    try:
        config = read_config_file(args)
        _determine_wrappers('conda', config, wrappers_by_dir, envs_by_program)
        _determine_wrappers('virtualenv', config, wrappers_by_dir, envs_by_program)
        _validate_wrappers(config, wrappers_by_dir, envs_by_program)
        _create_wrappers(args, config, wrappers_by_dir)
    except ConfigError as e:
        sys.stderr.write('%s\n' % e)
