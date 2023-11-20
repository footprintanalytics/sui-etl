import click

from suietl.jobs.export_checkpoints_job  import ExportCheckpointsJob
from suietl.jobs.exporters.checkpoints_item_exporter import checkpoints_item_exporter
from suietl.rpc.sui_rpc import SuiRpc
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-checkpoint', default=0, type=int, help='Start checkpoint')
@click.option('-e', '--end-checkpoint', required=True, type=int, help='End checkpoint')
@click.option('-p', '--provider-uri',  type=str, help='The URI of the remote Sui node')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--checkpoint-output', default=None, type=str,
              help='The output file for checkpoint. If not provided checkpoints will not be exported. Use "-" for stdout')
def export_checkpoints(start_checkpoint, end_checkpoint, provider_uri, max_workers, checkpoint_output):
    """Export checkpointss, transactions and actions."""

    if checkpoint_output is None:
        raise ValueError('Sui --checkpoint_output options must be provided')

    job = ExportCheckpointsJob(
        start_checkpoint=start_checkpoint,
        end_checkpoint=end_checkpoint,
        rpc=ThreadLocalProxy(lambda: SuiRpc(provider_uri)),
        max_workers=max_workers,
        item_exporter=checkpoints_item_exporter(checkpoint_output),
        export_checkpoints=checkpoint_output is not None,
    )
    job.run()


# if __name__ == '__main__':
#     export_checkpoints(6752575, 6838545, 'https://sui-mainnet.gateway.pokt.network/v1/lb/13ab2a666f8d9bff48fb95b0', 2, '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/sui/checkpoint_2023-07-25.json')

