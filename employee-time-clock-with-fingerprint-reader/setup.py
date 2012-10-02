#!/usr/bin/env python
from distutils.core import setup

def main():
    setup(name='timeclock',
          version='0.1',
          author='Joshua Pritikin',
          author_email='jpritikin@pobox.com',
          url='http://gitorious.org/employee-time-clock-with-fingerprint-reader/employee-time-clock-with-fingerprint-reader',
          scripts=['bin/timeclock'],
          package_dir={'': 'lib'},
          package_data={'': ['ui/*.ui']},
          packages=['timeclock'])

if __name__ == '__main__':
    main()
