import click

from blockchainetl.file_utils import smart_open
from suietl.jobs.export_transaction_blocks_job import ExportTransactionBlocksJob
from blockchainetl.logging_utils import logging_basic_config
from ethereumetl.thread_local_proxy import ThreadLocalProxy

from suietl.jobs.exporters.transaction_blocks_item_exporter import transaction_blocks_item_exporter
from suietl.rpc.sui_rpc import SuiRpc

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-t', '--transaction-block-digest', required=True, type=str,
              help='The file containing transaction hashes, one per line.')
@click.option('-p', '--provider-uri',  show_default=True, type=str, help='The URI of the web3 provider ')
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
@click.option('-c', '--chain', default='sui', show_default=True, type=str, help='The chain network to connect to.')
def export_transaction_blocks_and_events(
        transaction_block_digest, provider_uri, max_workers, transaction_blocks_output, events_output, move_calls_output, payments_output,
                             objects_output, chain='sui'):
    """Exports receipts and logs."""
    with smart_open(transaction_block_digest, 'r') as transaction_block_digests:
        job = ExportTransactionBlocksJob(
            transaction_block_digest_iterable=(transaction_block_digest.strip() for transaction_block_digest in transaction_block_digests),
            batch_size=1,  # 由于自带并发, 默认50 ,这个参数被disable了.
            rpc=ThreadLocalProxy(lambda: SuiRpc(provider_uri)),
            max_workers=max_workers,
            item_exporter=transaction_blocks_item_exporter(transaction_blocks_output, events_output, payments_output, move_calls_output, objects_output),
            export_transaction_blocks=transaction_blocks_output is not None,
            export_events=events_output is not None,
            export_move_calls=move_calls_output is not None,
            export_payments=payments_output is not None,
            export_objects=objects_output is not None
        )

        job.run()

# if __name__ == '__main__':
#     export_transaction_blocks_and_events(
#         '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/sui/tx_2023-07-25.json',
#         'https://sui-mainnet.public.blastapi.io',
#         3,
#         '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/sui/transaction_blocks_2023-07-25.json',
#         '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/sui/events_2023-07-25.json',
#         '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/sui/move_calls_2023-07-25.json',
#         '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/sui/payments_2023-07-25.json'
#     )
