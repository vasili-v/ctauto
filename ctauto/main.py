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
from ctauto.parser import TemplateParser

def arguments():
    parser = argparse.ArgumentParser(description="YAML driven C Templates")
    parser.add_argument("template", help="template files to process")

    arguments = parser.parse_args()
    return arguments.template

def main():
    template = arguments()

    parser = TemplateParser()
    parser.parse(read(template), template)

    return 0
