import json

from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob

from suietl.json_rpc_requests import generate_get_tx_json_rpc
from suietl.mappers.event_mapper import EventMapper
from suietl.mappers.move_call_mapper import MoveCallMapper
from suietl.mappers.object_mapper import ObjectMapper
from suietl.mappers.payment_mapper import PaymentMapper
from suietl.mappers.transaction_block_mapper import TransactionBlockMapper
from suietl.utils import rpc_response_batch_to_results


# from suietl.service.service import Service


class ExportTransactionBlocksJob(BaseJob):
    def __init__(
            self,
            transaction_block_digest_iterable,
            batch_size,
            batch_web3_provider,
            max_workers,
            item_exporter,
            export_events=True,
            export_transaction_blocks=True,
            export_payments=True,
            export_move_calls=True,
            export_objects=True
    ):

        self.transaction_block_digest_iterable = transaction_block_digest_iterable

        self.item_exporter = item_exporter
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)

        self.batch_web3_provider = batch_web3_provider

        self.export_transaction_blocks = export_transaction_blocks
        self.export_events = export_events
        self.export_payments = export_payments
        self.export_move_calls = export_move_calls
        self.export_objects = export_objects
        if not self.export_transaction_blocks and not self.export_events:
            raise ValueError('At least one of export_transaction_blocks or export_events')

        self.transaction_block_mapper = TransactionBlockMapper
        self.event_mapper = EventMapper
        self.payment_mapper = PaymentMapper
        self.object_mapper = ObjectMapper
        self.move_call_mapper = MoveCallMapper

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(self.transaction_block_digest_iterable, self._export_transaction_blocks)

    def _export_transaction_blocks(self, transaction_hashes):
        tx_rpc = generate_get_tx_json_rpc(transaction_hashes)
        response, endpoint_url = self.batch_web3_provider.make_batch_request(json.dumps(tx_rpc))
        tx_blocks = rpc_response_batch_to_results(response)
        for tx_block in tx_blocks:
            self._export_transaction_block(tx_block)

    def _export_transaction_block(self, transaction_blocks):
        if self.export_transaction_blocks:
            tx_block = self.transaction_block_mapper.from_dict(transaction_blocks)
            self.item_exporter.export_item(tx_block.to_dict())
        if self.export_events:
            for event in transaction_blocks['events']:
                _event = self.event_mapper.from_dict(event, transaction_blocks)
                self.item_exporter.export_item(_event.to_dict())
        if self.export_payments:
            for index, payment in enumerate(transaction_blocks["transaction"]["data"]["gasData"]["payment"]):
                _payment = self.payment_mapper.from_dict(payment, index, transaction_blocks)
                self.item_exporter.export_item(_payment.to_dict())
        if self.export_move_calls:
            # print('====transaction_blocks["transaction"]["data"]===', transaction_blocks["transaction"]["data"])
            if transaction_blocks["transaction"]["data"]['transaction'].get('kind') == 'ProgrammableTransaction':
                for index, tx in enumerate(transaction_blocks["transaction"]["data"]['transaction']["transactions"]):
                    if list(tx.keys())[0] == 'MoveCall':
                        _tx = self.move_call_mapper.from_dict(tx['MoveCall'], index, transaction_blocks)
                        self.item_exporter.export_item(_tx.to_dict())
    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
