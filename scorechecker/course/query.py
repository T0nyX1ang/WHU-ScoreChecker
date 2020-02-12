"""
Basic query library to search desired items.

The interfaces are uniformed as: function(score_table, condition)
Available queries: start_year, stop_year,
                   score_come_out, min_score, max_score,
                   min_credit, max_credit,
                   study_type, course_type,
                   course_academy, course_name
"""


def search_start_year(score_table, start_year):
    """
    Search courses from 'start_year'.

    'start_year' is a list: [year, semester] and will be converted to a tuple.
    """
    return {v for v in score_table if (v[5], v[6]) >= tuple(start_year)}


def search_stop_year(score_table, stop_year):
    """
    Search courses to 'stop_year'.

    'stop_year' is a list: [year, semester] and will be converted to a tuple.
    """
    return {v for v in score_table if (v[5], v[6]) <= tuple(stop_year)}


def search_score_come_out(score_table, come_out=True):
    """
    Search courses that scores have come out or not.

    'come_out' is a bool, set it to True to search scores that have come out,
    and set it to False to search that have not.
    """
    return {v for v in score_table if not (bool(v[7]) ^ come_out)}


def search_min_score(score_table, min_score):
    """
    Search scores greater than 'min_score'.

    'min_score' is a float that between 0 and 100.
    'min_score' should be better smaller than 'max_score'.
    """
    score_come_out = search_score_come_out(score_table, come_out=True)
    return {v for v in score_come_out if v[7] >= min_score}


def search_max_score(score_table, max_score):
    """
    Search scores smaller than 'max_score'.

    'max_score' is a float that between 0 and 100.
    'min_score' should be better smaller than 'max_score'.
    """
    score_come_out = search_score_come_out(score_table, come_out=True)
    return {v for v in score_come_out if v[7] <= max_score}


def search_min_credit(score_table, min_credit):
    """
    Search credits greater than 'min_credit'.

    'min_credit' is a float that between 0.0 and 8.0.
    'min_credit' should be better smaller that 'max_credit'.
    """
    return {v for v in score_table if v[2] >= min_credit}


def search_max_credit(score_table, max_credit):
    """
    Search credits smaller than 'max_credit'.

    'max_credit' is a float that between 0.0 and 8.0.
    'min_credit' should be better smaller that 'max_credit'.
    """
    return {v for v in score_table if v[2] <= max_credit}


def search_study_type(score_table, study_type):
    """
    Search study types of courses.

    'study_type' is a list, and we will match as much types as possible.
    """
    return {v for v in score_table if v[4] in study_type}


def search_course_type(score_table, course_type):
    """
    Search course types of courses.

    'course_type' is a list, and we will match as much types as possible.
    """
    return {v for v in score_table if v[1] in course_type}


def search_course_academy(score_table, course_academy):
    """
    Search academies of courses.

    'course_academy' is a list, and we will match as much acadmies as possible.
    """
    return {v for v in score_table if v[3] in course_academy}


def search_course_name(score_table, course_name):
    """
    Search names of courses.

    'course_name' is a list, and we will match as much namessss as possible.
    """
    return {v for v in score_table if v[0] in course_name}
