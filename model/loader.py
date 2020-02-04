# model validation and loader

def load_captcha_model(filename):
	from keras.models import load_model
	try:
		print('Trying to load the captcha model ...')
		model = load_model(filename)
		print('Model is loaded successfully ...')
		return model
	except Exception as e:
		print('Failed to load the model:', e)
		return None

def validate_single_key_value(key, value):
	# single key value checks.
	# including type_check and range_check, range check is a subset of type_check.

	type_check = lambda val, _type: True if type(val) in _type else False
	range_check = lambda val, lb, ub: True if lb <= val <= ub and type_check(val, [float, int, str]) else False
	
	allowed_query = {
		'start_year': lambda val: type_check(val, [list]),
		'stop_year': lambda val: type_check(val, [list]), 
		'score_come_out': lambda val: type_check(val, [bool]),
		'min_score': lambda val: range_check(val, 0.0, 100.0), 
		'max_score': lambda val: range_check(val, 0.0, 100.0), 
		'min_credit': lambda val: range_check(val, 0.0, 8.0), 
		'max_credit': lambda val: range_check(val, 0.0, 8.0),
		'study_type': lambda val: type_check(val, [list]), 
		'course_type': lambda val: type_check(val, [list]),
		'course_academy': lambda val: type_check(val, [list]), 
		'course_name': lambda val: type_check(val, [list]),
	}
	
	if key not in allowed_query:
		raise ValueError('Your key [%s] is not in the allowed list.' % key)
	elif not allowed_query[key](value):
		raise ValueError('Your key-value pair [%s: %s] does not pass the check' % (key, value))

def validate_query_model(model):
	for item in model['query'].keys():
		for each_key in model['query'][item].keys():
			validate_single_key_value(each_key, model['query'][item][each_key]) # type and range checks
		single_item = model['query'][item]

def validate_display_model(model):
	if model.get('display') and model['display'] not in model['query'].keys():
		raise ValueError('Your display score table name [%s] must append in the query keys.' % model['display'])

def load_query_model(filename):
	import json
	try:
		print('Trying to load the query model ...')
		with open(filename, 'r', encoding='utf-8') as f:
			fin = f.read()
			model = json.loads(fin)
		validate_query_model(model)
		validate_display_model(model)
		print('Model is loaded successfully ...')
		return model
	except Exception as e:
		print('Failed to load the model:', e)
		return None	
