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

import argparse
import yaml

from ctauto.reader import read
from ctauto.parser import parse

def get_arguments():
    parser = argparse.ArgumentParser(description="YAML driven C Templates")
    parser.add_argument("-c", "--code",
                        help='output code file (default template\'s base name '
                             'with ".c" extension)')
    parser.add_argument("--header",
                        help='output header file (default template\'s base '
                             'name with ".h" extension; if code file is '
                             'specified but this option isn\'t base name of '
                             'code file is used with ".h" extension)')
    parser.add_argument("template", help="template files to process")

    arguments = parser.parse_args()
    return arguments.template, arguments.code, arguments.header

def main():
    template, code, header = get_arguments()

    parse(read(template))

    return 0
