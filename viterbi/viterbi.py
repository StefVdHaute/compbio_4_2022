from typing import List, Dict, Tuple


def argmax(param) -> Tuple[int, int]:
    it = param.__iter__()
    m = it.__next__()
    index = 0

    for i, var in enumerate(it, start=1):
        if var > m:
            m = var
            index = i

    return index, m


def viterbi(  # unfinished
        path: str, mapping: Dict[str, int], hidden_mapping: Dict[str, int],
        transition_matrix: List[List[float]],
        emission_matrix: List[List[float]]
) -> str:
    # trellis = []  # matrix(len(S), len(O))  # To hold p. of each state given each observation.
    # pointers = []  # matrix(len(S), len(O)) # To hold backpointer to best prior state
    #
    # # Determine each hidden state's p. at time 0...
    # for s in range(len(hidden_mapping)):
    #     trellis.append([emission_matrix[mapping[path[0]]][s] * emission_matrix[s][mapping[path[0]]]])
    #     for o in range(1, len(path)):
    #         pointers.append([])
    #
    # # ...and afterwards, tracking each state's most likely prior state, k.
    # for o in range(1, len(path)):
    #     for s in range(len(hidden_mapping)):
    #         k = argmax(trellis[k][o - 1] * transition_matrix[k][s] * emission_matrix[s][mapping[path[o]]]
    #                    for k in range(len(trellis)))
    #         trellis[s][o] = trellis[k][o - 1] * transition_matrix[k][s] * emission_matrix[s][mapping[path[o]]]
    #         pointers[s][o] = k
    #
    # best_path = list()
    # k = argmax(trellis[k][len(path) - 1] for k in range(len(trellis)))  # Find k of best final state
    # for o in range(len(path) - 1, -1, -1):  # Backtrack from last observation.
    #     best_path.insert(0, hidden_mapping[k])  # Insert previous state on most likely path
    #     k = pointers[k][o]  # Use backpointer to find best previous state
    # return "".join(best_path)

    trellis = []
    pointers = []
    o = len(path) + 1
    initial_prob = emission_matrix[mapping[path[0]]]

    for i, _ in enumerate(mapping):
        trellis.append([0] * o)
        trellis[i][0] = initial_prob[i]
        pointers.append([0] * o)

    for j, var in enumerate(path, start=1):
        for hidden_var, i in hidden_mapping.items():
            pointers[i][j], trellis[i][j] = argmax(
                trellis[k][j - 1] * transition_matrix[k][i] * emission_matrix[i][mapping[var]]
                for _, k in hidden_mapping.items())

    z = argmax(row[-1] for row in trellis)[0]
    hidden_path = (state for state, i in hidden_mapping.items() if i == z).__next__()

    for j in range(-2, -len(path) - 1, -1):
        z = pointers[z][j]
        hidden_path += (state for state, i in hidden_mapping.items() if i == z).__next__()

    return hidden_path


if __name__ == '__main__':
    viterbi('yxzxx', {'z': 2, 'x': 0, 'y': 1}, {'B': 1, 'A': 0},
            [[0.24439433296892832, 0.7556056670310717], [0.24241542404217956, 0.7575845759578205]],
            [[0.7180611502606178, 0.19057500286653098, 0.09136384687285123],
             [0.291514305851776, 0.4407137316635376, 0.26777196248468643]])
