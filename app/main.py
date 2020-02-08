"""
Main app.

This is the CORE part of this project and should be the only file to be
executed when you are just a user. This file connects all the files needed.
"""

import time
from config import ConfigApp
from course import extract
from image import predict
from net import message, analyze
from result import ResultApp


class ScoreCheckerApp(object):
    """
    Main app (ScoreChecker App).

    This is the main part to deal with everything.
    """

    def __init__(self):
        """
        Initialization for the app.

        Just invoke this function to use it.
        """
        self._retries = 3  # global retry counter
        self.__control()

    def __control(self):
        # This part is the main control part, containing configuration,
        # login and query.
        print('Initializing configuration app ...')
        capp = ConfigApp()
        if capp.get_status():
            print('Fetching infomation for configuration app ...')
            _id, password, captcha_model, query_model = capp.get_credentials()
        else:
            return

        score_table = None
        while self._retries >= 0 and not score_table:
            print('Logging in, remaining retries:', self._retries)
            score_table = self.__login(_id, password, captcha_model)
            self._retries -= 1

        if self._retries < 0:
            print('Failed to log in, please check your connection.')
            return

        print('Logging in successfully, querying ...')
        self.__query(score_table, query_model)
        print('Querying successfully, see you next time.')

    def __login(self, _id, password, captcha_model):
        # A login module.
        url = 'http://bkjw.whu.edu.cn'  # url
        msg_handler = message.Message()  # message control
        try:
            base_content = msg_handler.get(url=url)
            captcha_id = analyze.get_captcha_id(base_content)
            captcha_url = url + captcha_id
            captcha_content = msg_handler.get(url=captcha_url)
            captcha = predict.predict_captcha(captcha_content, captcha_model)
            login_id = analyze.get_login_id(base_content)
            login_url = url + login_id
            login_data = {
                'timestamp': int(time.time() * 1000),
                'jwb': '%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A%A1\
%E7%B3%BB%E7%BB%9F',
                'id': _id,
                'pwd': password,
                'xdvfb': captcha,
            }
            login_content = msg_handler.post(url=login_url, data=login_data)
            csrf_token = analyze.get_csrf_token(login_content)
            score_table_url = url + '/servlet/Svlt_QueryStuScore?csrftoken=' \
                + csrf_token + '&year=0&term=&learnType=&scoreFlag=0&t=' \
                + str(time.ctime()).replace('  ', ' ') + ' GMT 0800 (中国标准时间)'
            score_table_content = msg_handler.get(url=score_table_url)
            raw_score_table = analyze.get_raw_score_table(score_table_content)
            score_table = analyze.get_score_table(raw_score_table)
            return score_table
        except Exception as e:
            print('Failed to log in:', e)
            print('Retrying ...')
            return None

    def __query(self, score_table, query_model):
        # A query module.
        result_score_table = extract.extract(score_table, query_model)
        ResultApp(result_score_table)


if __name__ == '__main__':
    app = ScoreCheckerApp()
