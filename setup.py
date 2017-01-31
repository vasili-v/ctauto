#   ctauto - YAML driven C Templates
#   Copyright (C) 2017  Vasili Vasilyeu
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(name='ctauto',
      version='0.0.1',
      description='YAML driven C Templates',
      long_description='The tool to instantiate templates of C code using YAML encoded declarations',
      author='Vasili Vasilyeu',
      author_email='vasili.v@tut.by',
      url='https://github.com/vasili-v/ctauto',
      entry_points = {'console_scripts': ['ctauto=ctauto.main:main']},
      packages = find_packages(exclude=['test']),
      license='GPLv3',
      platforms=('Linux', 'Darwin'),
      test_suite = "test")
