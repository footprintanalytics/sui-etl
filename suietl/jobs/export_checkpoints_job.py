import json

from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob
from blockchainetl_common.utils import validate_range

from base.misc.retriable_value_error import RetriableValueError
from suietl.json_rpc_requests import generate_get_block_by_number_json_rpc
from suietl.mappers.checkpoint_mapper import CheckpointMapper
from suietl.utils import rpc_response_batch_to_results


# from util.common_function import split


class ExportCheckpointsJob(BaseJob):
    def __init__(
            self,
            start_checkpoint,
            end_checkpoint,
            batch_web3_provider,
            max_workers,
            item_exporter,
            batch_size=100,
            export_checkpoints=True):
        self.start_block = start_checkpoint
        self.end_block = end_checkpoint
        validate_range(start_checkpoint, end_checkpoint)
        self.start_checkpoint = start_checkpoint
        self.end_checkpoint = end_checkpoint

        # self.batch_size = batch_size
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter
        self.batch_web3_provider = batch_web3_provider

        self.export_checkpoints = export_checkpoints
        if not self.export_checkpoints:
            raise ValueError('At least one of export_checkpoints')

        self.checkpoint_mapper = CheckpointMapper

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        start_block, end_block = block_number_batch[0], block_number_batch[-1]
        blocks_rpc = generate_get_block_by_number_json_rpc(start_block, end_block)
        response, endpoint_url = self.batch_web3_provider.make_batch_request(json.dumps(blocks_rpc))
        result = rpc_response_batch_to_results(response)
        checkpoints = result.get('data')
        if checkpoints is None:
            error_message = 'data is None in response {}.'.format(response)
            raise RetriableValueError(error_message)
        for checkpoint in checkpoints:
            self._export_checkpoint(checkpoint)

    def _export_checkpoint(self, checkpoint):
        if self.export_checkpoints:
            checkpoint = self.checkpoint_mapper.from_dict(checkpoint)
            self.item_exporter.export_item(checkpoint.to_dict())

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
