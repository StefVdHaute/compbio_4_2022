from typing import Dict, List, Iterator, Iterable


def probability_path(hidden_path: Iterable, mapping: Dict[str, int], trans_matrix: List[List[float]]) -> float:
    index: int
    # I'm pretty sure that here I assume that the initial state is always a chance of 1 for the first state
    prob: float = 1

    hidden_path: Iterator = hidden_path.__iter__()
    prev_index: int = mapping.get(hidden_path.__next__())

    for var in hidden_path:
        index = mapping.get(var)
        prob *= trans_matrix[prev_index][index]

        prev_index = index

    return prob / len(mapping)
