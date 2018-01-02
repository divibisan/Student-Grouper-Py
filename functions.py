import itertools


def find_best_groups(permutations, matrix):
    """Loop through each possible set of groups and calculate its score,
    given the supplied cost matrix.

    :param permutations: A list containing a lists of possible sets of groups
    :param matrix: The cost matrix for pairs of students
    :returns: A list of all possible sets of groups with the lowest score
        out of all possible sets
    """
    best_groups = []
    min_score = 99999
    for set_of_groups in permutations:
        score = 0
        for group in set_of_groups:
            # Generate all pair-combinations of students in each group
            #  and add the cost of that pairing
            group_combinations = itertools.combinations(group, 2)
            for a, b in group_combinations:
                score += int(matrix[a][b])
        # Score now contains the total score for the entire set of groups
        # Only keep sets of groups whose score is <= to the lowest found score
        if score == min_score:
            best_groups.append(set_of_groups)
        elif score < min_score:
            # If new group has lower score:
            #  update min_score
            #  clear best groups, and then add new group
            min_score = score
            best_groups = [set_of_groups]
    return best_groups


def cast_into_chunks(data, chunk_sizes):
    """Loop through list, divide list into list of lists of given sizes.

    :param data: a list of lists or tuples to be divided into sub-groups
    :param chunk_sizes: a list, each element is the size of the sub-groups
    :returns: A list of possible sets of groups,
        each of which is a list (a set of groups) of lists (groups) of students
    """
    # Loop through list of permutations
    for row in data:
        # Convert from tuple to list
        permutation = list(row)
        list_of_groups = []
        # Loop through each listed group size
        for chunk_size in chunk_sizes:
            group = []
            # Pop "chunk_size" number of indices from the front
            #  of the permutation and add to list
            for i in range(chunk_size):
                group.append(permutation.pop(0))
            # Append that chunk to the list of groups
            list_of_groups.append(group)
        yield list_of_groups

