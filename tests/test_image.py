import os
import unittest
from keras.models import load_model
from app.image.predict import predict_captcha

model = load_model('captcha_model.hdf5')
test_image_dir = os.path.join(os.getcwd(), os.path.join('tests', 'test_captcha'))

class TestImageRecognizer(unittest.TestCase):

    def test_predict(self):
        self.assertEqual(predict_captcha(None, None), '')
        self.assertEqual(predict_captcha(None, 'random_model'), '')
        self.assertEqual(predict_captcha('random_image', None), '')

        for filename in os.listdir(test_image_dir):
            captcha = os.path.splitext(filename)[0]
            with open(os.path.join(test_image_dir, filename), 'rb') as f:
                image = f.read()
            self.assertEqual(predict_captcha(image, model), captcha)
