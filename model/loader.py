# model loader

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

def validate_query_model(model):
	return True

def load_query_model(filename):
	import json
	try:
		print('Trying to load the query model ...')
		with open(filename, 'r', encoding='utf-8') as f:
			fin = f.read()
			model = json.loads(fin)
		if validate_query_model(model):
			print('Model is loaded successfully ...')
			return model
		else:
			return None
	except Exception as e:
		print('Failed to load the model:', e)
		return None		