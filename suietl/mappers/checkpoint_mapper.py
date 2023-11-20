from typing import List


class CheckpointMapper:
    def __init__(self, epoch: int, sequence_number: int, digest: str, network_total_transactions: int,
                 previous_digest: str, timestamp_ms: int, transactions: List[str],
                 checkpoint_commitments: List[str],
                 validator_signature: str, computation_cost: int, storage_cost: int, storage_rebate: int,
                 non_refundable_storage_fee: int):
        self.epoch = epoch
        self.sequence_number = sequence_number
        self.digest = digest
        self.network_total_transactions = network_total_transactions
        self.previous_digest = previous_digest
        self.timestamp_ms = timestamp_ms
        self.transactions = transactions
        self.checkpoint_commitments = checkpoint_commitments
        self.validator_signature = validator_signature
        self.computation_cost = computation_cost
        self.storage_cost = storage_cost
        self.storage_rebate = storage_rebate
        self.non_refundable_storage_fee = non_refundable_storage_fee

    def to_dict(self):
        return {
            "type": 'checkpoint',
            "epoch": self.epoch,
            "sequence_number": self.sequence_number,
            "digest": self.digest,
            "network_total_transactions": self.network_total_transactions,
            "previous_digest": self.previous_digest,
            "timestamp_ms": self.timestamp_ms,
            "transactions": self.transactions,
            "checkpoint_commitments": self.checkpoint_commitments,
            "validator_signature": self.validator_signature,
            "computation_cost": self.computation_cost,
            "storage_cost": self.storage_cost,
            "storage_rebate": self.storage_rebate,
            "non_refundable_storage_fee": self.non_refundable_storage_fee
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            epoch=int(data["epoch"]),
            sequence_number=int(data["sequenceNumber"]),
            digest=data["digest"],
            network_total_transactions=int(data["networkTotalTransactions"]),
            previous_digest=data["previousDigest"],
            timestamp_ms=int(data["timestampMs"]),
            transactions=data["transactions"],
            checkpoint_commitments=data["checkpointCommitments"],
            validator_signature=data["validatorSignature"],
            computation_cost=int(data["epochRollingGasCostSummary"]["computationCost"]),
            storage_cost=int(data["epochRollingGasCostSummary"]["storageCost"]),
            storage_rebate=int(data["epochRollingGasCostSummary"]["storageRebate"]),
            non_refundable_storage_fee=int(data["epochRollingGasCostSummary"]["nonRefundableStorageFee"])
        )
