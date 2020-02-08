"""
Base app defines the title and geometry settings of an app.

This module should better be inherited by other apps.
"""

import tkinter


class BaseApp(tkinter.Tk):
    """
    Base app which create center tkinter layouts.

    This class inherits tkinter.Tk module.
    To reuse it, make it inherited by other apps.
    """

    def __init__(self, title, width, height):
        """
        Initialize with title, width and height.

        Invoke this function to deal with layout settings.
        """
        super(BaseApp, self).__init__()
        self.title(title)
        self.__geometry(width, height)

    def __geometry(self, width, height):
        # put window in the center of the screen
        offset_width = (self.winfo_screenwidth() - width) // 5 * 2
        offset_height = (self.winfo_screenheight() - height) // 5 * 2
        self.geometry("%sx%s+%s+%s" %
                      (width, height, offset_width, offset_height))
