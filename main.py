import os
import json
import time
import hashlib
from model import loader
from config import ConfigApp
from net import message, analyze
from predict import predict
from result import ResultApp

class ScoreCheckerApp(object):
	def __init__(self):
		# This is the main app to deal with everything.
		self.__url = 'http://bkjw.whu.edu.cn' # url
		self.__message_handler = message.Message() # global message control
		self._retries = 3 # global retry counter
		self.__control()

	def __control(self):
		# This part is the main control part, containing config, login and query.
		# This module is private.
		print('Initializing configuration app ...')
		config_app = ConfigApp()
		if config_app.get_status():
			ID, password, captcha_model, query_model = config_app.get_credentials()
		else:
			return

		while self._retries > 0:
			print('Logging in, remaining retries:', self._retries)
			academy, score_table = self.login(ID, password, captcha_model)
			if academy and score_table:
				print('Logging in successfully ...')
				break
			self._retries -= 1
		if self._retries == 0:
			print('Failed to log in, please check your connection.')
			return

		print('Querying ...')
		self.__query(academy, score_table, query_model)
		print('Querying successfully, see you next time.')
		
	def login(self, ID, password, captcha_model):
		# A separate login module, could be used publicly.
		try:
			base_content = self.__message_handler.get(url=self.__url)
			captcha_id = analyze.get_captcha_id(base_content)
			captcha_url = self.__url + captcha_id
			captcha_content = self.__message_handler.get(url=captcha_url)
			captcha = predict(captcha_content, captcha_model)
			login_id = analyze.get_login_id(base_content)
			login_url = self.__url + login_id
			login_data = {
				'timestamp': int(time.time() * 1000),
				'jwb': '%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F',
				'id': ID,
				'pwd': hashlib.md5(password.encode()).hexdigest(),
				'xdvfb': captcha,
			}
			login_content = self.__message_handler.post(url=login_url, data=login_data)
			academy = analyze.get_academy(login_content)
			csrf_token = analyze.get_csrf_token(login_content)
			score_table_url = self.__url + '/servlet/Svlt_QueryStuScore?csrftoken=' + csrf_token + '&year=0&term=&learnType=&scoreFlag=0&t=' + \
				str(time.ctime()).replace('  ', ' ') + ' GMT 0800 (中国标准时间)'
			score_table_content = self.__message_handler.get(url=score_table_url)
			score_table = analyze.get_score_table(score_table_content)
			return academy, score_table
		except Exception as e:
			print('Failed to log in:', e)
			print('Retrying ...')
			return None, None

	def query(self, academy, score_table, query_model):
		# A separate query module, could be used publicly.
		result_app = ResultApp(score_table)

if __name__ == '__main__':
	app = ScoreCheckerApp()
