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

import io
import os
import re
from contextlib import redirect_stdout
from itertools import takewhile


def collapse(summary, content):
    r"""
    Collapsable content. Ps. It seems like <summary> is not working on pypi markdown.

    Usage:

    >>> collapse("Label", "text")
    '**Label**\n<details>\n<p>\n\ntext\n\n</p>\n</details>'

    Parameters
    ----------
    summary
    content

    Returns
    -------

    """
    # return f"<details>\n<summary>{summary}</summary>\n<p>\n\n{content}\n\n</p>\n</details>"
    return f"**{summary}**\n<details>\n<p>\n\n{content}\n\n</p>\n</details>"
    # return f"**{summary}**\n<p>\n\n{content}\n\n</p>"


def codify(text):
    """
    Usage:
    >>> print(codify("text"))
    ```python3
    text
    """
    return '```python3\n' + text


def output(text):
    '''
    Usage:

    >>> print(output("text"))  # doctest: +NORMALIZE_WHITESPACE
    """
    text"""
    ```
    '''
    if text:
        return '"""\n' + text + '"""\n```'
    else:
        return '```'


def rewrite(input_file, scripts_folder, output_file):
    """ Check existence of README-edit.md at the provided folder.

    Usage:
        >>> rewrite("README-edit.md", "examples", "README.md")
        Traceback (most recent call last):
        Exception: ('input_file not found:', 'README-edit.md')
    """
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
        code = code[1:]

        # Handle each code segment separately.
        line = 0
        partial = []
        while line < len(code):
            # Read until boundary given by "# ...".
            lines = list(takewhile(lambda x: "# ..." not in x, code[line:]))

            segment = "\n".join(lines)
            print("\t\t" + "\n\t\t".join(lines))
            if segment == "":
                break
            partial.append(codify(segment))

            # Run segment and capture output.
            f = io.StringIO()
            with redirect_stdout(f):
                exec(segment)
            out = f.getvalue()
            partial.append(output(out) + "\n")

            line += len(lines) + 1
        txt = txt.replace(tag, collapse(title, "\n".join(partial)))
    with open(output_file, "w") as f:
        f.write(txt)
        print("\t", output_file, "written!")
