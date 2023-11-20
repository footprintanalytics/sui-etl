import json
import logging

from blockchainetl_common.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl_common.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter

from suietl.enumeration.entity_type import EntityType
from suietl.jobs.export_checkpoints_job import ExportCheckpointsJob
from suietl.jobs.export_transaction_blocks_job import ExportTransactionBlocksJob
from suietl.json_rpc_requests import generate_current_block_json_rpc
from suietl.streaming.eth_item_id_calculator import EthItemIdCalculator
from suietl.streaming.eth_item_timestamp_calculator import EthItemTimestampCalculator


class StreamerAdapter:
    def __init__(
            self,
            batch_web3_provider,
            item_exporter=ConsoleItemExporter(),
            batch_size=100,
            max_workers=5,
            entity_types=tuple(EntityType.ALL_FOR_STREAMING)):
        self.batch_web3_provider = batch_web3_provider
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.entity_types = entity_types
        self.item_id_calculator = EthItemIdCalculator()
        self.item_timestamp_calculator = EthItemTimestampCalculator()

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        current_block_rpc = generate_current_block_json_rpc()
        result = self.batch_web3_provider.make_batch_request(json.dumps(current_block_rpc))
        return int(result[0].get('result'))

    def export_all(self, start_block, end_block):
        # Export blocks and transactions
        checkpoints, transaction_ids = [], []
        if self._should_export(EntityType.CHECKPOINT) or self._should_export(EntityType.TRANSACTION):
            checkpoints, transaction_ids = self._export_checkpoints(start_block, end_block)

        payments, events, transactions, move_calls = [], [], [], []
        if self._should_export(EntityType.TRANSACTION):
            payments, events, transactions, move_calls = self._export_transactions_and_extend(transaction_ids)

        enriched_blocks = checkpoints \
            if EntityType.CHECKPOINT in self.entity_types else []
        enriched_transactions = transactions \
            if EntityType.TRANSACTION in self.entity_types else []
        enriched_payments = payments \
            if EntityType.TRANSACTION in self.entity_types else []
        enriched_events = events \
            if EntityType.TRANSACTION in self.entity_types else []
        enriched_move_calls = move_calls \
            if EntityType.TRANSACTION in self.entity_types else []

        logging.info('Exporting with ' + type(self.item_exporter).__name__)

        all_items = \
            sort_by(enriched_blocks, 'sequence_number') + \
            sort_by(enriched_payments, 'tx_digest') + \
            sort_by(enriched_events, 'tx_digest') + \
            sort_by(enriched_move_calls, 'tx_digest') + \
            sort_by(enriched_transactions, ('digest', 'sequence_number'))

        self.calculate_item_ids(all_items)
        self.calculate_item_timestamps(all_items)

        self.item_exporter.export_items(all_items)

    def _export_checkpoints(self, start_block, end_block):
        item_exporter = InMemoryItemExporter(item_types=['checkpoint'])
        blocks_and_transactions_job = ExportCheckpointsJob(
            start_checkpoint=start_block,
            end_checkpoint=end_block,
            batch_size=self.batch_size,
            batch_web3_provider=self.batch_web3_provider,
            max_workers=self.max_workers,
            item_exporter=item_exporter,
            export_checkpoints=self._should_export(EntityType.CHECKPOINT)
        )
        blocks_and_transactions_job.run()
        checkpoints = item_exporter.get_items('checkpoint')
        transactions = [transaction for checkpoint in checkpoints for transaction in checkpoint["transactions"]]
        return checkpoints, transactions

    def _export_transactions_and_extend(self, transaction_ids):
        exporter = InMemoryItemExporter(item_types=['payment', 'event', 'transaction', 'move_call'])
        job = ExportTransactionBlocksJob(
            transaction_block_digest_iterable=transaction_ids,
            batch_size=self.batch_size,
            batch_web3_provider=self.batch_web3_provider,
            max_workers=self.max_workers,
            item_exporter=exporter,
            export_payments=True,
            export_transaction_blocks=True,
            export_move_calls=True,
            export_objects=False,
            export_events=True
        )
        job.run()
        payments = exporter.get_items('payment')
        events = exporter.get_items('event')
        transactions = exporter.get_items('transaction')
        move_calls = exporter.get_items('move_call')
        return payments, events, transactions, move_calls

    def _should_export(self, entity_type):
        if entity_type == EntityType.CHECKPOINT:
            return True

        if entity_type == EntityType.TRANSACTION:
            return EntityType.TRANSACTION in self.entity_types

        raise ValueError('Unexpected entity type ' + entity_type)

    def calculate_item_ids(self, items):
        for item in items:
            item['item_id'] = self.item_id_calculator.calculate(item)

    def calculate_item_timestamps(self, items):
        for item in items:
            item['item_timestamp'] = self.item_timestamp_calculator.calculate(item)

    def close(self):
        self.item_exporter.close()


def sort_by(arr, fields):
    if isinstance(fields, tuple):
        fields = tuple(fields)
    return sorted(arr, key=lambda item: tuple(item.get(f) for f in fields))
