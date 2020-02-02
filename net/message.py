import requests
from .headers import Headers
from .cookies import Cookies

class Message(object):
	# a wrapper for requests, trying to make use of the headers and cookies
	def __init__(self):
		self.__headers, self.__cookies = Headers(), Cookies()

	def get(self, url, timeout=2):
		# HTTP GET request
		try:
			print('Making a HTTP GET request ...')
			self.__headers.update('Content-Type') # Remove Content-Type header when GET
			self.__headers.update('Origin')	# Remove Origin header when GET
			response = requests.get(url=url, timeout=timeout, headers=self.__headers.current(), cookies=self.__cookies.current())
			self.__cookies.update(response.cookies) # Update cookies
			# self.__headers.update('Referer', response.url) # Update referrer
			content = response.content
			print('HTTP GET response is received successfully ...')
			return content
		except Exception as e:
			print('Failed to GET the page:', e)
			return None

	def post(self, url, data, timeout=2):
		# HTTP POST request
		try:
			print('Making a HTTP POST request ...')
			self.__headers.update('Content-Type', 'application/x-www-form-urlencoded') # Add Content-Type header when POST
			self.__headers.update('Origin', self.__headers.current()['Host']) # Add Origin header when POST
			response = requests.post(url=url, data=data, timeout=timeout, headers=self.__headers.current(), cookies=self.__cookies.current())
			self.__cookies.update(response.cookies) # update cookies
			# self.__headers.update('Referer', response.url) # Update referrer
			content = response.content
			print('HTTP POST response is received successfully ...')
			return content
		except Exception as e:
			print('Failed to POST your data:', e)
			return None
