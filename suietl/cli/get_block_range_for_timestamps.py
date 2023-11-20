import click

from blockchainetl_common.file_utils import smart_open
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy
from suietl.rpc.sui_rpc import SuiRpc
from suietl.service.block_range_service import SuiBlockRangeService

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-p', '--provider-uri', required=True, type=str, help='The URI of tendermint RPC')
@click.option('-s', '--start-timestamp', required=True, type=int, help='Start unix timestamp, in seconds.')
@click.option('-e', '--end-timestamp', required=True, type=int, help='End unix timestamp, in seconds.')
@click.option('-o', '--output', default='-', show_default=True, type=str, help='The output file. If not specified stdout is used.')
def get_block_range_for_timestamps(provider_uri, start_timestamp, end_timestamp, output):
    """Outputs start and end blocks for given date."""

    service = SuiBlockRangeService(ThreadLocalProxy(lambda: SuiRpc(provider_uri)))

    start_block, end_block = service.get_block_range_for_timestamps(start_timestamp, end_timestamp)

    with smart_open(output, 'w') as output_file:
        output_file.write('{},{}\n'.format(start_block, end_block))

# if __name__ == '__main__':
#     get_block_range_for_timestamps('https://sui-mainnet.gateway.pokt.network/v1/lb/13ab2a666f8d9bff48fb95b0', 1688428800, 1688515200, '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/sui/block_range.txt')
