# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import itertools
from collections import defaultdict


def join(left, right, join_fields, left_fields, right_fields):
    left_join_field, right_join_field = join_fields

    def field_list_to_dict(field_list):
        result_dict = {}
        for field in field_list:
            if isinstance(field, tuple):
                result_dict[field[0]] = field[1]
            else:
                result_dict[field] = field
        return result_dict

    left_fields_as_dict = field_list_to_dict(left_fields)
    right_fields_as_dict = field_list_to_dict(right_fields)

    left_map = defaultdict(list)
    for item in left: left_map[item[left_join_field]].append(item)

    right_map = defaultdict(list)
    for item in right: right_map[item[right_join_field]].append(item)

    for key in left_map.keys():
        for left_item, right_item in itertools.product(left_map[key], right_map[key]):
            result_item = {}
            for src_field, dst_field in left_fields_as_dict.items():
                result_item[dst_field] = left_item.get(src_field)
            for src_field, dst_field in right_fields_as_dict.items():
                result_item[dst_field] = right_item.get(src_field)

            yield result_item


def enrich_transactions(transactions, receipts):
    result = list(join(
        transactions, receipts, ('transaction_hash', 'transaction_hash'),
        left_fields=[
            'type',
            'block_timestamp',
            'block_number',
            'block_hash',
            'transaction_hash',
            '_type',
            'version',
            'max_fee',
            'sender_address',
            'chain_id',
            'contract_class',
            'compiled_class_hash',
            'class_hash',
            "constructor_calldata",
            "contract_address_salt",
            "contract_address",
            "signature",
            "nonce",
            "entry_point_selector",
            "calldata",
            "transaction_index"
        ],
        right_fields=[
            "actual_fee",
            "event_count",
            "messages_sent_count",
            "status",
            ('contract_address', 'receipt_contract_address')
        ]))

    if len(result) != len(transactions):
        raise ValueError('The number of transactions is wrong ' + str(result))

    # fix
    for item in result:
        receipt_contract_address = item.pop('receipt_contract_address')
        if item['_type'] in {'DEPLOY_ACCOUNT', 'DEPLOY'}:
            item['contract_address'] = receipt_contract_address
    return result


def enrich_logs(blocks, logs):
    result = list(join(
        logs, blocks, ('block_number', 'number'),
        [
            'type',
            'log_index',
            'transaction_hash',
            'transaction_index',
            'address',
            'data',
            'topics',
            'block_number'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(logs):
        raise ValueError('The number of logs is wrong ' + str(result))

    return result


def enrich_events(blocks, events):
    result = list(join(
        events, blocks, ('block_number', 'block_number'),
        [
            'type',
            'transaction_hash',
            'block_hash',
            'block_number',
            'data',
            'from_address',
            'keys',
            'event_index'
        ],
        [
            'block_timestamp'
        ]))

    if len(result) != len(events):
        raise ValueError('The number of events is wrong ' + str(result))

    return result


def enrich_messages(blocks, messages):
    result = list(join(
        messages, blocks, ('block_number', 'block_number'),
        [
            'type',
            'transaction_hash',
            'block_hash',
            'block_number',
            'from_address',
            'to_address',
            'payload',
            '_type',
            ('L2ToL1', 'direction')
        ],
        [
            'block_timestamp'
        ]))

    if len(result) != len(messages):
        raise ValueError('The number of messages is wrong ' + str(result))

    for item in result:
        item['direction'] = 'L2ToL1'

    return result


def enrich_token_transfers(blocks, token_transfers):
    result = list(join(
        token_transfers, blocks, ('block_number', 'block_number'),
        [
            'type',
            'transaction_hash',
            'block_hash',
            'block_number',
            'from_address',
            'to_address',
            'contract_address',
            'value',
            'event_index',
        ],
        [
            ('block_timestamp', 'block_timestamp')
        ]))

    if len(result) != len(token_transfers):
        raise ValueError('The number of token transfers is wrong ' + str(result))

    return result


def enrich_traces(blocks, traces):
    result = list(join(
        traces, blocks, ('block_number', 'block_number'),
        [
            'type',
            'transaction_index',
            'from_address',
            'to_address',
            'value',
            'input',
            'output',
            'trace_type',
            'call_type',
            'reward_type',
            'gas',
            'gas_used',
            'subtraces',
            'trace_address',
            'error',
            'status',
            'transaction_hash',
            'block_number',
            'trace_id',
            'trace_index'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(traces):
        raise ValueError('The number of traces is wrong ' + str(result))

    return result


def enrich_contracts(blocks, contracts):
    result = list(join(
        contracts, blocks, ('block_number', 'number'),
        [
            'type',
            'address',
            'bytecode',
            'function_sighashes',
            'is_erc20',
            'is_erc721',
            'block_number'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(contracts):
        raise ValueError('The number of contracts is wrong ' + str(result))

    return result


def enrich_tokens(blocks, tokens):
    result = list(join(
        tokens, blocks, ('block_number', 'number'),
        [
            'type',
            'address',
            'symbol',
            'name',
            'decimals',
            'total_supply',
            'block_number'
        ],
        [
            ('timestamp', 'block_timestamp'),
            ('hash', 'block_hash'),
        ]))

    if len(result) != len(tokens):
        raise ValueError('The number of tokens is wrong ' + str(result))

    return result
