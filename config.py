import os
import json
import keyring
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from model import loader
from base import BaseApp
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Random import get_random_bytes

class ConfigApp(object):
	# GUI for the config app.
	# Need to be called before login and query.

	def __init__(self):
		# Initialization for the GUI. All of the variables are private here.
		self.__status = False
		self.__ID = ''
		self.__password = ''
		self.__captcha_model = None
		self.__query_model = None
		self.__config_filename = 'checker.cfg'

		if os.path.exists(self.__config_filename):
			print('Trying to load configurations from disk ...')
			self.__load_config()

		if self.get_status():
			return # return initially if config is loaded successfully

		self.__main_window = BaseApp("Configurations", 600, 200)
		self.__main_frame = tkinter.Frame(self.__main_window)
		self.__main_frame.pack(expand=True)

		self.__ID_label = tkinter.Label(self.__main_frame, text="ID")
		self.__ID_label.grid(row=0, column=0, padx=20, pady=10)
		self.__ID_entry = tkinter.Entry(self.__main_frame, width=30)
		self.__ID_entry.grid(row=0, column=1, padx=20, pady=10)
		
		self.__password_label = tkinter.Label(self.__main_frame, text="Password")
		self.__password_label.grid(row=1, column=0, padx=20, pady=10)
		self.__password_entry = tkinter.Entry(self.__main_frame, width=30, show='●')
		self.__password_entry.grid(row=1, column=1, padx=20, pady=10)

		self.__button_frame = tkinter.Frame(self.__main_frame)
		self.__button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
		self.__captcha_model_button = tkinter.Button(self.__button_frame, text='Load Captcha Model', command=self.__load_captcha_model)
		self.__captcha_model_button.pack(side='left', padx=10)
		self.__query_model_button = tkinter.Button(self.__button_frame, text='Load Query Model', command=self.__load_query_model)
		self.__query_model_button.pack(side='left', padx=10)
		self.__proceed_button = tkinter.Button(self.__button_frame, text='Proceed', command=self.__proceed)
		self.__proceed_button.pack(side='left', padx=10)

		self.__config_save_enable = tkinter.BooleanVar()
		self.__config_box = tkinter.Checkbutton(self.__main_frame, text='Save configurations', variable=self.__config_save_enable, command=self.__enable_save_warning)
		self.__config_box['selectcolor'] = self.__config_box['bg']
		self.__config_box.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

		self.__main_window.mainloop()

	def __load_model(self, model_category, filetypes, loader):
		# generic model loader, filetypes work as a filter, loader is a function
		model_category = model_category.lower()
		capitalized_model_category = model_category.capitalize()
		model_filename = tkinter.filedialog.askopenfilename(filetypes=filetypes, title='Load %s Model' % capitalized_model_category)
		model = loader(model_filename)
		if model is None:
			tkinter.messagebox.showerror('Load %s Model' % capitalized_model_category, 'Failed to load the %s model, please retry.' % model_category)
		else:
			tkinter.messagebox.showinfo('Load %s Model' % capitalized_model_category, 'The %s model is loaded successfully.' % model_category)
		return model_filename, model

	def __load_captcha_model(self):
		# Load a captcha model, should be HDF5 format.
		# The model is a (filename, Object) tuple
		self.__captcha_model = self.__load_model(model_category='captcha', filetypes=[('HDF5 format', '.hdf5')], loader=loader.load_captcha_model)

	def __load_query_model(self):
		# Load a query model, should be JSON format.
		# The model is a (filename, Object) tuple
		self.__query_model = self.__load_model(model_category='query', filetypes=[('JSON format', '.json')], loader=loader.load_query_model)

	def __proceed(self):
		# Process the variables passed in.
		status = True
		fail_hint = 'Failed to proceed:' + os.linesep
		self.__ID = self.__ID_entry.get()
		if len(self.__ID) == 0: 
			status = False
			fail_hint += 'Your ID should not be empty.' + os.linesep
			
		self.__password = MD5.new(self.__password_entry.get().encode()).digest().hex()
		if self.__password == 'd41d8cd98f00b204e9800998ecf8427e': # empty string hash
			status = False
			fail_hint += 'Your password should not be empty.' + os.linesep

		if self.__captcha_model[1] is None:
			status = False 
			fail_hint += 'You should load a captcha model to recognize the captcha.' + os.linesep

		if self.__query_model[1] is None:
			status = False
			fail_hint += 'You should load a query model to query your score table.' + os.linesep

		if status:
			print('Status checkes have been passed ...')
			self.__main_window.destroy()
		else:
			print('Some checkes have been failed ...')
			tkinter.messagebox.showerror("Proceed", fail_hint)

		self.__status = status
		self.__save_config()

	def __enable_save_warning(self):
		if self.__config_save_enable.get():
			ignore_warning = tkinter.messagebox.askyesno("Enable Saving Config Mode", "Saving your configurations will help with your ID, password and models automatically without opening a window every time you use. Although we make efforts to encrypt your credentials in AES and save a random password in the keyring, we can't guarantee your infomation stored securely. You can disable this mode by deleting the '%s' file on your disk. Will you still enable this mode?" % self.__config_filename)
			if not ignore_warning:
				print('Saving config mode enabled by user ...')
				self.__config_save_enable.set(False)

	def __load_config(self):
		json_config = self.__decrypt()
		if json_config:
			print('Extracting configurations from file ...')
			config = json.loads(json_config)
			self.__ID = config['ID']
			self.__password = config['password']
			self.__captcha_model = config['captcha_model_path'], loader.load_captcha_model(config['captcha_model_path'])
			self.__query_model = config['query_model_path'], loader.load_query_model(config['query_model_path'])
		else:
			print('Failed to load configurations from file, removing this file ...')
			os.remove(self.__config_filename)
			return

		if self.__ID is None or self.__password is None or self.__captcha_model[1] is None or self.__query_model[1] is None:
			print('Invalid configuration file, removing this file ...')
			os.remove(self.__config_filename)
		
		self.__status = True

	def __save_config(self):
		if self.__config_save_enable.get():
			config = {
				'ID': self.__ID,
				'password': self.__password,
				'captcha_model_path': self.__captcha_model[0],
				'query_model_path': self.__query_model[0],
			}
			json_config = json.dumps(config).encode()
			if self.__encrypt(json_config):
				print('Configurations have been saved to disk successfully.')

	def get_status(self):
		# Call this function before you call get_credentials.
		# A PermissionError will be thrown probably if you don't do the check here.
		return self.__status

	def get_credentials(self):
		# This should be the only data connection between this app and the caller.
		# For security, this function should be called after status flag have been set to True.
		# Once called, the status flag is set to False.
		# Please handle it with care.
		if self.get_status():
			self.__status = False # reset status flag
			return self.__ID, self.__password, self.__captcha_model[1], self.__query_model[1]
		else:
			raise PermissionError('Your access to this function violates the security policy here.')

	def __encrypt(self, data):
		try:
			key = get_random_bytes(32)
			cipher = AES.new(key, AES.MODE_EAX)
			nonce = cipher.nonce
			ciphertext, tag = cipher.encrypt_and_digest(data)
			keyring.set_password("ScoreChecker Crypto Module", "sccm_key", key.hex())
			keyring.set_password("ScoreChecker Crypto Module", "sccm_nonce", nonce.hex())
			keyring.set_password("ScoreChecker Crypto Module", "sccm_tag", tag.hex())
			with open(self.__config_filename, 'wb') as f:
				f.write(ciphertext)
			return True
		except Exception as e:
			print('Failed to encrypt the data:', e)
			raise e
			return False

	def __decrypt(self):
		try:
			with open(self.__config_filename, 'rb') as f:
				ciphertext = f.read()
			key = bytes.fromhex(keyring.get_password("ScoreChecker Crypto Module", "sccm_key"))
			nonce = bytes.fromhex(keyring.get_password("ScoreChecker Crypto Module", "sccm_nonce"))
			tag = bytes.fromhex(keyring.get_password("ScoreChecker Crypto Module", "sccm_tag"))
			cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
			plaintext = cipher.decrypt(ciphertext)
			cipher.verify(tag)
			if not self.__encrypt(plaintext):
				raise PermissionError("Failed to reset the key after decryption.")
			return plaintext
		except Exception as e:
			print('Failed to decrypt the data:', e)
			return None
