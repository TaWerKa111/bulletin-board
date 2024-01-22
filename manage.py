import click
from app.management.create import create_superuser


@click.group()
def cli():
    pass


cli.add_command(create_superuser)


if __name__ == "__main__":
    cli()
