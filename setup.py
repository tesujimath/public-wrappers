#!/usr/bin/env python
#
# distutils setup script for public-wrappers package

from setuptools import setup, find_packages

long_description = """public-wrappers provides a means to wrap selected public programs from conda
environments, so they may be invoked directly by users without having to
explicitly activate the environment.  It makes use of exec-wrappers to do the
wrapping.
"""

setup(name='public-wrappers',
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      description='Wrap selected public programs from conda/virtualenv environments',
      long_description=long_description,
      author='Simon Guest',
      author_email='simon.guest@tesujimath.org',
      url='https://github.com/tesujimath/public-wrappers',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',
      ],
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'configure-public-wrappers = public_wrappers.__main__:main',
        ],
      },
      package_data={
          'doc': ['*.rst'],
      },
      license='MIT',
      install_requires=[
          'exec-wrappers',
          'future',
          'pytoml',
      ],
      python_requires='>=2.7',
     )
