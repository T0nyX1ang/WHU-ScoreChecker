import tkinter

class BaseApp(tkinter.Tk):
    # This is the base app which create center tkinter layouts
    # To reuse it, make it inherited by other app files
    def __init__(self, title, width, height):
        super(BaseApp, self).__init__()
        self.title(title)
        self.__geometry(width, height)

    def __geometry(self, width, height):
        # put window in the center of the screen
        offset_width = (self.winfo_screenwidth() - width) // 5 * 2
        offset_height = (self.winfo_screenheight() - height) // 5 * 2
        self.geometry("%sx%s+%s+%s" % (width, height, offset_width, offset_height))
        
if __name__ == '__main__':
    app = BaseApp('hello', 400, 300)
    app.mainloop()
