"""
Main app.

This is the CORE part of this project and should be the only file to be
executed when you are just a user. This file connects all the files needed.
"""

from .auth import auth_procedure
from .config import ConfigApp
from .course import extract
from .result import ResultApp


def run(retries=3):
    """
    Run the app.

    Just invoke this function to use it.
    """
    print('Initializing configuration app ...')
    capp = ConfigApp()
    if capp.get_status():
        print('Fetching infomation for configuration app ...')
        _id, password, captcha_model, query_model = capp.get_credentials()
    else:
        return

    score_table = auth_procedure(_id, password, captcha_model, retries=retries)
    if score_table:
        print('Authenticating successfully, querying ...')
        result_score_table = extract.extract(score_table, query_model)
        ResultApp(result_score_table)
        print('Querying successfully, see you next time.')
