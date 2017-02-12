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
import os.path

from ctauto.reader import read
from ctauto.parser import TemplateParser
from ctauto.engine import run
from ctauto.renderer import render

def arguments():
    parser = argparse.ArgumentParser(description="YAML driven C Templates")
    parser.add_argument("template", help="template files to process")
    parser.add_argument("-o", "--output",
                        help="file to write output to (by default the same as template name with .c extension")

    arguments = parser.parse_args()

    directory = os.path.dirname(arguments.template)
    output = os.path.splitext(arguments.template)[0] + ".c" if arguments.output is None else arguments.output

    return directory, arguments.template, output

def main():
    directory, template, output = arguments()

    blocks = TemplateParser().parse(read(template), template)
    render(run(blocks, directory), output)

    return 0
