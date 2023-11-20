
class PaymentMapper:
    def __init__(self, checkpoint, tx_digest, timestamp_ms, object_id, version, digest, payment_seq):
        self.checkpoint = checkpoint
        self.tx_digest = tx_digest
        self.timestamp_ms = timestamp_ms
        self.object_id = object_id
        self.version = version
        self.digest = digest
        self.payment_seq = payment_seq

    @classmethod
    def from_dict(cls, payment, index, tx_blocks):
        return cls(
            int(tx_blocks['checkpoint']),
            tx_blocks["digest"],
            int(tx_blocks['timestampMs']),
            payment['objectId'],
            payment['version'],
            payment['digest'],
            index
        )

    def to_dict(self):
        return {
            "type": 'payment',
            'checkpoint': self.checkpoint,
            'tx_digest': self.tx_digest,
            'timestamp_ms': self.timestamp_ms,
            'object_id': self.object_id,
            'version': self.version,
            'digest': self.digest,
            'payment_seq': self.payment_seq
        }
