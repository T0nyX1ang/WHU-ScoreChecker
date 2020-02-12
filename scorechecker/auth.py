"""
Authentication app.

Deal with user's login and logout actions.
"""

import time
from .image import predict
from .net import message, analyze


def auth_procedure(_id, password, captcha_model, retries=3):
    """
    A authentication module for user. Perform multiple authentications.

    Any exceptions will be caught.
    If a valid score table is returned, no exceptions will be caught.
    Otherwise, it will return None for nothing.
    'retries' show the number of retrying attempts.
    """
    score_table = None

    while retries >= 0:
        print('Authenticating, remaining retries:', retries)
        url = 'http://bkjw.whu.edu.cn'  # url
        msg_handler = message.Message()  # message control
        try:
            # fetch and predict captcha
            base_content = msg_handler.get(url=url)
            captcha_id = analyze.get_captcha_id(base_content)
            captcha_url = url + captcha_id
            captcha_content = msg_handler.get(url=captcha_url)
            captcha = predict.predict_captcha(captcha_content, captcha_model)

            # fetch login_id and log in
            login_id = analyze.get_login_id(base_content)
            login_url = url + login_id
            login_data = {
                'timestamp': int(time.time() * 1000),
                'jwb': '%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A\
%A1%E7%B3%BB%E7%BB%9F',
                'id': _id,
                'pwd': password,
                'xdvfb': captcha,
            }
            login_content = msg_handler.post(url=login_url, data=login_data)

            # fetch csrf token and score table
            csrf_token = analyze.get_csrf_token(login_content)
            score_table_url = url + '/servlet/Svlt_QueryStuScore?csrftoken=' \
                + csrf_token + '&year=0&term=&learnType=&scoreFlag=0&t=' \
                + str(time.ctime()).replace('  ', ' ') + ' GMT 0800 (中国标准时间)'
            score_table_content = msg_handler.get(url=score_table_url)
            score_table = analyze.get_score_table(score_table_content)

            # log out for next-time use
            logout_url = url + '/servlet/logout'
            msg_handler.get(url=logout_url)
            return score_table
        except Exception as e:
            print('Failed to authenticate:', e)
            print('Retrying ...')
            retries -= 1

    # this will happen if retries = 0
    print('Failed to authenticate, please check your connection.')
