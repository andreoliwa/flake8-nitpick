"""Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mnitpick` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``nitpick.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``nitpick.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import itertools
from enum import Enum

import click

from nitpick import Nitpick
from nitpick.config import Config
from nitpick.constants import ERROR_PREFIX


class NitpickFlags(Enum):
    """Flags to be used with the CLI."""

    OFFLINE = "Offline mode: no style will be downloaded (no HTTP requests at all)"


@click.command()
@click.option(f"--{NitpickFlags.OFFLINE.name.lower()}", is_flag=True, default=False, help=NitpickFlags.OFFLINE.value)
@click.option(
    "--check",
    "-c",
    is_flag=True,
    default=False,
    help="Don't modify the configuration files, just print the difference."
    " Return code 0 means nothing would change. Return code 1 means some files would be modified.",
)
def nitpick_cli(offline=False, check=False):
    """Enforce the same configuration across multiple projects."""
    from nitpick.flake8 import check_files  # pylint: disable=import-outside-toplevel

    nit = Nitpick(offline, check)
    config = Config(nit.project_root, nit.plugin_manager)
    for err in itertools.chain(config.merge_styles(), check_files(True), check_files(False)):
        click.echo(f"{ERROR_PREFIX}{err.number:03} {err.message}{err.suggestion}")
    # FIXME[AA]: replace NitpickApp by Nitpick everywhere
    # FIXME[AA]: rename Nitpick
    # FIXME[AA]: follow steps of NitpickExtension.run()
