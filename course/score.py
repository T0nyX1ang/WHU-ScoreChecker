# a module to calculate GPA and credit weight-based score

def convert_to_float(score):
	if len(score) == 0:
		return 0.0
	else:
		return float(score)

def calculate_single_GPA(score):
	# use a lookup table to calculate a single GPA
	lookup_table = [0.0] * 60 + [1.0] * 4 + [1.5] * 4 + [2.0] * 4 + [2.3] * 3 + [2.7] * 3 + [3.0] * 4 + [3.3] * 3 + [3.7] * 5 + [4.0] * 11
	return 0.0 if score is None or score < 0 or score > 100 else lookup_table[int(score)]	

def calculate_GPA(score_table):
	# calculate GPA from selected courses
	if len(score_table) == 0:
		return (0, 0) # when the score table is empty

	total_GPA, total_credit = [0] * 2
	for item in score_table:
		single_score = convert_to_float(item[7])
		single_GPA = calculate_single_GPA(single_score)
		single_credit = convert_to_float(item[2])
		total_GPA += (single_GPA * single_credit)
		total_credit += single_credit
	
	# calculate GPA and score
	return total_GPA / total_credit

def calculate_score(score_table):
	# calculate score from selected courses
	if len(score_table) == 0:
		return (0, 0) # when the score table is empty

	total_score, total_credit = [0] * 2
	for item in score_table:
		single_score = convert_to_float(item[7])
		single_credit = convert_to_float(item[2])
		total_score += (single_score * single_credit)
		total_credit += single_credit
	
	# calculate GPA and score
	return total_score / total_credit
