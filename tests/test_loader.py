import os
import sys
import unittest
from scorechecker.loader import *
from keras.engine.sequential import Sequential

test_query_model_dir = os.path.join(os.getcwd(), os.path.join('tests', 'test_query'))
default_query_model_dir = os.path.join(os.getcwd(), 'static')


class TestCaptchaModelLoader(unittest.TestCase):

    def test_captcha_model_loader(self):
        self.assertIsNone(load_captcha_model(None), None)
        self.assertIsNone(load_captcha_model('invalid_model_name.hdf5'), None)
        self.assertIsNone(load_captcha_model(1), None)
        self.assertIs(type(load_captcha_model('captcha_model.hdf5')), Sequential)
        self.assertTrue(hasattr(load_captcha_model('captcha_model.hdf5'), 'predict'))


class TestQueryModelValidationAndLoader(unittest.TestCase):

    def test_single_key_value_checker(self):
        self.assertIsNone(validate_single_key_value('start_year', [2016, 4]))
        self.assertRaises(ValueError, validate_single_key_value, 'start_year', 123)
        
        self.assertIsNone(validate_single_key_value('stop_year', [2019, 0]))
        self.assertRaises(ValueError, validate_single_key_value, 'stop_year', 123)
        
        self.assertIsNone(validate_single_key_value('score_come_out', True))
        self.assertIsNone(validate_single_key_value('score_come_out', False))
        self.assertRaises(ValueError, validate_single_key_value, 'score_come_out', 123)

        self.assertIsNone(validate_single_key_value('min_score', 0.0))
        self.assertRaises(ValueError, validate_single_key_value, 'min_score', -1.0)
        self.assertRaises(ValueError, validate_single_key_value, 'min_score', 101.0)
        self.assertRaises(ValueError, validate_single_key_value, 'min_score', '1.0')

        self.assertIsNone(validate_single_key_value('max_score', 100.0))
        self.assertRaises(ValueError, validate_single_key_value, 'max_score', -1.0)
        self.assertRaises(ValueError, validate_single_key_value, 'max_score', 101.0)
        self.assertRaises(ValueError, validate_single_key_value, 'max_score', '1.0')

        self.assertIsNone(validate_single_key_value('min_credit', 0.0))
        self.assertRaises(ValueError, validate_single_key_value, 'min_credit', -1.0)
        self.assertRaises(ValueError, validate_single_key_value, 'min_credit', 9.0)
        self.assertRaises(ValueError, validate_single_key_value, 'min_credit', '1.0')       

        self.assertIsNone(validate_single_key_value('max_credit', 8.0))
        self.assertRaises(ValueError, validate_single_key_value, 'max_credit', -1.0)
        self.assertRaises(ValueError, validate_single_key_value, 'max_credit', 9.0)
        self.assertRaises(ValueError, validate_single_key_value, 'max_credit', '1.0')   

        self.assertIsNone(validate_single_key_value('study_type', ['a', 'b', 'c']))
        self.assertRaises(ValueError, validate_single_key_value, 'study_type', 'a')

        self.assertIsNone(validate_single_key_value('course_type', ['d', 'e', 'f']))
        self.assertRaises(ValueError, validate_single_key_value, 'course_type', 'a')
        
        self.assertIsNone(validate_single_key_value('course_academy', ['g', 'h', 'i']))
        self.assertRaises(ValueError, validate_single_key_value, 'course_academy', 'a')

        self.assertIsNone(validate_single_key_value('course_name', ['j', 'k', 'l']))
        self.assertRaises(ValueError, validate_single_key_value, 'course_name', 'a')

        self.assertRaises(KeyError, validate_single_key_value, 'invalid_key', 'any_value')

    def test_query_model_loader(self):
        for filename in os.listdir(test_query_model_dir):
            _filename, filetype = os.path.splitext(filename)
            if filetype.lower() == '.json':
                status = _filename.split('_')[0].lower()
                if status == 'fail':
                    self.assertIsNone(load_query_model(os.path.join(test_query_model_dir, filename)))
                elif status == 'success':
                    self.assertIs(type(load_query_model(os.path.join(test_query_model_dir, filename))), dict)

    def test_default_query_models(self):
        # This test makes sure all query models uploaded to Github is correct.
        for filename in os.listdir(default_query_model_dir):
            filetype = os.path.splitext(filename)[1]
            if filetype.lower() == '.json':
                self.assertIs(type(load_query_model(os.path.join(default_query_model_dir, filename))), dict)