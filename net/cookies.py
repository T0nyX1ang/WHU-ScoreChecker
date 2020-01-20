import requests.cookies

class Cookies(object):
	# Basic cookies part.
	def __init__(self):
		self.__cookies = requests.cookies.RequestsCookieJar()
		
	def update(self, new_cookies):
		# update the cookie jar with the response data
		self.__cookies.update(new_cookies)

	def current(self):
		# return current cookies
		return self.__cookies