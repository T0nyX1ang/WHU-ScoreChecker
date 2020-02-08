"""
Process headers during HTTP requests.

The module works like a simple session, and set some initial headers.
You can add/delete header items into/from the initial headers.
"""


class Headers(object):
    """
    Basic headers class.

    Contains initial headers, headers updating and current headers fetching.
    """

    def __init__(self):
        """
        Initialize with basic headers.

        The initial headers use a Windows x64 + Chrome 79.0.3945.117 UA.
        Other settings are common.
        """
        self.__headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Host": "bkjw.whu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://bkjw.whu.edu.cn"
        }

    def update(self, key, value=None):
        """
        Update a header item with a key-value pair.

        If the value is set to None, the item with the key will be DELETED.
        Instead, the item will be UPDATED with the key.
        """
        if key not in self.__headers:
            return
        elif value is not None:
            self.__headers[key] = value
        else:
            self.__headers.pop(key)

    def current(self):
        """
        Fetch current headers.

        Invoke this function while constucting an HTTP request.
        """
        return self.__headers
