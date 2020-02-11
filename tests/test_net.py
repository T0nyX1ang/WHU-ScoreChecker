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


class TestAnalyze(unittest.TestCase):

    def test_captcha_id(self):
        self.assertEqual(get_captcha_id(test_a), '/correct.html')
        self.assertRaises(AttributeError, get_captcha_id, test_d)
        self.assertRaises(ValueError, get_captcha_id, test_e)

    def test_login_id(self):
        self.assertEqual(get_login_id(test_a), '/here_is_the_login_page.html')
        self.assertRaises(AttributeError, get_login_id, test_d)

    def test_csrf_token(self):
        self.assertEqual(get_csrf_token(test_b), '01234567-89ab-cdef-fedc-ba9876543210')
        self.assertRaises(ValueError, get_csrf_token, test_d)

    def test_score_table(self):
        self.assertEqual(get_score_table(test_c), {
            ('AAAAAA', '专业选修', 3.0, 'CCCCCC', '普通', 2019, 1, None),
            ('aaaaaa', '专业必修', 6.0, 'cccccc', '普通', 2018, 2, 92.0)
        })
        self.assertEqual(get_score_table(test_d), set())
        self.assertRaises(ValueError, get_score_table, test_e)