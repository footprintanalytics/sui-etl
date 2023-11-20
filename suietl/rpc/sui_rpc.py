from base.rpc.rpc import BaseRpc


class SuiRpc(BaseRpc):
    transaction_blocks_call_limit = 50
    object_ids_call_limit = 50

    def get_checkpoints(self, number, interval=100):
        return self.call('', data={
            "jsonrpc": "2.0",
            "id": str(number - 1),
            "method": "sui_getCheckpoints",
            "params": [
                str(number - 1),
                interval,
                False
            ]
        })

    def get_checkpoint(self, number):
        return self.call('', data={
            "jsonrpc": "2.0",
            "id": str(number),
            "method": "sui_getCheckpoint",
            "params": [
                str(number)
            ]
        })

    def get_latest_checkpoint_number(self):
        return self.call('', data={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sui_getLatestCheckpointSequenceNumber",
            "params": []
        })

    def get_transaction_blocks(self, tx_digests: [str]):
        assert len(tx_digests) <= self.transaction_blocks_call_limit
        return self.call('', data=
        {
            "jsonrpc": "2.0",
            "id": str(tx_digests)[:10],
            "method": "sui_multiGetTransactionBlocks",
            "params": [
                tx_digests,
                {
                    "showInput": True,
                    "showRawInput": False,
                    "showEffects": True,
                    "showEvents": True,
                    "showObjectChanges": True,
                    "showBalanceChanges": True
                }
            ]

        })

    def get_objects(self, object_ids: [str]):
        assert len(object_ids) <= self.object_ids_call_limit
        return self.call('', data=
        {
            "jsonrpc": "2.0",
            "id": str(object_ids)[:10],
            "method": "sui_multiGetObjects",
            "params": [
                object_ids,
                {
                    "showType": True,
                    "showOwner": True,
                    "showPreviousTransaction": True,
                    "showDisplay": True,
                    "showContent": True,
                    "showBcs": True,
                    "showStorageRebate": True
                }
            ]

        })

    def get_past_objects(self, object_ids):
        assert len(object_ids) <= self.object_ids_call_limit
        return self.call('', data={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sui_tryMultiGetPastObjects",
            "params": [
                object_ids,
                {
                    "showType": True,
                    "showOwner": True,
                    "showPreviousTransaction": True,
                    "showDisplay": True,
                    "showContent": True,
                    "showBcs": True,
                    "showStorageRebate": True
                }
            ]
        })


if __name__ == '__main__':
    print(SuiRpc(provider_uri='https://sui-mainnet-rpc.nodereal.io').get_past_objects(
        [{"objectId": "0xaeab97f96cf9877fee2883315d459552b2b921edc16d7ceac6eab944dd88919c", "version": "32325351"}
         # {"objectId": "0xf9ff3ef935ef6cdfb659a203bf2754cebeb63346e29114a535ea6f41315e5a3f", "version": "6707520"}
        ]
    ))
    print(SuiRpc(provider_uri='https://sui-mainnet-rpc.nodereal.io').get_objects(
        ["0xaeab97f96cf9877fee2883315d459552b2b921edc16d7ceac6eab944dd88919c",
         "0xf9ff3ef935ef6cdfb659a203bf2754cebeb63346e29114a535ea6f41315e5a3f"]
    ))