import os
import unittest
from app.net.analyze import *
from app.net.headers import Headers
from app.net.message import Message

test_html_dir = os.path.join(os.getcwd(), os.path.join('tests', 'test_html'))
with open(os.path.join(test_html_dir, 'test_a.html'), 'r', encoding='utf-8') as f:
    test_a = f.read()

with open(os.path.join(test_html_dir, 'test_b.html'), 'r', encoding='utf-8') as f:
    test_b = f.read()

with open(os.path.join(test_html_dir, 'test_c.html'), 'r', encoding='utf-8') as f:
    test_c = f.read()

with open(os.path.join(test_html_dir, 'test_d.html'), 'r', encoding='utf-8') as f:
    test_d = f.read()

with open(os.path.join(test_html_dir, 'test_e.html'), 'r', encoding='utf-8') as f:
    test_e = f.read()

class TestHeaders(unittest.TestCase):

    def test_headers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Host": "bkjw.whu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://bkjw.whu.edu.cn"
        }       
        h = Headers()
        self.assertEqual(h.current(), headers)
        h.update("Connection", "closed")
        headers["Connection"] = "closed"
        self.assertEqual(h.current(), headers)
        h.update("DNT")
        headers.pop("DNT")
        self.assertEqual(h.current(), headers)
        h.update("invalid_key", "invalid_value")
        self.assertEqual(h.current(), headers)
        h.update("invalid_key")
        self.assertEqual(h.current(), headers)


class TestMessage(unittest.TestCase):

    def test_message(self):
        m = Message()
        self.assertIsNone(m.get(url='invalid_url'))
        self.assertIsNone(m.post(url='invalid_url', data={'key': 'value'}))
        self.assertIsNotNone(m.get(url='http://httpbin.org', timeout=100))
        self.assertIsNotNone(m.post(url='http://httpbin.org/post', data={'key': 'value'}, timeout=100))


class TestAnalyze(unittest.TestCase):

    def test_captcha_id(self):
        self.assertEqual(get_captcha_id(test_a), '/correct.html')
        self.assertIsNone(get_captcha_id(test_d))
        self.assertIsNone(get_captcha_id(test_e))
        self.assertIsNone(get_captcha_id(None))

    def test_login_id(self):
        self.assertEqual(get_login_id(test_a), '/here_is_the_login_page.html')
        self.assertIsNone(get_login_id(test_d))
        self.assertIsNone(get_login_id(None))

    def test_csrf_token(self):
        self.assertEqual(get_csrf_token(test_b), '01234567-89ab-cdef-fedc-ba9876543210')
        self.assertIsNone(get_csrf_token(test_d))
        self.assertIsNone(get_csrf_token(None))

    def test_score_table(self):
        self.assertIsNone(get_score_table(None))
        self.assertIsNone(get_score_table(test_e))
        self.assertEqual(get_score_table(test_d), set())
        self.assertEqual(get_score_table(test_c), {
            ('AAAAAA', '专业选修', 3.0, 'CCCCCC', '普通', 2019, 1, None),
            ('aaaaaa', '专业必修', 6.0, 'cccccc', '普通', 2018, 2, 92.0)
        })