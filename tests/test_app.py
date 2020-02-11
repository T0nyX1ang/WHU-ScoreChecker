import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'app'))

import pytest
from app.base import BaseApp
from app.config import ConfigApp
from app.result import ResultApp
from app.main import ScoreCheckerApp
import tkinter



def test_base_app(monkeypatch):
    monkeypatch.setattr(tkinter.Tk, 'mainloop', lambda x:0)
    base_app = BaseApp('hello_world', 400, 300)
    assert base_app.title() == 'hello_world'
    

def test_result_app(monkeypatch):
    monkeypatch.setattr(tkinter.Tk, 'mainloop', lambda x:0)
    result_app = ResultApp(set())
    result_app = ResultApp(
        {(('课程11', '专业选修', 2.5, '学院01', '普通', 2018, 2, None))})


def test_config_app(monkeypatch):
    monkeypatch.setattr(tkinter.Tk, 'mainloop', lambda x:0)
    config_app = ConfigApp()
    assert config_app.get_status() == False

