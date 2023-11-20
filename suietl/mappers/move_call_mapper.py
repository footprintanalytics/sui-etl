import json


class MoveCallMapper:
    def __init__(self, checkpoint, timestamp_ms, tx_digest, move_call_seq, package, module, function, arguments):
        self.checkpoint = checkpoint
        self.timestamp_ms = timestamp_ms
        self.tx_digest = tx_digest
        self.move_call_seq = move_call_seq
        self.package = package
        self.module = module
        self.function = function
        self.arguments = arguments

    @classmethod
    def from_dict(cls, move_calls, index, tx_blocks):
        return cls(
            int(tx_blocks['checkpoint']),
            int(tx_blocks['timestampMs']),
            tx_blocks["digest"],
            index,
            move_calls['package'],
            move_calls['module'],
            move_calls['function'],
            json.dumps(move_calls.get('arguments'))
        )

    def to_dict(self):
        return {
            'type': 'move_call',
            'checkpoint': self.checkpoint,
            'timestamp_ms': self.timestamp_ms,
            'tx_digest': self.tx_digest,
            'move_call_seq': self.move_call_seq,
            'package': self.package,
            'module': self.module,
            'function': self.function,
            'arguments': self.arguments
        }

