public-wrappers
===============

public-wrappers provides a means to wrap programs from conda environments, so
they may be invoked directly by users without having to explicitly activate the
environment.  It makes use of exec-wrappers to do the wrapping.

public-wrappers identifies only certain programs from a conda environment as
being public, by means of a configuration file.  These public programs are
wrapped, using exec-wrappers.

A number of conda environments may be wrapped, either into separate or a common
wrappers directory.
