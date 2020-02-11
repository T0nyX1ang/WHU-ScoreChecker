import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'app'))
from app.base import BaseApp
from app.config import ConfigApp
from app.result import ResultApp
from app.main import ScoreCheckerApp
from app.util.cryptography import *
from keras.engine.sequential import Sequential
import requests
import tkinter
import unittest
import json


config_message = {
    'ID': 'true_id',
    'password': 'true_password',
    'captcha_model': os.path.join(os.getcwd(), 'captcha_model.hdf5'),
    'query_model': os.path.join(os.path.join(os.getcwd(), 'static'), 'default.json')
}


test_html_dir = os.path.join(os.getcwd(), os.path.join('tests', 'test_html'))
with open(os.path.join(test_html_dir, 'test_a.html'), 'r', encoding='utf-8') as f:
    test_a = f.read()

with open(os.path.join(test_html_dir, 'test_b.html'), 'r', encoding='utf-8') as f:
    test_b = f.read()

with open(os.path.join(test_html_dir, 'test_c.html'), 'r', encoding='utf-8') as f:
    test_c = f.read()

with open(os.path.join(test_html_dir, 'test_d.html'), 'r', encoding='utf-8') as f:
    test_d = f.read()

test_image_dir = os.path.join(os.getcwd(), os.path.join('tests', 'test_captcha'))
with open(os.path.join(test_image_dir, '8Q68.jpg'), 'rb') as f:
    image = f.read()

class MockResponseA:
    content = test_a
    cookies = {'new': 'cookies!'}

class MockResponseB:
    content = test_b
    cookies = {}

class MockResponseC:
    content = test_c
    cookies = {}

class MockResponseD:
    content = test_d
    cookies = {}

class MockResponseI:
    content = image
    cookies = {'new': 'cookies?'}

def test_base_app(monkeypatch):
    monkeypatch.setattr(tkinter.Tk, 'mainloop', lambda x:0)
    base_app = BaseApp('hello_world', 400, 300)
    assert base_app.title() == 'hello_world'
    

def test_result_app(monkeypatch):
    monkeypatch.setattr(tkinter.Tk, 'mainloop', lambda x:0)
    result_app = ResultApp(set())
    result_app = ResultApp(
        {(('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None))})


def test_config_app(monkeypatch):
    reset()
    monkeypatch.setattr(tkinter.Tk, 'mainloop', lambda x:0)
    config_app = ConfigApp()
    assert config_app.get_status() == False
    reset()


def test_main_app(monkeypatch):
    reset()
    def mock_get(*args, **kwargs):
        if kwargs['url'] == 'http://bkjw.whu.edu.cn':
            return MockResponseA()
        elif kwargs['url'] == 'http://bkjw.whu.edu.cn/correct.html':
            return MockResponseI()
        elif kwargs['url'][:49] == 'http://bkjw.whu.edu.cn/servlet/Svlt_QueryStuScore':
            return MockResponseC()
        elif kwargs['url'] == 'http://bkjw.whu.edu.cn/servlet/logout':
            return MockResponseA()
    def mock_post(*args, **kwargs):
        if kwargs['url'] == 'http://bkjw.whu.edu.cn/here_is_the_login_page.html':
            return MockResponseB()
    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(tkinter.Tk, 'mainloop', lambda x:0)
    encrypt(json.dumps(config_message).encode())
    main_app = ScoreCheckerApp()
    reset()
    main_app = ScoreCheckerApp()


class TestAppWithoutWindow(unittest.TestCase):
    
    def test_config_app(self):
        reset()
        encrypt(json.dumps(config_message).encode())
        config_app = ConfigApp()
        self.assertTrue(config_app.get_status())
        _id, password, cmodel, qmodel = config_app.get_credentials()
        self.assertEqual(_id, 'true_id')
        self.assertEqual(password, 'true_password')
        self.assertIs(type(cmodel), Sequential)
        self.assertTrue(hasattr(cmodel, 'predict'))
        self.assertIs(type(qmodel), dict)
        for i in range(0, 5):
            self.assertRaises(PermissionError, config_app.get_credentials)
        reset()