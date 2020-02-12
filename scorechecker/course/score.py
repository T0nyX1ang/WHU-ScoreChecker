"""
A module to calculate gpa and credit weight-based score.

Available functions are: calculate_gpa, calculate_score
"""


def calculate_single_gpa(score):
    """
    Calculate gpa with a score.

    Use a lookup table to calculate a single gpa.
    Empty scores or scores not between 0 and 100 will be regarded as 0.
    """
    lookup_table = [0.0] * 60 + [1.0] * 4 + [1.5] * 4 + [2.0] * 4 + \
        [2.3] * 3 + [2.7] * 3 + [3.0] * 4 + [3.3] * 3 + [3.7] * 5 + [4.0] * 11
    return 0.0 if score is None or score < 0 or score > 100 else lookup_table[
        int(score)]


def calculate_gpa(score_table):
    """
    Calculate gpa from a score table.

    Scores that have not come out will be regarded as 0.
    Please query/configure in advance.
    """
    if len(score_table) == 0:
        return 0.0  # when the score table is empty

    total_gpa, total_credit = [0] * 2
    for item in score_table:
        single_score = item[7]
        single_gpa = calculate_single_gpa(single_score)
        single_credit = item[2]
        total_gpa += (single_gpa * single_credit)
        total_credit += single_credit

    # calculate gpa and score
    return total_gpa / total_credit


def calculate_score(score_table):
    """
    Calculate weight-based score from a score table.

    Scores that have not come out will be regarded as 0.
    Please query/configure in advance.
    """
    if len(score_table) == 0:
        return 0.0  # when the score table is empty

    total_score, total_credit = [0] * 2
    for item in score_table:
        single_score = item[7]
        if single_score is None:
            single_score = 0.0
        single_credit = item[2]
        total_score += (single_score * single_credit)
        total_credit += single_credit

    # calculate gpa and score
    return total_score / total_credit
