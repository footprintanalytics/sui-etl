from suietl.mappers.checkpoint_mapper import CheckpointMapper
from suietl.service.service import Service
from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob
from blockchainetl_common.utils import validate_range
from util.common_function import split


class ExportCheckpointsJob(BaseJob):
    def __init__(
            self,
            start_checkpoint,
            end_checkpoint,
            rpc,
            max_workers,
            item_exporter,
            batch_size=100,
            export_checkpoints=True):
        validate_range(start_checkpoint, end_checkpoint)
        self.start_checkpoint = start_checkpoint
        self.end_checkpoint = end_checkpoint
        self.batch_size = batch_size
        self.batch_work_executor = BatchWorkExecutor(1, max_workers)  # 这里因为sui有自带的batch功能, 这里默认size为1
        self.item_exporter = item_exporter

        self.export_checkpoints = export_checkpoints
        if not self.export_checkpoints :
            raise ValueError('At least one of export_checkpoints')

        self.service = Service(rpc)
        self.checkpoint_mapper = CheckpointMapper

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        split_point = split(self.start_checkpoint, self.end_checkpoint, self.batch_size)
        self.batch_work_executor.execute(
            split_point,
            self._export_batch,
            total_items=len(split_point)
        )

    def _export_batch(self, arg: list):
        start_point, end_point, intervals = arg[0]
        checkpoints = self.service.get_checkpoints(start_point, intervals=intervals)
        for checkpoint in checkpoints:
            self._export_checkpoint(checkpoint)

    def _export_checkpoint(self, checkpoint):
        if self.export_checkpoints:
            checkpoint = self.checkpoint_mapper.from_dict(checkpoint)
            self.item_exporter.export_item(checkpoint.to_dict())

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
