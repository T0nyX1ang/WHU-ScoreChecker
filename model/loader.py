from keras.models import load_model

# model loader
# models must be put in the model folder.

def load(filename):
	try:
		print('Trying to load the model ...')
		model = load_model(filename)
		print('Model is loaded successfully ...')
		return model
	except Exception as e:
		print('Failed to load the model:', e)
		return None
