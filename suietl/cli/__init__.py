# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

import click

from suietl.cli.export_transaction_blocks_and_events import export_transaction_blocks_and_events
from suietl.cli.export_checkpoints import export_checkpoints
from suietl.cli.get_block_range_for_timestamps import get_block_range_for_timestamps
from suietl.cli.extract_files import extract_field_file as extract_field



@click.group()
@click.version_option(version='1.0.0')
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(export_transaction_blocks_and_events, "export_transaction_blocks_and_events")
cli.add_command(export_checkpoints, "export_checkpoints")

# utils
cli.add_command(get_block_range_for_timestamps, "get_block_range_for_timestamps")
cli.add_command(extract_field, "extract_field")
