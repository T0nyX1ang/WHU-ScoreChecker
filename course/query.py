import time

# query library to search desired items.
# available queries: year_range, score_come_out, score_range, credit, study_type, course_type

def search_year_range(score_table, start=None, stop=None):
	# search the year range between start and stop
	# start and stop are tuples: (year, semester), and their default values are based on your local time
	if start is None:
		start = (str(time.localtime().tm_year - 7), '1')
	if stop is None:
		stop = (str(time.localtime().tm_year), '3')

	result_table = []
	for table_row in score_table:
		if start <= (table_row[5], table_row[6]) <= stop:
			result_table.append(table_row)
	return result_table

def search_score_come_out(score_table, come_out=True):
	# search the scores that has come out
	result_table = []
	for table_row in score_table:
		if (come_out and len(table_row[7]) != 0) or (not come_out and len(table_row[7]) == 0):
			result_table.append(table_row)
	return result_table

def search_score_range(score_table, lowerbound=0.0, upperbound=100.0):
	# search the score range between lowerbound and upperbound
	score_table = search_score_come_out(score_table, come_out=True) # Only find score that comes out
	result_table = []
	for table_row in score_table:
		if lowerbound <= float(table_row[7]) <= upperbound:
			result_table.append(table_row)
	return result_table

def search_credit_range(score_table, lowerbound=0.0, upperbound=8.0):
	# search the credit range between lowerbound and upperbound
	result_table = []
	for table_row in score_table:
		if lowerbound <= float(table_row[2]) <= upperbound:
			result_table.append(table_row)
	return result_table

def search_study_type(score_table, study_type=None):
	# search study type
	if study_type is None:
		return score_table # no type will be regarded as wide types
	result_table = []
	for table_row in score_table:
		if table_row[4] == study_type:
			result_table.append(table_row)
	return result_table

def search_course_type(score_table, course_type=None):
	# search course type
	if course_type is None:
		return score_table # no type will be regarded as wide types
	result_table = []
	for table_row in score_table:
		if table_row[1] == course_type:
			result_table.append(table_row)
	return result_table

def search_course_academy(score_table, academy):
	# search academy (fuzzy)
	# may search for a long time
	if academy is None:
		return []
	result_table = []
	for table_row in score_table:
		correct = True
		for word in academy:
			if word not in table_row[3]:
				correct = False
				break
		if correct:
			result_table.append(table_row)
	return result_table

def search_course(score_table, course):
	# search course name (fuzzy)
	# may search for a long time
	if course is None:
		return []
	result_table = []
	for table_row in score_table:
		correct = True
		for word in course:
			if word not in table_row[0]:
				correct = False
				break
		if correct:
			result_table.append(table_row)
	return result_table
