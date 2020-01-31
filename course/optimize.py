import itertools
from .score import calculate_score

# main optimization model, construct your optimizers here.
# default optimizer is classifier

def classifier(major_complusory, major_selective, selection):
	# this matches the classifier part in query part
	# major_complusory is all required courses
	# select a number of courses in major_selective courses

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