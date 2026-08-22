"""CLI interface for file organizer."""

import click


CATEGORY_COLORS = {
    "images": "cyan",
    "documents": "green",
    "code": "yellow",
    "data": "blue",
    "archives": "red",
    "audio": "magenta",
    "video": "white",
    "other": "bright_black",
}


@click.command()
@click.argument("source_dir")
@click.option("--dry-run", is_flag=True, help="Preview changes without moving files")
@click.option("--verbose", "-v", is_flag=True, help="Print detailed output")
@click.option("--by-date", is_flag=True, help="Organize by modification date instead of type")
@click.option("--date-format", type=click.Choice(["year", "year-month", "full"]), default="year-month", help="Date folder format")
@click.option("--color/--no-color", default=True, help="Enable/disable colored output")
@click.option("--report", is_flag=True, help="Save a JSON report after organizing")
def main(source_dir: str, dry_run: bool, verbose: bool, by_date: bool, date_format: str, color: bool, report: bool):
    """Organize files in a directory by type or date."""
    from .organizer import generate_report, organize_by_date, organize_files, save_report

    if dry_run:
        click.echo("DRY RUN - No files will be moved\n")

    try:
        if by_date:
            result = organize_by_date(source_dir, dry_run=dry_run, verbose=verbose, date_format=date_format)
        else:
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
    action = "Would organize" if dry_run else "Organized"
    click.echo(f"\n{action} {total} files:")

    for category, files in sorted(result.items()):
        count = len(files)
        label = f"  {category}/ ({count} files)"
        if color and category in CATEGORY_COLORS:
            label = click.style(label, fg=CATEGORY_COLORS[category])
        click.echo(label)

    if report and not dry_run:
        report_path = save_report(result, source_dir)
        click.echo(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
