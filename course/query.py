from .base_query import *

# main query model, construct your queries here.
# please make sure that the amount of classifications be appropriate. (2 - 5)

# default query model is a classifier to classify major_complusory and major_selective courses

def classifier(score_table, academy):
	# a classifier to deal with courses, available classifiers are:
	# major_complusory, major_selective, other_courses
	major_complusory = search_score_come_out(search_study_type(search_course_type(search_course_academy(score_table, academy), '专业必修'), '普通'))
	major_selective = search_score_come_out(search_study_type(search_course_type(search_course_academy(score_table, academy), '专业选修'), '普通'))
	other_courses = subtract(subtract(score_table, major_complusory), major_selective)
	return major_complusory, major_selective, other_courses

