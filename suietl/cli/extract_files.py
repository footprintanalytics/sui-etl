import click

from suietl import misc_utils


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', '--input', default='-', show_default=True, type=str,
              help='The input file. If not specified stdin is used.')
@click.option('-o', '--output', default='-', show_default=True, type=str,
              help='The output file. If not specified stdout is used.')
@click.option('-f', '--field', required=True, type=str, help='The field name to extract.')
def extract_field_file(input, output, field):
    """Extracts field from given CSV or JSON newline-delimited file."""
    misc_utils.extract_field(input, output, field)



