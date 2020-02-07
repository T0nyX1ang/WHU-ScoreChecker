import time

# base query library to search desired items.
# available queries: start_year, stop_year, 
#                    score_come_out, min_score, max_score, 
#                    min_credit, max_credit, 
#                    study_type, course_type,
#                    course_academy, course_name

def search_start_year(score_table, start_year):
    return {val for val in score_table if (val[5], val[6]) >= tuple(start_year)}

def search_stop_year(score_table, stop_year):
    return {val for val in score_table if (val[5], val[6]) <= tuple(stop_year)}

def search_score_come_out(score_table, come_out=True):
    return {val for val in score_table if not (bool(val[7]) ^ come_out)}

def search_min_score(score_table, min_score):
    score_come_out = search_score_come_out(score_table, come_out=True)
    return {val for val in score_table if val[7] >= min_score}

def search_max_score(score_table, max_score):
    score_come_out = search_score_come_out(score_table, come_out=True)
    return {val for val in score_table if val[7] <= max_score}

def search_min_credit(score_table, min_credit):
    return {val for val in score_table if val[2] >= min_credit}

def search_max_credit(score_table, max_credit):
    return {val for val in score_table if val[2] <= max_credit}

def search_study_type(score_table, study_type):
    return {val for val in score_table if val[4] in study_type}

def search_course_type(score_table, course_type):
    return {val for val in score_table if val[1] in course_type}

def search_course_academy(score_table, course_academy):
    return {val for val in score_table if val[3] in course_academy}

def search_course_name(score_table, course_name):
    return {val for val in score_table if val[0] in course_name}
