from blockchainetl_common.jobs.exporters.composite_item_exporter import CompositeItemExporter


def checkpoints_item_exporter(
        checkpoints_output=None
):
    filename_mapping = {}
    field_mapping = {'checkpoint': [
        'epoch',
        'sequence_number',
        'digest',
        'network_total_transactions',
        'previous_digest',
        'timestamp_ms',
        'transactions',
        'checkpoint_commitments',
        'validator_signature',
        'computation_cost',
        'storage_cost',
        'storage_rebate',
        'non_refundable_storage_fee'
    ]}

    if checkpoints_output is not None:
        filename_mapping['checkpoint'] = checkpoints_output

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
