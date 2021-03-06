#!/usr/bin/env python

#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the autoreadme project.
#  Please respect the license - more about this in the section (*) below.
#
#  autoreadme is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  autoreadme is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with autoreadme.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

import getopt
import sys


def main(argv):
    """Args handling based on https://www.tutorialspoint.com/python/python_command_line_arguments.htm"""
    from autoreadme_.autoreadme import rewrite
    inputfile = scripts = outputfile = None
    try:
        opts, args = getopt.getopt(argv, "hi:s:o:", ["ifile=", "scripts=", "ofile="])
    except getopt.GetoptError:
        print("Usage:")
        print('rewritereadme.py -i <inputfile> -s <scriptsfolder> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('rewritereadme.py -i <inputfile> -s <scriptsfolder> -o <outputfile>')
            print(
                "Tags <<mycode1>>, <<mycode2>>, ...  in the inputfile will be replaced by the code and its output, using markdown syntax.")
            print("The first line in each script should be a comment containing a title for the code.")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--scripts"):
            scripts = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if None in [inputfile, scripts, outputfile]:
        print("Usage:")
        print('rewritereadme.py -i <inputfile> -s <scriptsfolder> -o <outputfile>')
        sys.exit(2)
    rewrite(inputfile, scripts, outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
