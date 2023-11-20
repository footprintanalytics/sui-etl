import click

from suietl.jobs.export_checkpoints_job import ExportCheckpointsJob
from suietl.jobs.exporters.checkpoints_item_exporter import checkpoints_item_exporter
from suietl.providers.auto import get_multi_provider_from_uris
from suietl.providers.multi_batch_rpc import EndpointManager
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-checkpoint', default=0, type=int, help='Start checkpoint')
@click.option('-e', '--end-checkpoint', required=True, type=int, help='End checkpoint')
@click.option('-b', '--batch-size', default=100, show_default=True, type=int, help='The number of blocks to export at a time.')
@click.option('-p', '--provider-uri', type=str, help='The URI of the remote Sui node')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--checkpoint-output', default=None, type=str,
              help='The output file for checkpoint. If not provided checkpoints will not be exported. Use "-" for stdout')
def export_checkpoints(start_checkpoint, end_checkpoint, batch_size, provider_uri, max_workers, checkpoint_output):
    """Export checkpointss, transactions and actions."""

    if checkpoint_output is None:
        raise ValueError('Sui --checkpoint_output options must be provided')

    endpoint_manager = EndpointManager(provider_uri.split(','))

    job = ExportCheckpointsJob(
        start_checkpoint=start_checkpoint,
        end_checkpoint=end_checkpoint,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_multi_provider_from_uris(provider_uri, endpoint_manager=endpoint_manager, batch=True)),
        max_workers=max_workers,
        item_exporter=checkpoints_item_exporter(checkpoint_output),
        export_checkpoints=checkpoint_output is not None,
    )
    job.run()
