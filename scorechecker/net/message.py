"""
Process continous HTTP requests.

The module works like a simple session with headers and cookies updated
automatically.
"""

import requests
from .headers import Headers
from .cookies import Cookies


class Message(object):
    """
    Basic message class.

    A wrapper for requests, trying to make use of the headers and cookies.
    """

    def __init__(self):
        """
        Initialization for initial headers and cookies.

        Based on the cookies and headers class.
        """
        self.__headers, self.__cookies = Headers(), Cookies()

    def get(self, url, timeout=2):
        """
        Make HTTP GET requests.

        'url' is the URL you want to make a request.
        'timeout' is set to 2.0 seconds on default.
        """
        print('Making a HTTP GET request ...')
        # Remove Content-Type and Origin header when GET
        self.__headers.update('Content-Type')
        self.__headers.update('Origin')
        response = requests.get(
            url=url,
            timeout=timeout,
            headers=self.__headers.current(),
            cookies=self.__cookies.current()
        )
        self.__cookies.update(response.cookies)  # Update cookies
        # self.__headers.update('Referer', response.url)
        content = response.content
        print('HTTP GET response is received successfully ...')
        return content

    def post(self, url, data, timeout=2):
        """
        Make HTTP POST requests.

        'url' is the URL you want to make a request.
        'timeout' is set to 2.0 seconds on default.
        """
        print('Making a HTTP POST request ...')
        # Add Content-Type and Origin header when GET
        self.__headers.update('Content-Type',
                              'application/x-www-form-urlencoded'
                              )
        self.__headers.update('Origin',
                              self.__headers.current()
                              ['Host'])
        response = requests.post(url=url,
                                 data=data,
                                 timeout=timeout,
                                 headers=self.__headers.current(),
                                 cookies=self.__cookies.current())
        self.__cookies.update(response.cookies)  # update cookies
        # self.__headers.update('Referer', response.url)
        content = response.content
        print('HTTP POST response is received successfully ...')
        return content
