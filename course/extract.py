from .query import *
from .optimize import *
from ast import literal_eval

def convert(key):
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
	# main module, the results will be sent to the result app.
	# for convenience, we use literal_eval to transform a str to a function.
	# please note: if you want to use the model separately, you must validate the model for security issues.

	if not query_model.get('display'):
		return score_table

	middle_extract = {} # store for later use
	for item in query_model['query'].keys():
		temp_score_table = score_table	
		for each_key in query_model['query'][item].keys():
			temp_score_table = convert(each_key)(temp_score_table, query_model['query'][item][each_key])
		middle_extract[item] = temp_score_table

	return middle_extract[query_model['display']]
