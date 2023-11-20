def special_chain_task(chain: str, task: str):
    # return (chain in ['arbitrum', 'harmony'] and task == 'transactions') or (chain in ['thunder_core'] and task == 'blocks') or (chain in ['fantom'] and task == 'traces')
    return chain in ['fantom'] and task == 'traces'
