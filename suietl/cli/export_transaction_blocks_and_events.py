import click
from blockchainetl_common.file_utils import smart_open
from blockchainetl_common.logging_utils import logging_basic_config
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

from suietl.jobs.export_transaction_blocks_job import ExportTransactionBlocksJob
from suietl.jobs.exporters.transaction_blocks_item_exporter import transaction_blocks_item_exporter
from suietl.providers.auto import get_multi_provider_from_uris
from suietl.providers.multi_batch_rpc import EndpointManager

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-t', '--transaction-block-digest', required=True, type=str,
              help='The file containing transaction hashes, one per line.')
@click.option('-p', '--provider-uri', show_default=True, type=str, help='The URI of the web3 provider ')
@click.option('-w', '--max-workers', default=5, show_default=True, type=int, help='The maximum number of workers.')
@click.option('--transaction-blocks-output', default=None, show_default=True, type=str,
              help='The output file for transaction-blocks')
@click.option('--events-output', default=None, show_default=True, type=str,
              help='The output file for events. ')
@click.option('--move-calls-output', default=None, show_default=True, type=str,
              help='The output file for move-calls. ')
@click.option('--payments-output', default=None, show_default=True, type=str,
              help='The output file for payments. ')
@click.option('--objects-output', default=None, show_default=True, type=str,
              help='The output file for objects. ')
@click.option('-b', '--batch-size', default=100, show_default=True, type=int,
              help='The number of blocks to export at a time.')
def export_transaction_blocks_and_events(
        batch_size, transaction_block_digest, provider_uri, max_workers, transaction_blocks_output,
        events_output, move_calls_output, payments_output, objects_output):
    endpoint_manager = EndpointManager(provider_uri.split(','))
    """Exports receipts and logs."""
    with smart_open(transaction_block_digest, 'r') as transaction_block_digests:
        job = ExportTransactionBlocksJob(
            transaction_block_digest_iterable=(transaction_block_digest.strip() for transaction_block_digest in
                                               transaction_block_digests),
            batch_size=batch_size,
            batch_web3_provider=ThreadLocalProxy(
                lambda: get_multi_provider_from_uris(provider_uri, endpoint_manager=endpoint_manager, batch=True)),
            max_workers=max_workers,
            item_exporter=transaction_blocks_item_exporter(transaction_blocks_output, events_output, payments_output,
                                                           move_calls_output, objects_output),
            export_transaction_blocks=transaction_blocks_output is not None,
            export_events=events_output is not None,
            export_move_calls=move_calls_output is not None,
            export_payments=payments_output is not None,
            export_objects=objects_output is not None
        )

        job.run()
