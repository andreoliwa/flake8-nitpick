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
import click

from nitpick import Nitpick


@click.command()
@click.option(
    "--check",
    "-c",
    is_flag=True,
    default=False,
    help="Don't modify the configuration files, just print the difference."
    " Return code 0 means nothing would change. Return code 1 means some files would be modified.",
)
# FIXME[AA]: add offline option
def nitpick_cli(check=False):
    """Enforce the same configuration across multiple projects."""
    Nitpick(check=check).cli_debug_info()
    # FIXME[AA]: follow steps of NitpickExtension.run()
