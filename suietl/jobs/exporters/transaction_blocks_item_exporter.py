from blockchainetl_common.jobs.exporters.composite_item_exporter import CompositeItemExporter


def transaction_blocks_item_exporter(
        transaction_blocks_output=None,
        events_output=None,
        payments_output=None,
        move_calls_output=None,
        objects_output=None
):
    filename_mapping = {}
    field_mapping = {'event': [
        'epoch',
        'checkpoint',
        'timestamp_ms',
        'tx_digest',
        'event_seq',
        'package_id',
        'transaction_module',
        'sender',
        '_type',
        'parsed_json',
        'bcs'
    ], 'transaction_block':  [
        'digest',
        'timestamp_ms',
        'payment',
        'gas_owner',
        'price',
        'budget',
        'sender',
        'transaction',
        'tx_signatures',
        'len_events',
        'checkpoint',
        'message_version',
        'status',
        'gas_computation_cost',
        'gas_storage_cost',
        'gas_storage_rebate',
        'gas_non_refundable_storage_fee',
        'modified_at_versions',
        'shared_objects',
        'created',
        'mutated',
        'deleted',
        'gas_object',
        'events_digest',
        'dependencies',
        'object_change',
        'balance_change'
    ],  'move_call': [
        'checkpoint',
        'timestamp_ms',
        'tx_digest',
        'move_call_seq',
        'package',
        'module',
        'function',
        'arguments'
    ], 'payment': [
        'checkpoint',
        'tx_digest',
        'timestamp_ms',
        'object_id',
        'version',
        'digest',
        'payment_seq'
    ], 'object': [
        'checkpoint',
        'object_id',
        'version',
        'digest',
        '_type',
        'owner_type',
        'owner_address',
        'has_public_transfer',
        'storage_rebate',
        'previous_transaction',
        'content',
        'bcs'
    ]
    }

    if events_output is not None:
        filename_mapping['event'] = events_output

    if transaction_blocks_output is not None:
        filename_mapping['transaction_block'] = transaction_blocks_output

    if payments_output is not None:
        filename_mapping['payment'] = payments_output

    if move_calls_output is not None:
        filename_mapping['move_call'] = move_calls_output

    if objects_output is not None:
        filename_mapping['object'] = objects_output

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
