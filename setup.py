# -*- coding: utf-8 -*-
"""NOTICE: This file was generated automatically by the command: xpoetry setup-py."""
from distutils.core import setup

packages = ["flake8_nitpick", "flake8_nitpick.files"]

package_data = {"": ["*"]}

install_requires = ["attrs", "dictdiffer", "flake8>=3.0.0", "pyyaml", "requests", "toml"]

entry_points = {"flake8.extension": ["NIP = flake8_nitpick.plugin:NitpickChecker"]}

setup_kwargs = {
    "name": "flake8-nitpick",
    "version": "0.7.1",
    "description": "Flake8 plugin to enforce the same lint configuration (flake8, isort, mypy, pylint) across multiple Python projects",
    "long_description": '# flake8-nitpick\n\n<a href="https://pypi.python.org/pypi/flake8-nitpick"><img alt="PyPI" src="https://img.shields.io/pypi/v/flake8-nitpick.svg"></a>\n<a href="https://travis-ci.com/andreoliwa/flake8-nitpick"><img alt="Travis CI" src="https://travis-ci.com/andreoliwa/flake8-nitpick.svg?branch=master"></a>\n<a href="https://coveralls.io/github/andreoliwa/flake8-nitpick?branch=master"><img alt="Coveralls" src="https://coveralls.io/repos/github/andreoliwa/flake8-nitpick/badge.svg?branch=master"></a>\n\nFlake8 plugin to enforce the same lint configuration (flake8, isort, mypy, pylint) across multiple Python projects.\n\nA "nitpick code style" is a [TOML](https://github.com/toml-lang/toml) file with settings that should be present in config files from other tools. E.g.:\n\n- `pyproject.toml` and `setup.cfg` (used by [flake8](http://flake8.pycqa.org/), [black](https://black.readthedocs.io/), [isort](https://isort.readthedocs.io/), [mypy](https://mypy.readthedocs.io/));\n- `.pylintrc` (used by [pylint](https://pylint.readthedocs.io/) config);\n- more files to come.\n\n---\n\n- [Installation and usage](#installation-and-usage)\n- [Style file](#style-file)\n- [setup.cfg](#setupcfg)\n\n---\n\n## Installation and usage\n\nSimply install the package (in a virtualenv or globally, wherever) and run `flake8`:\n\n    $ pip install -U flake8-nitpick\n    $ flake8\n\nYou will see warnings if your project configuration is different than [the default style file](https://raw.githubusercontent.com/andreoliwa/flake8-nitpick/master/nitpick-style.toml).\n\n## Style file\n\n### Configure your own style file\n\nChange your project config on `pyproject.toml`, and configure your own style like this:\n\n    [tool.nitpick]\n    style = "https://raw.githubusercontent.com/andreoliwa/flake8-nitpick/master/nitpick-style.toml"\n\nYou can set `style` with any local file or URL. E.g.: you can use the raw URL of a [GitHub Gist](https://gist.github.com).\n\n### Default search order for a style file\n\n1. A file or URL configured in the `pyproject.toml` file, `[tool.nitpick]` section, `style` key, as [described above](#configure-your-own-style-file).\n\n2. Any `nitpick-style.toml` file found in the current directory (the one in which `flake8` runs from) or above.\n\n3. If no style is found, then [the default style file from GitHub](https://raw.githubusercontent.com/andreoliwa/flake8-nitpick/master/nitpick-style.toml) is used.\n\n### Style file syntax\n\nA style file contains basically the configuration options you want to enforce in all your projects.\n\nThey are just the config to the tool, prefixed with the name of the config file.\n\nE.g.: To [configure the black formatter](https://github.com/ambv/black#configuration-format) with a line length of 120, you use this in your `pyproject.toml`:\n\n    [tool.black]\n    line-length = 120\n\nTo enforce that all your projects use this same line length, add this to your `nitpick-style.toml` file:\n\n    ["pyproject.toml".tool.black]\n    line-length = 120\n\nIt\'s the same exact section/key, just prefixed with the config file name (`"pyproject.toml".`)\n\nThe same works for `setup.cfg`.\nTo [configure mypy](https://mypy.readthedocs.io/en/latest/config_file.html#config-file-format) to ignore missing imports in your project:\n\n    [mypy]\n    ignore_missing_imports = true\n\nTo enforce all your projects to ignore missing imports, add this to your `nitpick-style.toml` file:\n\n    ["setup.cfg".mypy]\n    ignore_missing_imports = true\n\n### Absent files\n\nTo enforce that certain files should not exist in the project, you can add them to the style file.\n\n    [[files.absent]]\n    file = "myfile1.txt"\n\n    [[files.absent]]\n    file = "another_file.env"\n    message = "This is an optional extra string to display after the warning"\n\nMultiple files can be configured as above.\nThe `message` is optional.\n\n## setup.cfg\n\n### Comma separated values\n\nOn `setup.cfg`, some keys are lists of multiple values separated by commas, like `flake8.ignore`.\n\nOn the style file, it\'s possible to indicate which key/value pairs should be treated as multiple values instead of an exact string.\nMultiple keys can be added.\n\n    ["setup.cfg"]\n    comma_separated_values = ["flake8.ignore", "isort.some_key", "another_section.another_key"]\n',
    "author": "W. Augusto Andreoli",
    "author_email": "andreoliwa@gmail.com",
    "url": "https://github.com/andreoliwa/flake8-nitpick",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.6,<4.0",
}


setup(**setup_kwargs)  # type: ignore
