import click
from helpers import libvirt


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("save-fixed-usb")
def save_fixed_usb():
    libvirt.save_fixed_usb()


if __name__ == '__main__':
    cli(obj={})
