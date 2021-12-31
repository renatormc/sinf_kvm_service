import click
from helpers import libvirt


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("save-current-devices")
def save_current_devices():
    libvirt.save_exclude_devices()


if __name__ == '__main__':
    cli(obj={})
