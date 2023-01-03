import itertools


def pad_or_truncate(some_list, target_len):
    return some_list[:target_len] + [0]*(target_len - len(some_list))

def flatten_list(some_list):
    return list(itertools.chain.from_iterable(some_list))
