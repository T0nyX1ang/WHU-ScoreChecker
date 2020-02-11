"""
Configuration app.

This app provides a window to deal with settings, and a configuration
saving feature. The keys are saved in the keyring, and it's for one-time use.
The saved configurations are stored on disk and encrypted with AES.
"""

import os
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from loader import load_captcha_model, load_query_model
from base import BaseApp
from Crypto.Hash import MD5
from util import cryptography


class ConfigApp(BaseApp):
    """
    GUI for the config app.

    This class needs to be called before login and query.
    """

    def __init__(self):
        """
        Initialization for the GUI.

        All of the variables are private here.
        If saved configurations are loaded successfully,
        no window will be shown later.
        """
        self.__fail_hint = ''
        self.__default_config()
        print('Trying to load configurations ...')
        if not (self.__load_config() and self.get_status()):
            print('Failed to load configurations.')
            cryptography.reset()
            self.__set_layout()

    def __default_config(self):
        self.__config = {
            'ID': '',
            'password': 'd41d8cd98f00b204e9800998ecf8427e',
            'captcha_model': None,
            'query_model': None
        }

    def __set_layout(self):
        # set layouts
        super(ConfigApp, self).__init__("Configurations", 600, 200)
        self.__main_frame = tkinter.Frame(self)
        self.__main_frame.pack(expand=True)

        self.__ID_label = tkinter.Label(self.__main_frame, text="ID")
        self.__ID_label.grid(row=0, column=0, padx=20, pady=10)
        self.__ID_entry = tkinter.Entry(self.__main_frame, width=30)
        self.__ID_entry.grid(row=0, column=1, padx=20, pady=10)

        self.__password_label = tkinter.Label(self.__main_frame,
                                              text="Password")
        self.__password_label.grid(row=1, column=0, padx=20, pady=10)
        self.__password_entry = tkinter.Entry(self.__main_frame,
                                              width=30,
                                              show='●')
        self.__password_entry.grid(row=1, column=1, padx=20, pady=10)

        self.__button_frame = tkinter.Frame(self.__main_frame)
        self.__button_frame.grid(row=2, column=0, columnspan=2,
                                 padx=20, pady=10)
        self.__captcha_model_button = tkinter.Button(
            self.__button_frame, text='Load Captcha Model',
            command=self.__load_captcha_model)
        self.__captcha_model_button.pack(side='left', padx=10)
        self.__query_model_button = tkinter.Button(
            self.__button_frame, text='Load Query Model',
            command=self.__load_query_model)
        self.__query_model_button.pack(side='left', padx=10)
        self.__proceed_button = tkinter.Button(self.__button_frame,
                                               text='Proceed',
                                               command=self.__proceed)
        self.__proceed_button.pack(side='left', padx=10)

        self.__config_save_enable = tkinter.BooleanVar()
        self.__config_box = tkinter.Checkbutton(
            self.__main_frame, text='Save configurations',
            variable=self.__config_save_enable,
            command=self.__enable_save_warning)
        self.__config_box['selectcolor'] = self.__config_box['bg']
        self.__config_box.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        self.mainloop()

    def __load_captcha_model(self):
        # Load a captcha model, should be HDF5 format.
        # This function only returns a filepath and will not do loading jobs.
        self.__config['captcha_model'] = tkinter.filedialog.askopenfilename(
            filetypes=[('HDF5 format', '.hdf5')], title='Load Captcha Model')

    def __load_query_model(self):
        # Load a query model, should be JSON format.
        # This function only returns a filepath and will not do loading jobs.
        self.__config['query_model'] = tkinter.filedialog.askopenfilename(
            filetypes=[('JSON format', '.json')], title='Load Query Model')

    def __proceed(self):
        self.__config['ID'] = self.__ID_entry.get()
        self.__config['password'] = MD5.new(
            self.__password_entry.get().encode()).hexdigest()
        if self.get_status():
            self.destroy()
            self.__save_config()
        else:
            tkinter.messagebox.showerror("Status Check", self.__fail_hint)

    def __enable_save_warning(self):
        # A saving configuration feature warning window.
        if self.__config_save_enable.get():
            ignore_warning = tkinter.messagebox.askyesno(
                "Enable Saving Config Mode",
                "Saving your configurations will load your ID, password \
and models automatically without opening a window every time you use. \
Although we make efforts to encrypt your credentials in AES and save a \
random password in the keyring, we can't guarantee your infomation stored \
securely. Will you still enable this mode? The saved data can be removed.")
            if not ignore_warning:
                self.__config_save_enable.set(False)

    def __load_config(self):
        # Load configurations from disk.
        try:
            plaintext = cryptography.decrypt().decode()
            json_config = json.loads(plaintext)
            self.__config['ID'] = json_config['ID']
            self.__config['password'] = json_config['password']
            self.__config['captcha_model'] = json_config['captcha_model']
            self.__config['query_model'] = json_config['query_model']
            return True
        except:
            return False

    def __save_config(self):
        # Save configurations to disk.
        if self.__config_save_enable.get():
            json_config = json.dumps(self.__config).encode()
            try:
                cryptography.encrypt(json_config)
                print('Configurations have been saved successfully.')
            except Exception as e:
                print('Failed to encrypt the configurations:', e)

    def get_status(self):
        """
        Get data status.

        This function will be called before you call get_credentials.
        """
        fail = False
        fail_hint = 'You failed the status check:' + os.linesep
        if len(self.__config['ID']) == 0:
            fail = True
            fail_hint += 'Your ID should not be empty.' + os.linesep

        if self.__config['password'] == 'd41d8cd98f00b204e9800998ecf8427e':
            fail = True
            fail_hint += 'Your password should not be empty.' + os.linesep

        if load_captcha_model(self.__config['captcha_model']) is None:
            fail = True
            fail_hint += 'You should load a valid captcha model.' + os.linesep

        if load_query_model(self.__config['query_model']) is None:
            fail = True
            fail_hint += 'You should load a query model.' + os.linesep

        if fail:
            self.__fail_hint = fail_hint
            print('Some checkes have been failed ...')
            print(fail_hint.replace(os.linesep, '\n'))
            return False

        return True

    def get_credentials(self):
        """
        Get data/credentials from the app once.

        This should be the only data connection between this app
        and the caller.
        """
        if self.get_status():
            _id = self.__config['ID']
            password = self.__config['password']
            captcha_model = load_captcha_model(self.__config['captcha_model'])
            query_model = load_query_model(self.__config['query_model'])
            self.__default_config()
            return (_id, password, captcha_model, query_model)
        else:
            raise PermissionError(
                'Your access to this function violates the security policy.'
            )
