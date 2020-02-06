import tkinter
import tkinter.ttk
from base import BaseApp
from course import score

class ResultApp(object):
	def __init__(self, score_table):
		# This app should be utilized to show score results
		self.__main_window = BaseApp("Query Results", 800, 600)
		self.__score_frame = tkinter.Frame(self.__main_window)

		# Information
		self.__GPA = score.calculate_GPA(score_table)
		self.__avg_score = score.calculate_score(score_table)
		self.__info_label = tkinter.Label(self.__score_frame, text='GPA: ' + str(self.__GPA) + '     Average score: ' + str(self.__avg_score))
		self.__info_label.pack(side='top', pady=20)

		# score table
		self.__columns = ('课程名称', '课程类型', '学分', '授课学院', '学习类型', '学年', '学期', '成绩')
		self.__columns_width = (200, 80, 40, 120, 80, 40, 40, 60)				
		self.__score_frame.pack(expand=True)
		self.__score_view_scrollbar = tkinter.Scrollbar(self.__score_frame)
		self.__score_view = tkinter.ttk.Treeview(self.__score_frame, show='headings', columns=self.__columns, height=20, yscrollcommand=self.__score_view_scrollbar.set)
		self.__score_view_scrollbar.pack(side='right', fill='y')
		self.__score_view_scrollbar.config(command=self.__score_view.yview)
		for i in range(0, len(self.__columns)):
			self.__score_view.column(self.__columns[i], anchor='center', width=self.__columns_width[i])
			self.__score_view.heading(self.__columns[i], text=self.__columns[i])

		# auto-sorting feature
		score_table = list(score_table)
		score_table.sort(key=lambda col:(col[5], col[6]))

		for val in score_table:
			# deal with score that does not come out
			if val[7] is None:
				val = list(val)
				val[7] = ''
				val = tuple(val)
			self.__score_view.insert('', 'end', values=val)
		self.__score_view.pack()
		self.__main_window.mainloop()

	def __set__geometry(self, width, height):
		# put window in the center of the screen
		offset_width = (self.__main_window.winfo_screenwidth() - width) // 5 * 2
		offset_height = (self.__main_window.winfo_screenheight() - height) // 5 * 2
		self.__main_window.geometry("%sx%s+%s+%s" % (width, height, offset_width, offset_height))
