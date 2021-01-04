![test](https://github.com/davips/autoreadme/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/autoreadme/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/autoreadme)

# autoreadme
Generate READMEs with collapsable* code and corresponding output from Python.

# Install
```bash
pip install autoreadme
autoreadme
```

# Example
A typical *README-edit.md* file would be:

```markdown
# Uses
We can cook using the following Python code:
<<cook>>

However, we can also clean:
<<clean>>
```

The example file (given in this repo as *examples/README-edit.md*) depends on two scripts.
Each script should have a `# ...` line where the output until that moment is expected to appear:

*examples/cook.py*:
```python3
# Cooking
x = 2 * 8
print("This script prints something:", x)
# ...
```

*examples/clean.py*:
```python3
# Cleaning
y = 34 % 5
print("this script prints another thing.", y)
# ...
```

Running...
```bash
autoreadme -i examples/README-edit.md -s examples/ -o examples/README.md examples/README-edit.md
```
...will result in the following markdown:


<blockquote>
# Uses

We can cook using the following Python code:

**Cooking**
<details>
<p>

```python3
x = 2 * 8
print("This script prints something:", x)
```

```
This script prints something: 16
```

</p>
</details>

However, we can also clean:

**Cleaning** 
<details>
<p>

```python3
y = 34 % 5
print("this script prints another thing.", y)
```

```
this script prints another thing. 4
```

</p>
</details>
</blockquote>
