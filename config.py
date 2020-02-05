import os
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from model import loader

class ConfigApp(object):
	# GUI for the config app.
	# Need to be called before login and query.

	def __init__(self):
		# Initialization for the GUI. All of the variables are private here.
		self.__main_window = tkinter.Tk()
		self.__main_window.title("Configurations")
		self.__main_window.geometry("400x150+600+300")
		self.__status = False

		self.__ID = ''
		self.__ID_label = tkinter.Label(self.__main_window, text="ID")
		self.__ID_label.grid(row=0, column=0, padx=20, pady=10)
		self.__ID_entry = tkinter.Entry(self.__main_window, width=30)
		self.__ID_entry.grid(row=0, column=1, padx=20, pady=10)

		self.__password = ''
		self.__password_label = tkinter.Label(self.__main_window, text="Password")
		self.__password_label.grid(row=1, column=0, padx=20, pady=10)
		self.__password_entry = tkinter.Entry(self.__main_window, width=30)
		self.__password_entry.grid(row=1, column=1, padx=20, pady=10)

		self.__button_frame = tkinter.Frame(self.__main_window)
		self.__button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
		self.__captcha_model = None
		self.__captcha_model_button = tkinter.Button(self.__button_frame, text='Load Captcha Model', command=self.__load_captcha_model)
		self.__captcha_model_button.pack(side='left', padx=10)
		self.__query_model = None
		self.__query_model_button = tkinter.Button(self.__button_frame, text='Load Query Model', command=self.__load_query_model)
		self.__query_model_button.pack(side='left', padx=10)
		self.__proceed_button = tkinter.Button(self.__button_frame, text='Proceed', command=self.__proceed)
		self.__proceed_button.pack(side='left', padx=10)

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
		return model

	def __load_captcha_model(self):
		# Load a captcha model, should be HDF5 format.
		self.__captcha_model = self.__load_model(model_category='captcha', filetypes=[('HDF5 format', '.hdf5')], loader=loader.load_captcha_model)

	def __load_query_model(self):
		# Load a query model, should be JSON format.
		self.__query_model = self.__load_model(model_category='query', filetypes=[('JSON format', '.json')], loader=loader.load_query_model)

	def __proceed(self):
		# Process the variables passed in.
		status = True
		fail_hint = 'Failed to proceed:' + os.linesep
		self.__ID = self.__ID_entry.get()
		if len(self.__ID) == 0: 
			status = False
			fail_hint += 'Your ID should not be empty.' + os.linesep
			
		self.__password = self.__password_entry.get()
		if len(self.__password) == 0:
			status = False
			fail_hint += 'Your password should not be empty.' + os.linesep

		if self.__captcha_model is None:
			status = False 
			fail_hint += 'You should load a captcha model to recognize the captcha.' + os.linesep

		if self.__query_model is None:
			status = False
			fail_hint += 'You should load a query model to query your score table.' + os.linesep

		if status:
			print('Status checkes have been passed ...')
			self.__main_window.destroy()
		else:
			print('Some checkes have been failed ...')
			tkinter.messagebox.showerror("Proceed", fail_hint)

		self.__status = status

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
			return self.__ID, self.__password, self.__captcha_model, self.__query_model
		else:
			raise PermissionError('Your access to this function violates the security policy here.')

if __name__ == '__main__':
	app = ConfigApp()
	if app.get_status():
		print(app.get_credentials())