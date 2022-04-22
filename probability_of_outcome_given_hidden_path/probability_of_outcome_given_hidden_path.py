from typing import List, Iterable, Dict, Iterator


def probability_outcome_hidden_path(
        path: Iterable, mapping: Dict[str, int],
        hidden_path: Iterable, hidden_mapping: Dict[str, int],
        emission_matrix: List[List[float]]
) -> float:
    var: str
    hidden_var: str
    prob: float = 1

    hidden_path: Iterator = hidden_path.__iter__()
    for var in path:
        hidden_var = hidden_path.__next__()

        prob *= emission_matrix[hidden_mapping.get(hidden_var)][mapping.get(var)]

    return prob
