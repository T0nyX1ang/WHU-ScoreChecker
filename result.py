import tkinter
import tkinter.ttk
from course import score

class ResultApp(object):
	def __init__(self, score_table):
		self._main_window = tkinter.Tk()
		self._main_window.title("Query Results")
		self._main_window.geometry("800x600+400+200")
		self._score_frame = tkinter.Frame(self._main_window)

		# Information
		self._GPA = score.calculate_GPA(score_table)
		self._avg_score = score.calculate_score(score_table)
		self._info_label = tkinter.Label(self._score_frame, text='GPA: ' + str(self._GPA) + '     Average score: ' + str(self._avg_score))
		self._info_label.pack(side='top', pady=20)

		# score table
		self._columns = ('课程名称', '课程类型', '学分', '授课学院', '学习类型', '学年', '学期', '成绩')
		self._columns_width = (200, 80, 40, 120, 80, 40, 40, 60)				
		self._score_frame.pack(expand=True)
		self._score_view_scrollbar = tkinter.Scrollbar(self._score_frame)
		self._score_view = tkinter.ttk.Treeview(self._score_frame, show='headings', columns=self._columns, height=20, yscrollcommand=self._score_view_scrollbar.set)
		self._score_view_scrollbar.pack(side='right', fill='y')
		self._score_view_scrollbar.config(command=self._score_view.yview)
		for i in range(0, len(self._columns)):
			self._score_view.column(self._columns[i], anchor='center', width=self._columns_width[i])
			self._score_view.heading(self._columns[i], text=self._columns[i])
		for val in score_table:
			self._score_view.insert('', 'end', values=tuple(val))
		self._score_view.pack()
		self._main_window.mainloop()
