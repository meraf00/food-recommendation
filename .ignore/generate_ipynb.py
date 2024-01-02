import os
import json


def create_cell(source, cell_type="code", execution_count=1, outputs=[]):
    return {
        "cell_type": cell_type,
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs,
        "source": source,
    }


def convert(filename):
    sources = []

    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                if line.startswith("# In["):
                    sources.append([])
                else:
                    sources.append([line])
            elif line.strip():
                sources[-1].append(line)

    template = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.6",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    for execution_count, source in enumerate(sources):
        if source:
            template["cells"].append(create_cell(source, execution_count=execution_count))

    with open(filename.replace(".py", "_ipynb.ipynb"), "w") as f:
        f.write(json.dumps(template))


files = os.listdir()

ignore = ["generate_ipynb.py", "generate_py.py"]

for filename in files:
    if filename.endswith(".py") and filename not in ignore:
        convert(filename)
