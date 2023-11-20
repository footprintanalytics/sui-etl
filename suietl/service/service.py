import pydash
from base.service.service import BaseService


class Service(BaseService):

    def get_checkpoints(self, block_number, intervals):
        res = self.rpc.get_checkpoints(block_number, intervals)
        if 'error' in res:
            print(res['error'])
        assert 'error' not in res, res['error']
        return res['result']['data']

    def get_checkpoint(self, block_number):
        res = self.rpc.get_checkpoint(block_number)
        if 'error' in res:
            print(res['error'])
        assert 'error' not in res, res['error']
        return res['result']

    def get_checkpoint_timestamp(self, block_number):
        return block_number, int(self.get_checkpoint(block_number)['timestampMs'])/1000

    def get_genesis_checkpoint_timestamp(self):
        return 1, int(self.get_checkpoint(1)['timestampMs'])/1000

    def get_latest_checkpoint_timestamp(self):
        number = self.rpc.get_latest_checkpoint_number()['result']
        number = int(number)
        return number, int(self.get_checkpoint(number)['timestampMs'])/1000

    def transaction_blocks(self, all_txs):
        tx_blocks = self.rpc.get_transaction_blocks(all_txs)
        assert 'error' not in tx_blocks, tx_blocks['error']
        return tx_blocks['result']

    def get_past_objects(self, object_ids):
        return self.rpc.get_past_objects(object_ids)

    def get_objects(self, object_ids):
        return self.rpc.get_objects(object_ids)



