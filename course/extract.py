"""
Extract information from a score table.

Available functions: convert, extract
"""

from .query import search_start_year, search_stop_year, \
    search_score_come_out, search_min_score, search_max_score, \
    search_min_credit, search_max_credit, \
    search_study_type, search_course_type, \
    search_course_academy, search_course_name


def convert(key):
    """
    Convert keys to their functions.

    Available keys are: start_year, stop_year,
    score_come_out, min_score, max_score, min_credit, max_credit
    study_type, course_type, course_academy, course_name
    """
    lookup_table = {
        'start_year': lambda s, v: search_start_year(s, v),
        'stop_year': lambda s, v: search_stop_year(s, v),
        'score_come_out': lambda s, v: search_score_come_out(s, v),
        'min_score': lambda s, v: search_min_score(s, v),
        'max_score': lambda s, v: search_max_score(s, v),
        'min_credit': lambda s, v: search_min_credit(s, v),
        'max_credit': lambda s, v: search_max_credit(s, v),
        'study_type': lambda s, v: search_study_type(s, v),
        'course_type': lambda s, v: search_course_type(s, v),
        'course_academy': lambda s, v: search_course_academy(s, v),
        'course_name': lambda s, v: search_course_name(s, v),
    }
    return lookup_table[key]


def extract(score_table, query_model):
    """
    Extract required information from a score table based on the query model.

    This is the main module, the results will be sent to the result app.
    If you want to use the model separately, you must validate the model.
    """
    if not query_model.get('display'):
        return score_table

    middle_extract = {}  # store for later use
    for item in query_model['query'].keys():
        temp_score_table = score_table
        for each_key in query_model['query'][item].keys():
            temp_score_table = convert(each_key)(
                temp_score_table, query_model['query'][item][each_key])
        middle_extract[item] = temp_score_table

    return middle_extract[query_model['display']]
