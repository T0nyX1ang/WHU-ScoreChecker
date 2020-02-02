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

	def __load_captcha_model(self):
		# Load a captcha model, should be HDF5 format.
		model_filename = tkinter.filedialog.askopenfilename(filetypes=[('HDF5 format', '.hdf5')], title='Load Captcha Model')
		self.__captcha_model = loader.load_captcha_model(model_filename)
		if self.__captcha_model is None:
			tkinter.messagebox.showerror("Load Captcha Model", "Failed to load the captcha model, please retry.")
		else:
			tkinter.messagebox.showinfo("Load Captcha Model", "The captcha model is loaded successfully.")

	def __load_query_model(self):
		# Load a query model, should be JSON format.
		model_filename = tkinter.filedialog.askopenfilename(filetypes=[('JSON format', '.json')], title='Load Query Model')
		self.__query_model = loader.load_query_model(model_filename)
		if self.__query_model is None:
			tkinter.messagebox.showerror("Load Query Model", "Failed to load the query model, please retry.")
		else:
			tkinter.messagebox.showinfo("Load Query Model", "The query model is loaded successfully.")

	def __proceed(self):
		# Process the variables passed in.
		status = True
		fail_hint = 'Failed to proceed:' + os.linesep
		if len(self.__ID_entry.get()) == 0: 
			status = False
			fail_hint += 'Your ID should not be empty.' + os.linesep
		else:
			self.__ID = self.__ID_entry.get()

		if len(self.__password_entry.get()) == 0:
			status = False
			fail_hint += 'Your password should not be empty.' + os.linesep
		else:
			self.__password = self.__password_entry.get()

		if self.__captcha_model is None:
			status = False 
			fail_hint += 'You should load a captcha model to recognize the captcha.' + os.linesep

		if self.__query_model is None:
			status = False
			fail_hint += 'You should load a query model to query your score table.' + os.linesep

		if status:
			print('Status checkes have been passed ...')
			self.__main_window.quit()
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