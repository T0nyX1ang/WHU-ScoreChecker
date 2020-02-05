import os, numpy
from .process import preprocess, resize, otsu
from .partition import partition

# predict the captcha

def predict_captcha(bytes_im, model):
	captcha = ''
	INV_TRANSFORM_STR = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
	if bytes_im is None:
		print('Please check your network.')

	if model is not None:
		array_im = numpy.asarray(bytearray(bytes_im), dtype='uint8')
		proc_im = preprocess(array_im)
		parts = partition(proc_im)
		for val in parts:
			crop = proc_im[val[1]:val[1] + val[3], val[0]:val[0] + val[2]]
			letter = resize(crop, width=20, height=20)
			letter = otsu(letter) # threshold again for more simple image
			letter = numpy.expand_dims(letter, axis=2) // 255
			letter = numpy.expand_dims(letter, axis=0)
			prediction = model.predict(letter) # predict the letter
			captcha += INV_TRANSFORM_STR[numpy.argmax(prediction)]
	
	return captcha
