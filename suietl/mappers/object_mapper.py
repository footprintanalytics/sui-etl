import json


class ObjectMapper:
    def __init__(self, checkpoint, object_id, version, digest, _type, owner_type, owner_address, has_public_transfer,
                 storage_rebate, previous_transaction, content, bcs):
        self.checkpoint = checkpoint
        self.object_id = object_id
        self.version = version
        self.digest = digest
        self._type = _type
        self.owner_type = owner_type
        self.owner_address = owner_address
        self.has_public_transfer = has_public_transfer
        self.storage_rebate = storage_rebate
        # self.initial_shared_version = initial_shared_version
        self.previous_transaction = previous_transaction
        self.content = content
        self.bcs = bcs

    @classmethod
    def from_dict(cls, data, checkpoint):
        owner_type = list(data['owner'].keys())[0]
        owner_address = data['owner'][owner_type]
        content = data['content']['fields']['id']['id']
        bcs = data['bcs']['bcsBytes']
        return cls(
            int(checkpoint),
            data['objectId'],
            int(data['version']),
            data['digest'],
            json.dumps(data['type']),
            owner_type,
            owner_address,
            data['content']['hasPublicTransfer'],
            int(data['storageRebate']),
            data['previousTransaction'],
            content,
            bcs
        )

    def to_dict(self):
        return {
            'type': 'object',
            'checkpoint': self.checkpoint,
            'object_id': self.object_id,
            'version': self.version,
            'digest': self.digest,
            '_type': self._type,
            'owner_type': self.owner_type,
            'owner_address': self.owner_address,
            'has_public_transfer': self.has_public_transfer,
            'storage_rebate': self.storage_rebate,
            'previous_transaction': self.previous_transaction,
            'content': self.content,
            'bcs': self.bcs
        }
