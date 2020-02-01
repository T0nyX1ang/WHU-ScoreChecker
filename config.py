import os
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox

class ConfigApp(object):
	# main GUI for the score checker app

	def __init__(self):
		self._CONFIG_FILENAME = 'config.json'
		self._main_window = tkinter.Tk()
		self._main_window.title("Configurations")
		self._main_window.geometry("300x150+600+300")
		self._ID = tkinter.StringVar()
		self._password = tkinter.StringVar()
		self._model_dir = tkinter.StringVar()
		self.__on_load()
		self._ID_label = tkinter.Label(self._main_window, text="ID")
		self._ID_label.grid(row=0, column=0, padx=20, pady=10)
		self._ID_entry = tkinter.Entry(self._main_window, textvariable=self._ID)
		self._ID_entry.grid(row=0, column=1, padx=20, pady=10)
		self._password_label = tkinter.Label(self._main_window, text="Password")
		self._password_label.grid(row=1, column=0, padx=20, pady=10)
		self._password_entry = tkinter.Entry(self._main_window, textvariable=self._password)
		self._password_entry.grid(row=1, column=1, padx=20, pady=10)
		self._button_frame = tkinter.Frame(self._main_window)
		self._button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
		self._model_entry = tkinter.Button(self._button_frame, text='Load Model', command=self.__load_model)
		self._model_entry.pack(side='left', padx=10)
		self._save_button = tkinter.Button(self._button_frame, text='   Save   ', command=self.__save)
		self._save_button.pack(side='left', padx=10)
		self._exit_button = tkinter.Button(self._button_frame, text='   Exit   ', command=self.__exit)
		self._exit_button.pack(side='left', padx=10)

	def __on_load(self):
		if os.path.exists(self._CONFIG_FILENAME):
			with open(self._CONFIG_FILENAME, 'r') as f:
				json_file = f.read()
			try:
				config = json.loads(json_file)
				self._ID.set(config['ID'])
				self._password.set(config['Password'])
				self._model_dir.set(config['Model Directory'])
				print('Previous configuration file has been loaded successfully...')
			except Exception as e:
				self._ID.set("")
				self._password.set("")
				self._model_dir.set("")
				print('Configuration file has been corrupted, removing it...')
				os.remove(self._CONFIG_FILENAME)

	def __load_model(self):
		model_filename = tkinter.filedialog.askopenfilename(filetypes=[('HDF5 file', '.hdf5')], title='Load Model')
		from model import loader
		model = loader.load(model_filename)
		if model is not None:
			self._model_dir.set(model_filename)
		else:
			tkinter.messagebox.showerror("Load Model", "Failed to load the model, please retry.")

	def __save(self):
		config = {}
		config['ID'] = self._ID_entry.get()
		config['Password'] = self._password_entry.get()
		config['Model Directory'] = self._model_dir.get()
		with open(self._CONFIG_FILENAME, 'w') as f:
			f.write(json.dumps(config, indent=4))

	def __exit(self):
		self._main_window.quit()

	def run(self):
		self._main_window.mainloop()

if __name__ == '__main__':
	app = ConfigApp()
	app.run()