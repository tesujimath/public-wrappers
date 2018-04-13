===============
public-wrappers
===============

public-wrappers provides a means to wrap selected public programs from conda
and/or virtualenv environments, so they may be invoked directly by users without
having to explicitly activate the environment.  It makes use of `exec-wrappers
<https://github.com/gqmelo/exec-wrappers>`_ to do the wrapping.

public-wrappers identifies only certain programs from each environment as being
public, by means of a configuration file.  These public programs are wrapped,
using `exec-wrappers <https://github.com/gqmelo/exec-wrappers>`_.

A number of environments may be wrapped, either into separate or a common
wrappers directory.

Configuration
=============
A configuration file is required.  The configuration file is the first of these
which exist:

- via the command line option ``--config``
- via the environment variable ``PUBLIC_WRAPPERS_CONFIG``
- ``~/.public-wrappers.toml``
- ``/etc/public-wrappers.toml``

The configuration file simply lists the conda and virtualenv environments
along with the list of their public programs to be wrapped.  Each environment
may have its own destination directory for wrapper scripts, or these may be
shared.

Programs must be unique within each wrapper directory, or globally unique if the
configuration item ``globally-unique-wrappers`` is ``true``.

Environment variables such as ``$HOME`` or user-relative pathnames such as
``~`` may be used in the configuration file.

See the `example configuration file <doc/example-config.toml>`__.  Also, it is
recommended to install a profile file into ``/etc/profile.d``.  See the
`example profile.sh <doc/example-profile.sh>`__.

Usage
=====

For example, if ``~/.public-wrappers.toml`` exists:

::

  configure-public-wrappers

Otherwise, for example:

::

  configure-public-wrappers -c ~/example-config.toml

Installation
============
public-wrappers is available on PyPI.

::

  $ virtualenv ~/virtualenvs/public-wrappers
  $ source ~/virtualenvs/public-wrappers/bin/activate
  (public-wrappers)$ pip install public-wrappers
  (public-wrappers)$ configure-public-wrappers --help

and also on `conda-forge <https://conda-forge.org/>`_.

::

  $ conda install public-wrappers
  $ configure-public-wrappers --help
