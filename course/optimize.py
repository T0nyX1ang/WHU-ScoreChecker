"""
Main optimization model, construct your optimizers here.

Make sure the model is registered in the query part properly.
"""
import itertools
from .score import calculate_score


def classifier(major_complusory, major_selective, selection):
    """
    Default optimizer.

    'major_complusory': a major complusory course score table.
    'major_selective': a major selective course score table.
    'selection': selections from 'major_selective'
    """
    if selection > len(major_selective):
        selection = len(major_selective)

    max_score = 0
    select_result = []

    for sel in itertools.combinations(major_selective, selection):
        score_table = major_complusory + list(sel)
        score = calculate_score(score_table)
        if (score > max_score):
            max_score = score
            select_result = score_table

    return select_result
