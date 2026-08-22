"""CLI interface for file organizer."""

import click


@click.command()
@click.argument("source_dir")
@click.option("--dry-run", is_flag=True, help="Preview changes without moving files")
@click.option("--verbose", "-v", is_flag=True, help="Print detailed output")
def main(source_dir: str, dry_run: bool, verbose: bool):
    """Organize files in a directory by type."""
    from .organizer import organize_files

    if dry_run:
        click.echo("DRY RUN - No files will be moved\n")

    try:
        result = organize_files(source_dir, dry_run=dry_run, verbose=verbose)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    except NotADirectoryError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if not result:
        click.echo("No files to organize.")
        return

    total = sum(len(files) for files in result.values())
    click.echo(f"\n{'Would organize' if dry_run else 'Organized'} {total} files:")

    for category, files in sorted(result.items()):
        click.echo(f"  {category}/ ({len(files)} files)")


if __name__ == "__main__":
    main()
