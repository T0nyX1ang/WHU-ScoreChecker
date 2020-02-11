import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'app'))

import pytest
import requests
from app.auth import auth_procedure
from app.net.message import Message
from keras.models import load_model

model = load_model('captcha_model.hdf5')

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

def test_success_auth(monkeypatch):
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

    result = auth_procedure(_id='true_id', password='true_password', captcha_model=model)
    assert result == {
        ('AAAAAA', '专业选修', 3.0, 'CCCCCC', '普通', 2019, 1, None),
        ('aaaaaa', '专业必修', 6.0, 'cccccc', '普通', 2018, 2, 92.0)
    }

def test_fake_auth(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseD()

    monkeypatch.setattr(requests, "get", mock_get)

    result = auth_procedure(_id='fake_id', password='fake_password', captcha_model=model)
    assert result is None
