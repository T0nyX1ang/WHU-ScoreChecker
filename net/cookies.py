"""
Process cookies during HTTP requests.

The module works like a simple session, and set some initial cookies.
The CookieJar in requests.cookies is used in this module.
"""

import requests.cookies


class Cookies(object):
    """
    Basic cookies class.

    Contains initial cookies, cookies updating and current cookies fetching.
    """

    def __init__(self):
        """
        Initialization.

        For each single session, please call this once.
        """
        self.__cookies = requests.cookies.RequestsCookieJar()
        self.__cookies['userLanguage'] = 'zh-CN'

    def update(self, new_cookies):
        """
        Update the cookie jar with the response data.

        The new_cookies should be a requests HTTP request with cookies.
        """
        self.__cookies.update(new_cookies)

    def current(self):
        """
        Fetch current cookies.

        Invoke this function while constucting an HTTP request.
        """
        return self.__cookies
