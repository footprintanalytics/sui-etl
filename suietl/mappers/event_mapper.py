import json


class EventMapper:
    def __init__(self, tx_digest, event_seq, package_id, transaction_module, sender, type, parsed_json, bcs, checkpoint,
                 timestamp_ms):
        self.tx_digest = tx_digest
        self.event_seq = int(event_seq)
        self.package_id = package_id
        self.transaction_module = transaction_module
        self.sender = sender
        self.type = type
        self.parsed_json = parsed_json
        self.bcs = bcs
        self.checkpoint = int(checkpoint)
        self.timestamp_ms = int(timestamp_ms)

    def to_dict(self):
        return {
            "type": 'event',
            "tx_digest": self.tx_digest,
            "event_seq": self.event_seq,
            "package_id": self.package_id,
            "transaction_module": self.transaction_module,
            "sender": self.sender,
            "_type": self.type,
            "parsed_json": self.parsed_json,
            "bcs": self.bcs,
            "timestamp_ms": self.timestamp_ms,
            "checkpoint": self.checkpoint,
        }

    @classmethod
    def from_dict(cls, event, tx_blocks):
        tx_digest = event['id']['txDigest']
        event_seq = event['id']['eventSeq']
        package_id = event['packageId']
        transaction_module = event['transactionModule']
        sender = event['sender']
        type_ = event['type']
        parsed_json = json.dumps(event['parsedJson'])
        bcs = event['bcs']
        checkpoint = tx_blocks['checkpoint']
        timestamp_ms = tx_blocks['timestampMs']
        Ev = cls(tx_digest, event_seq, package_id, transaction_module, sender, type_, parsed_json, bcs, checkpoint,
                 timestamp_ms)
        return Ev
