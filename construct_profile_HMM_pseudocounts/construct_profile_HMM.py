from collections import Counter
from typing import Sequence

DELETE: int = 0
INSERT: int = 1
MATCH: int = 2
MATCH_OR_INSERT: int = 2
START: int = 2


def profile_HMM_pseudocounts(
        threshold: float, pseudocount: float, alphabet: str, patterns: list[str]
) -> tuple[dict[str, dict[str, float]], dict[str, dict[str, float]]]:
    """
    Calculates the transmission and emission matrix for a list of sequence-aligned patterns.

    :param threshold: The minimum percentage of "-" for an index over all patterns for it to be considered an insert.
    :param pseudocount: The change given to a possible path when the chance otherwise would have been 0.
    :param alphabet: All possible values excluding "-" that can be in a pattern.
    :param patterns: A list of sequence-aligned patterns.
    :return: A tuple consisting of the calculated transmission matrix and emission matrix.
    """
    transmission: dict[str, dict[str, float]] = {}
    emission: dict[str, dict[str, float]] = {"S": {alpha: 0.0 for alpha in alphabet}}

    len_patterns: int = len(patterns)
    level: int = 1  # level of the HMM

    # these 3 did not benefit from being numpy (nd)arrays
    prev_states: list[int] = [START] * len_patterns
    curr_states: list[int] = prev_states.copy()
    from_to: list[list[int]] = [[0] * 4 for __ in range(3)]

    for i in range(len(patterns[0])):
        # perhaps count nodes can be done in background for all i.
        # The background then cals count nodes with curr_states i - 1 as prev states.
        # all counters and curr_states should be kept increasing the memory requirements, especially for large patterns
        counter, curr_states = count_nodes(patterns, from_to, prev_states, i, len_patterns)

        ######################
        # Calculate matrices #
        ######################
        if counter["-"] / len_patterns > threshold:  # threshold was passed, non "-"-nodes were INSERT's
            for to_states in from_to:  # the MATCH'S need to be moved to the inserts.
                # Inserts can be repeated and these counts need to be kept
                to_states[INSERT] += to_states[MATCH_OR_INSERT]

            for j, state in enumerate(curr_states):
                if state == MATCH:  # The state should have been INSERT
                    curr_states[j] = INSERT
                else:  # state == DELETE, the previous state was preserved, instead of DELETED
                    curr_states[j] = prev_states[j]

            ###################
            # store emissions #
            ###################
            if f"I{level - 1}" not in emission:
                emission[f"I{level - 1}"] = counter.copy()
            else:
                emission[f"I{level - 1}"].update(counter)
        else:  # threshold wasn't passed, non "-"-nodes were MATCH's
            # almost everything in this else can be done at any point in the algorithm as soon as the data is available.
            # This means that parallelization might be beneficial. However, not on data of this size.

            # calculate emissions with previous counts
            emission[f"M{level}"], emission[f"I{level - 1}"] = (
                calc_emissions(counter, alphabet, pseudocount,
                               # ins_counter only exists if f"I{level - 1}" in emission
                               ins_counter=emission[f"I{level - 1}"] if f"I{level - 1}" in emission else None))

            denominator = 1 + 3 * pseudocount
            ###########################
            # calculate transmissions #
            ###########################
            if level > 1:  # default calculation
                for from_state, to_states in enumerate(from_to):
                    s: str = get_state_str(from_state, level - 1)

                    total = sum(to_states[:-1])
                    if total:
                        transmission[s] = calc_transmissions(to_states, denominator, level, total, pseudocount)
                    else:
                        transmission[s] = {f"I{level - 1}": 1 / 3,
                                           f"M{level}": 1 / 3,
                                           f"D{level}": 1 / 3}
            else:  # first calculation
                to_states = from_to[START]
                transmission["S"] = calc_transmissions(to_states, denominator, level, len_patterns, pseudocount)

                to_states = from_to[INSERT]
                if sum(to_states[:-1]):
                    transmission["I0"] = calc_transmissions(to_states, denominator, level, len_patterns, pseudocount)
                else:
                    transmission["I0"] = {f"I{level - 1}": 1 / 3,
                                          f"M{level}": 1 / 3,
                                          f"D{level}": 1 / 3}

            level += 1  # on to the next level of the HMM
            # Reset inserts
            for from_state in from_to:
                from_state[INSERT] = 0

        ##############
        # Reset loop #
        ##############
        prev_states = curr_states.copy()
        for to_state in (DELETE, MATCH, MATCH_OR_INSERT):
            for from_state in from_to:
                from_state[to_state] = 0

    # end state reached
    _calc_end_emiss_transmiss(emission, transmission, from_to, curr_states, level - 1, pseudocount, alphabet)

    return transmission, emission


def calc_transmissions(to_states: Sequence[int], denominator: float, level: int, total: int, pseudocount: float
                       ) -> dict[str, float]:
    """
    Calculates the normalized transmission probabilities for the owner of `to_states`.

    :param to_states: A Sequence containing the occurrence count of DELETION, INSERT and MATCH in given order.
    :param denominator: The value by which to divide in order to do a normalization.
    :param level: The level at which `to_states` was taken.
    :param total: The amount of values that were counted for `to_states`.
    :param pseudocount: The value to normalize with.
    :return: A dict of the next possible states and their normalized probabilities.
    """
    return {
        f"I{level - 1}": normalize(to_states[INSERT], pseudocount, denominator, total),
        f"M{level}": normalize(to_states[MATCH], pseudocount, denominator, total),
        f"D{level}": normalize(to_states[DELETE], pseudocount, denominator, total),
    }


def calc_transmissions_end(state: int, curr_states: Sequence[int], p: float, level: int) -> dict[str, float]:
    """
    Calculates the normalized transmission probabilities for `state` of `level`.

    :param state: The state for which to calculate the transmission dict.
    :param curr_states: The last states encountered in the order of occurrence of their pattern.
    :param p: The probability to use when the state was in curr_states
    :param level: The last level in the HMM.
    :return: A dict of the next possible states and their normalized probabilities.
    """
    trans_dict: dict[str, float]
    if state not in curr_states:
        trans_dict = {f"I{level}": 0.5, "E": 0.5}
    else:
        trans_dict = {f"I{level}": p, "E": 1.0 - p}

    return trans_dict


def _calc_end_emiss_transmiss(emission: dict[str, dict[str, float]], transmission: dict[str, dict[str, float]],
                              from_to: Sequence[Sequence[int]], curr_states: Sequence[int], level: int,
                              pseudocount: float, alphabet: str) -> None:
    """
    Finishes the emission and transmission matrix for the transition to the end state.

    Has an execution time of O(3 + len(alphabet)).

    :param emission: The emission matrix.
    :param transmission: The transmission matrix.
    :param from_to: The matrix representing the last state transitions.
    :param curr_states: The last states encountered in the order of occurrence of their pattern.
    :param level: The last level in the HMM.
    :param pseudocount: The value to normalize with.
    :param alphabet: The alphabet of the patterns.
    :return: None
    """
    denominator: float = 1 + 2 * pseudocount

    p = normalize(from_to[INSERT][INSERT], pseudocount, denominator, (from_to[INSERT][INSERT] or 1) + 1)
    if INSERT not in curr_states:
        emission[f"I{level}"] = {alpha: 1 / len(alphabet) for alpha in alphabet}

        transmission[f"I{level}"] = {f"I{level}": 0.5, "E": 0.5}
        transmission[f"M{level}"] = calc_transmissions_end(MATCH, curr_states, p, level)
        transmission[f"D{level}"] = calc_transmissions_end(DELETE, curr_states, p, level)
    else:
        counter: Counter = emission[f"I{level}"]
        total: int = counter.total() - counter["-"]
        emission[f"I{level}"] = {
            alpha: normalize(counter[alpha], pseudocount, 1 + len(alphabet) * pseudocount, total)
            for alpha in alphabet}

        transmission[f"I{level}"] = {f"I{level}": p, "E": 1.0 - p}

        p = normalize(from_to[MATCH][INSERT], pseudocount, denominator, (from_to[MATCH][INSERT] or 1) + 1)
        transmission[f"M{level}"] = calc_transmissions_end(MATCH, curr_states, p, level)

        p = normalize(from_to[DELETE][INSERT], pseudocount, denominator, (from_to[DELETE][INSERT] or 1) + 1)
        transmission[f"M{level}"] = calc_transmissions_end(MATCH, curr_states, p, level)


def calc_emissions(counter: Counter, alphabet: str, pseudocount: float, ins_counter: Counter = None
                   ) -> tuple[dict[str, float], dict[str, float]]:
    """
    Calculates the normalized emission probabilities for the given `level` according to `counter`.

    Has an execution time of O(4 * len(alphabet)), but is probably closer to O(4 * len(alphabet))
    due to the usage of a Counter to get the total.

    :param counter: A dict containing a count of all matched values.
    :param alphabet: The alphabet of possible values.
    :param pseudocount: The value to normalize with.
    :param ins_counter: An optional dict containing a count of all inserted values.
    :return: A tuple of the emissions for a match state and of the emissions for an insert state.
    """
    total: int = counter.total() - counter["-"]
    denominator: float = 1 + len(alphabet) * pseudocount
    emission_match: dict[str, float] = {alpha: normalize(counter[alpha], pseudocount, denominator, total)
                                        for alpha in alphabet}

    emission_insert: dict[str, float]
    if ins_counter is None:
        emission_insert = {alpha: 1 / len(alphabet) for alpha in alphabet}
    else:
        total = ins_counter.total() - ins_counter["-"]
        emission_insert = {alpha: normalize(ins_counter[alpha], pseudocount, denominator, total)
                           for alpha in alphabet}

    return emission_match, emission_insert


def count_nodes(patterns: Sequence[Sequence[str]], from_to: list[list[int]], prev_states: list[int], i: int,
                len_patterns: int) -> tuple[Counter, list[int]]:
    """
    Counts the nodes for index `i` and updates `from_to` to reflect this count.

    Has an execution time of O(len_patterns). Worsened by slow access times to the sequences.

    :param patterns: A list of sequence-aligned patterns.
    :param from_to: The matrix to represent the state transitions (also contains counts of possible recurring inserts).
    :param prev_states: The previous states encountered in the order of occurrence of their pattern.
    :param len_patterns: The amount of patterns.
    :param i: The current index to count the nodes of.
    :return: A tuple of the Counter and the current states found while counting.
    """
    # passing patterns as a numpy ndarray was faster for this function
    # but this speedup was not enough to offset the cost of converting patterns
    # This function might be rewritten to benefit from parallelization.
    # At the moment the usage of prev_states and from_to prevents parallelization from being possible.

    counter: Counter = Counter()
    curr_states: list[int] = [0] * len_patterns

    for j in range(len_patterns):  # get j'th node of each pattern
        node: str = patterns[j][i]

        counter[node] += 1
        if node == "-":  # DELETE
            # count a DELETE for the previous state
            from_to[prev_states[j]][DELETE] += 1
            curr_states[j] = DELETE
        else:  # MATCH or INSERT
            # count a MATCH for the previous state
            from_to[prev_states[j]][MATCH_OR_INSERT] += 1
            curr_states[j] = MATCH

    return counter, curr_states


def normalize(value: int, pseudocount: float, denominator: float, total: int) -> float:
    """
    Calculates the normalized value.

    :return: (value / total + pseudocount) / denominator
    """
    return (value / total + pseudocount) / denominator


def get_state_str(state_nr: int, i: int) -> str:
    """Returns the string representation of a `state_nr` at a given index `i`"""
    s: str
    if state_nr == MATCH:
        s = f"M{i}"
    elif state_nr == DELETE:
        s = f"D{i}"
    elif state_nr == INSERT:
        s = f"I{i}"
    elif state_nr == START:
        s = "S"
    else:
        raise IndexError

    return s
