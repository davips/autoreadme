#!/usr/bin/python

#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the autoreadme project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      autoreadme is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      autoreadme is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with autoreadme.  If not, see <http://www.gnu.org/licenses/>.
#

import io
import os
import re
from contextlib import redirect_stdout
from itertools import takewhile
import sys, getopt


def collapse(summary, content):
    return f"<details>\n<summary>{summary}</summary>\n<p>\n\n{content}\n\n</p>\n</details>"


def codify(text):
    return '```python3\n' + text + '\n```'


def output(text):
    return '```bash\n' + text + '```'


def rewrite(input_file, scripts_folder, output_file):
    # Check existence of README-edit.md at the provided folder.
    file = input_file
    if not os.path.exists(file):
        raise Exception("input_file not found:", input_file)
    print(input_file)

    # Read "extended" markdown file and locate tags indicating file inclusion.
    txt = "\n".join(open(file).read().split("\n"))
    tags = re.findall('<<.*?>>', txt)

    # Replace each tag by its respective code file (and output by running it).
    for tag in tags:
        # Read code file as lines.
        filename = tag[2:-2]
        print("\t", filename)
        script = scripts_folder + "/" + filename + ".py"
        if not os.path.exists(script):
            print("script file not found:", script)
            continue

        code = open(script).read().split("\n")
        title = code[0][2:]

        # Handle each code segment separately.
        line = 0
        partial = []
        while line < len(code):
            # Read until boundary given by "# ...".
            lines = list(takewhile(lambda x: "# ..." not in x, code[line:]))

            print(lines)
            segment = "\n".join(lines)
            if segment == "":
                break
            partial.append(codify(segment))

            # Run segment and capture output.
            f = io.StringIO()
            with redirect_stdout(f):
                exec(segment)
            out = f.getvalue()
            partial.append("\n" + output(out))

            line += len(lines) + 1
        txt = txt.replace(tag, collapse(title, "\n".join(partial)))
    with open(output_file, "w") as f:
        f.write(txt)
        print("\t", output_file, "written!")


def main(argv):
    # Args handling based on https://www.tutorialspoint.com/python/python_command_line_arguments.htm
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
            print("Tags <<mycode1>>, <<mycode2>>, ...  in the inputfile will be replaced by the code and its output, using markdown syntax.")
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
