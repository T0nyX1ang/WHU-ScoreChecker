import unittest

from app.course.extract import *
from app.course.query import *
from app.course.score import *

test_score_table = {
    ('课程01', '公共必修', 0.5, '学院01', '普通', 2016, 1, 89.0),
    ('课程02', '公共选修', 3.0, '学院02', '普通', 2016, 1, 84.0),
    ('课程03', '专业必修', 1.0, '学院03', '普通', 2016, 2, 65.0),
    ('课程04', '专业选修', 4.0, '学院03', '普通', 2017, 1, 90.0),
    ('课程05', '公共必修', 4.5, '学院02', '普通', 2017, 1, 100.0),
    ('课程06', '公共选修', 2.0, '学院01', '普通', 2017, 2, 60.0),
    ('课程07', '专业必修', 5.0, '学院01', '普通', 2017, 2, 85.0),
    ('课程08', '专业必修', 6.0, '学院03', '普通', 2017, 2, 68.0),
    ('课程09', '专业必修', 8.0, '学院04', '普通', 2018, 1, 75.0),
    ('课程10', '公共必修', 1.5, '学院02', '普通', 2018, 1, 63.0),
    ('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None),
    ('课程12', '专业选修', 5.5, '学院02', '普通', 2018, 2, 78.0),
    ('课程13', '专业选修', 3.0, '学院03', '辅修', 2018, 3, 79.0),
    ('课程14', '专业必修', 4.0, '学院04', '辅修', 2019, 1, 72.0),
    ('课程15', '公共选修', 2.0, '学院05', '普通', 2019, 1, 73.0),
    ('课程16', '专业必修', 3.0, '学院06', '辅修', 2019, 1, 82.0),
}


class TestExtract(unittest.TestCase):
    def test_convert(self):
        # make sure the conversions are normally changed.
        self.assertIs(convert('start_year'), search_start_year)
        self.assertIs(convert('stop_year'), search_stop_year)
        self.assertIs(convert('score_come_out'), search_score_come_out)
        self.assertIs(convert('min_score'), search_min_score)
        self.assertIs(convert('max_score'), search_max_score)
        self.assertIs(convert('min_credit'), search_min_credit)
        self.assertIs(convert('max_credit'), search_max_credit)
        self.assertIs(convert('study_type'), search_study_type)
        self.assertIs(convert('course_type'), search_course_type)
        self.assertIs(convert('course_academy'), search_course_academy)
        self.assertIs(convert('course_name'), search_course_name)
        self.assertRaises(KeyError, convert, 'not_into_it')

    def test_extract(self):

        without_display = {
            "query": {
                "without_display": {
                    "start_year": [2017, 1],
                    "stop_year": [2018, 3],
                    "score_come_out": True,
                    "min_score": 85.0,
                    "max_score": 98.0,
                    "min_credit": 0.5,
                    "max_credit": 5.0,
                    "study_type": ["普通"],
                    "course_type": ["专业必修", "专业选修"],
                    "course_academy": [],
                    "course_name": []
                }
            },
        }

        null_display = {
            "query": {
                "null_display": {
                    "course_academy": [],
                    "course_name": []
                }
            },
            "display": "null_display"
        }

        example_display = {
            "query": {
                "example_table": {
                    "start_year": [2017, 1],
                    "stop_year": [2018, 3],
                    "score_come_out": True,
                    "min_score": 85.0,
                    "max_score": 98.0,
                    "min_credit": 0.5,
                    "max_credit": 5.0,
                    "study_type": ["普通"],
                    "course_type": ["专业必修", "专业选修"],
                }
            },
            "display": "example_table"
        }

        course_display = {
            "query": {
                "course_table": {
                    "course_name": ["课程01", "课程05", "课程10", "课程15"],
                    "course_academy": ["学院01", "学院02"]
                }
            },
            "display": "course_table"
        }

        self.assertEqual(extract(test_score_table, without_display),
                         test_score_table)
        self.assertEqual(extract(test_score_table, null_display), set())
        self.assertEqual(
            extract(test_score_table, example_display), {
                ('课程04', '专业选修', 4.0, '学院03', '普通', 2017, 1, 90.0),
                ('课程07', '专业必修', 5.0, '学院01', '普通', 2017, 2, 85.0),
            })
        self.assertEqual(
            extract(test_score_table, course_display), {
                ('课程01', '公共必修', 0.5, '学院01', '普通', 2016, 1, 89.0),
                ('课程05', '公共必修', 4.5, '学院02', '普通', 2017, 1, 100.0),
                ('课程10', '公共必修', 1.5, '学院02', '普通', 2018, 1, 63.0),
            })


class TestQuery(unittest.TestCase):
    def test_start_year(self):
        self.assertEqual(search_start_year(test_score_table, [2015, 1]),
                         test_score_table)
        self.assertEqual(
            search_start_year(test_score_table, [2017, 40]), {
                ('课程09', '专业必修', 8.0, '学院04', '普通', 2018, 1, 75.0),
                ('课程10', '公共必修', 1.5, '学院02', '普通', 2018, 1, 63.0),
                ('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None),
                ('课程12', '专业选修', 5.5, '学院02', '普通', 2018, 2, 78.0),
                ('课程13', '专业选修', 3.0, '学院03', '辅修', 2018, 3, 79.0),
                ('课程14', '专业必修', 4.0, '学院04', '辅修', 2019, 1, 72.0),
                ('课程15', '公共选修', 2.0, '学院05', '普通', 2019, 1, 73.0),
                ('课程16', '专业必修', 3.0, '学院06', '辅修', 2019, 1, 82.0),
            })
        self.assertEqual(search_start_year(test_score_table, [2020, 1]), set())

    def test_stop_year(self):
        self.assertEqual(search_stop_year(test_score_table, [2015, 1]), set())
        self.assertEqual(
            search_stop_year(test_score_table, [2017, 40]), {
                ('课程01', '公共必修', 0.5, '学院01', '普通', 2016, 1, 89.0),
                ('课程02', '公共选修', 3.0, '学院02', '普通', 2016, 1, 84.0),
                ('课程03', '专业必修', 1.0, '学院03', '普通', 2016, 2, 65.0),
                ('课程04', '专业选修', 4.0, '学院03', '普通', 2017, 1, 90.0),
                ('课程05', '公共必修', 4.5, '学院02', '普通', 2017, 1, 100.0),
                ('课程06', '公共选修', 2.0, '学院01', '普通', 2017, 2, 60.0),
                ('课程07', '专业必修', 5.0, '学院01', '普通', 2017, 2, 85.0),
                ('课程08', '专业必修', 6.0, '学院03', '普通', 2017, 2, 68.0),
            })
        self.assertEqual(search_stop_year(test_score_table, [2020, 1]),
                         test_score_table)

    def test_score_come_out(self):
        self.assertEqual(search_score_come_out(test_score_table, False),
                         {('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None)})
        self.assertEqual(
            search_score_come_out(test_score_table, True), {
                ('课程01', '公共必修', 0.5, '学院01', '普通', 2016, 1, 89.0),
                ('课程02', '公共选修', 3.0, '学院02', '普通', 2016, 1, 84.0),
                ('课程03', '专业必修', 1.0, '学院03', '普通', 2016, 2, 65.0),
                ('课程04', '专业选修', 4.0, '学院03', '普通', 2017, 1, 90.0),
                ('课程05', '公共必修', 4.5, '学院02', '普通', 2017, 1, 100.0),
                ('课程06', '公共选修', 2.0, '学院01', '普通', 2017, 2, 60.0),
                ('课程07', '专业必修', 5.0, '学院01', '普通', 2017, 2, 85.0),
                ('课程08', '专业必修', 6.0, '学院03', '普通', 2017, 2, 68.0),
                ('课程09', '专业必修', 8.0, '学院04', '普通', 2018, 1, 75.0),
                ('课程10', '公共必修', 1.5, '学院02', '普通', 2018, 1, 63.0),
                ('课程12', '专业选修', 5.5, '学院02', '普通', 2018, 2, 78.0),
                ('课程13', '专业选修', 3.0, '学院03', '辅修', 2018, 3, 79.0),
                ('课程14', '专业必修', 4.0, '学院04', '辅修', 2019, 1, 72.0),
                ('课程15', '公共选修', 2.0, '学院05', '普通', 2019, 1, 73.0),
                ('课程16', '专业必修', 3.0, '学院06', '辅修', 2019, 1, 82.0),
            })

    def test_min_score(self):
        self.assertEqual(
            search_min_score(test_score_table, 85.0), {
                ('课程01', '公共必修', 0.5, '学院01', '普通', 2016, 1, 89.0),
                ('课程04', '专业选修', 4.0, '学院03', '普通', 2017, 1, 90.0),
                ('课程05', '公共必修', 4.5, '学院02', '普通', 2017, 1, 100.0),
                ('课程07', '专业必修', 5.0, '学院01', '普通', 2017, 2, 85.0),
            })

    def test_max_score(self):
        self.assertEqual(
            search_max_score(test_score_table, 69.9), {
                ('课程03', '专业必修', 1.0, '学院03', '普通', 2016, 2, 65.0),
                ('课程06', '公共选修', 2.0, '学院01', '普通', 2017, 2, 60.0),
                ('课程08', '专业必修', 6.0, '学院03', '普通', 2017, 2, 68.0),
                ('课程10', '公共必修', 1.5, '学院02', '普通', 2018, 1, 63.0),
            })

    def test_min_credit(self):
        self.assertEqual(
            search_min_credit(test_score_table, 5.0), {
                ('课程07', '专业必修', 5.0, '学院01', '普通', 2017, 2, 85.0),
                ('课程08', '专业必修', 6.0, '学院03', '普通', 2017, 2, 68.0),
                ('课程09', '专业必修', 8.0, '学院04', '普通', 2018, 1, 75.0),
                ('课程12', '专业选修', 5.5, '学院02', '普通', 2018, 2, 78.0),
            })

    def test_max_credit(self):
        self.assertEqual(
            search_max_credit(test_score_table, 2.0), {
                ('课程01', '公共必修', 0.5, '学院01', '普通', 2016, 1, 89.0),
                ('课程03', '专业必修', 1.0, '学院03', '普通', 2016, 2, 65.0),
                ('课程06', '公共选修', 2.0, '学院01', '普通', 2017, 2, 60.0),
                ('课程10', '公共必修', 1.5, '学院02', '普通', 2018, 1, 63.0),
                ('课程15', '公共选修', 2.0, '学院05', '普通', 2019, 1, 73.0),
            })

    def test_study_type(self):
        self.assertEqual(
            search_study_type(test_score_table, ['辅修', 'Abnormal']), {
                ('课程13', '专业选修', 3.0, '学院03', '辅修', 2018, 3, 79.0),
                ('课程14', '专业必修', 4.0, '学院04', '辅修', 2019, 1, 72.0),
                ('课程16', '专业必修', 3.0, '学院06', '辅修', 2019, 1, 82.0),
            })

    def test_course_type(self):
        self.assertEqual(
            search_course_type(test_score_table, ['专业必修', '专业选修', 'Abnormal']),
            {
                ('课程03', '专业必修', 1.0, '学院03', '普通', 2016, 2, 65.0),
                ('课程04', '专业选修', 4.0, '学院03', '普通', 2017, 1, 90.0),
                ('课程07', '专业必修', 5.0, '学院01', '普通', 2017, 2, 85.0),
                ('课程08', '专业必修', 6.0, '学院03', '普通', 2017, 2, 68.0),
                ('课程09', '专业必修', 8.0, '学院04', '普通', 2018, 1, 75.0),
                ('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None),
                ('课程12', '专业选修', 5.5, '学院02', '普通', 2018, 2, 78.0),
                ('课程13', '专业选修', 3.0, '学院03', '辅修', 2018, 3, 79.0),
                ('课程14', '专业必修', 4.0, '学院04', '辅修', 2019, 1, 72.0),
                ('课程16', '专业必修', 3.0, '学院06', '辅修', 2019, 1, 82.0),
            })

    def test_course_academy(self):
        self.assertEqual(
            search_course_academy(test_score_table,
                                  ['学院03', '学院06', '学院07', 'Abnormal']),
            {
                ('课程03', '专业必修', 1.0, '学院03', '普通', 2016, 2, 65.0),
                ('课程04', '专业选修', 4.0, '学院03', '普通', 2017, 1, 90.0),
                ('课程08', '专业必修', 6.0, '学院03', '普通', 2017, 2, 68.0),
                ('课程13', '专业选修', 3.0, '学院03', '辅修', 2018, 3, 79.0),
                ('课程16', '专业必修', 3.0, '学院06', '辅修', 2019, 1, 82.0),
            })

    def test_course_name(self):
        self.assertEqual(
            search_course_name(test_score_table, ['课程01', '课程02', '不存在的课程']), {
                ('课程01', '公共必修', 0.5, '学院01', '普通', 2016, 1, 89.0),
                ('课程02', '公共选修', 3.0, '学院02', '普通', 2016, 1, 84.0),
            })


class TestScore(unittest.TestCase):
    def test_single_score_to_gpa(self):
        self.assertEqual(calculate_single_gpa(None), 0.0)
        self.assertEqual(calculate_single_gpa(-1.0), 0.0)
        self.assertEqual(calculate_single_gpa(101.0), 0.0)
        self.assertEqual(calculate_single_gpa(0.0), 0.0)
        self.assertEqual(calculate_single_gpa(59.0), 0.0)
        self.assertEqual(calculate_single_gpa(60.0), 1.0)
        self.assertEqual(calculate_single_gpa(63.0), 1.0)
        self.assertEqual(calculate_single_gpa(64.0), 1.5)
        self.assertEqual(calculate_single_gpa(67.0), 1.5)
        self.assertEqual(calculate_single_gpa(68.0), 2.0)
        self.assertEqual(calculate_single_gpa(71.0), 2.0)
        self.assertEqual(calculate_single_gpa(72.0), 2.3)
        self.assertEqual(calculate_single_gpa(74.0), 2.3)
        self.assertEqual(calculate_single_gpa(75.0), 2.7)
        self.assertEqual(calculate_single_gpa(77.0), 2.7)
        self.assertEqual(calculate_single_gpa(78.0), 3.0)
        self.assertEqual(calculate_single_gpa(81.0), 3.0)
        self.assertEqual(calculate_single_gpa(82.0), 3.3)
        self.assertEqual(calculate_single_gpa(84.0), 3.3)
        self.assertEqual(calculate_single_gpa(85.0), 3.7)
        self.assertEqual(calculate_single_gpa(89.0), 3.7)
        self.assertEqual(calculate_single_gpa(90.0), 4.0)
        self.assertEqual(calculate_single_gpa(100.0), 4.0)

    def test_calculate_gpa(self):
        self.assertEqual(calculate_gpa(set()), 0.0)
        self.assertEqual(
            calculate_gpa({('课程05', '公共必修', 4.5, '学院02', '普通', 2017, 1, 100.0),
                           ('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None)
                           }), (4.5 * 4 + 2.5 * 0) / (4.5 + 2.5))

    def test_calculate_score(self):
        self.assertEqual(calculate_score(set()), 0.0)
        self.assertEqual(
            calculate_score({
                ('课程10', '公共必修', 1.5, '学院02', '普通', 2018, 1, 63.0),
                ('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None),
                ('课程12', '专业选修', 5.5, '学院02', '普通', 2018, 2, 78.0),
                ('课程13', '专业选修', 3.0, '学院03', '辅修', 2018, 3, 79.0),
            }), (1.5 * 63.0 + 2.5 * 0 + 5.5 * 78.0 + 3.0 * 79.0) /
            (1.5 + 2.5 + 5.5 + 3.0))


# class TestOptimize(unittest.TestCase):
#     # The tests will come out when this feature comes out fully.
#     pass
