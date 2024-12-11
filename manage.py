import os
import click
from alembic import command
from alembic.config import Config

# Path to your alembic.ini configuration file
alembic_cfg_path = "alembic.ini"

# Create a CLI group
@click.group()
def cli():
    # CLI for managing migrations.
    pass


@cli.command()
def runserver():
    """Run the FastAPI server."""
    click.echo("Starting FastAPI server...")
    os.system("poetry run fastapi dev app/main.py --port 8000")
# Command to generate migrations
@cli.command()
def generate_migrations():
    # Generate a new migration
    alembic_cfg = Config(alembic_cfg_path)
    command.revision(alembic_cfg, autogenerate=True)

# Command to upgrade the database
@cli.command()
def migrate():
    # Apply migrations.
    alembic_cfg = Config(alembic_cfg_path)
    command.upgrade(alembic_cfg, "head")
    click.echo("Migrations applied successfully.")

# Command to downgrade the database
@cli.command()
def downgrade():
    """Revert last migration."""
    alembic_cfg = Config(alembic_cfg_path)
    command.downgrade(alembic_cfg, "-1")

# Command to reset the database
@cli.command()
def reset_database():
    """Reset the database to its initial state."""
    alembic_cfg = Config(alembic_cfg_path)
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
    click.echo("Database reset successfully.")

if __name__ == "__main__":
    cli()
