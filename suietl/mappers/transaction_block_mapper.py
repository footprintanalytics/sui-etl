import json


class TransactionBlockMapper:
    def __init__(self, digest, timestamp_ms, payment, gas_owner, price, budget, sender, transaction, tx_signatures,
                 len_events, checkpoint, message_version, status, gas_computation_cost, gas_storage_cost,
                 gas_storage_rebate, gas_non_refundable_storage_fee, modified_at_versions, shared_objects, created,
                 mutated, deleted, gas_object, events_digest, dependencies, object_change, balance_change):
        self.digest = digest
        self.timestamp_ms = timestamp_ms
        self.payment = payment
        self.gas_owner = gas_owner
        self.price = price
        self.budget = budget
        self.sender = sender
        self.transaction = transaction
        self.tx_signatures = tx_signatures
        self.len_events = len_events
        self.checkpoint = checkpoint
        self.message_version = message_version
        self.status = status
        self.gas_computation_cost = gas_computation_cost
        self.gas_storage_cost = gas_storage_cost
        self.gas_storage_rebate = gas_storage_rebate
        self.gas_non_refundable_storage_fee = gas_non_refundable_storage_fee
        self.modified_at_versions = modified_at_versions
        self.shared_objects = shared_objects
        self.created = created
        self.mutated = mutated
        self.deleted = deleted
        self.gas_object = gas_object
        self.events_digest = events_digest
        self.dependencies = dependencies
        self.object_change = object_change
        self.balance_change = balance_change

    def to_dict(self):
        return {
            'type': 'transaction',
            "digest": self.digest,
            "timestamp_ms": self.timestamp_ms,
            "payment": self.payment,
            "gas_owner": self.gas_owner,
            "price": self.price,
            "budget": self.budget,
            "sender": self.sender,
            "transaction": self.transaction,
            "tx_signatures": self.tx_signatures,
            "len_events": self.len_events,
            "checkpoint": self.checkpoint,
            "message_version": self.message_version,
            "status": self.status,
            "gas_computation_cost": self.gas_computation_cost,
            "gas_storage_cost": self.gas_storage_cost,
            "gas_storage_rebate": self.gas_storage_rebate,
            "gas_non_refundable_storage_fee": self.gas_non_refundable_storage_fee,
            "modified_at_versions": self.modified_at_versions,
            "shared_objects": self.shared_objects,
            "created": self.created,
            "mutated": self.mutated,
            "deleted": self.deleted,
            "gas_object": self.gas_object,
            "events_digest": self.events_digest,
            "dependencies": self.dependencies,
            "object_change": self.object_change,
            "balance_change": self.balance_change
        }

    @classmethod
    def from_dict(cls, tx_blocks):
        return cls(
            tx_blocks["digest"],
            int(tx_blocks["timestampMs"]),
            [json.dumps(item) for item in tx_blocks["transaction"]["data"]["gasData"]["payment"]],
            tx_blocks["transaction"]["data"]["gasData"]["owner"],
            int(tx_blocks["transaction"]["data"]["gasData"]["price"]),
            int(tx_blocks["transaction"]["data"]["gasData"]["budget"]),
            tx_blocks["transaction"]["data"]["sender"],
            json.dumps(tx_blocks["transaction"]["data"]["transaction"]),
            tx_blocks["transaction"]["txSignatures"],
            len(tx_blocks['events']),
            int(tx_blocks["checkpoint"]),
            tx_blocks["transaction"]["data"]["messageVersion"],
            tx_blocks["effects"]["status"]["status"],
            int(tx_blocks["effects"]["gasUsed"]["computationCost"]),
            int(tx_blocks["effects"]["gasUsed"]["storageCost"]),
            int(tx_blocks["effects"]["gasUsed"]["storageRebate"]),
            int(tx_blocks["effects"]["gasUsed"]["nonRefundableStorageFee"]),
            [json.dumps(item) for item in tx_blocks["effects"]["modifiedAtVersions"]],
            [json.dumps(item) for item in tx_blocks["effects"].get("sharedObjects", [])],
            [json.dumps(item) for item in tx_blocks["effects"].get("created", [])],
            [json.dumps(item) for item in tx_blocks["effects"].get("mutated", [])],
            [json.dumps(item) for item in tx_blocks["effects"].get("deleted", [])],
            json.dumps(tx_blocks["effects"]["gasObject"]),
            tx_blocks["effects"].get("eventsDigest"),
            tx_blocks["effects"]["dependencies"],
            [json.dumps(item) for item in tx_blocks.get("objectChanges", [])],
            [json.dumps(item) for item in tx_blocks.get("balanceChanges", [])]
        )
