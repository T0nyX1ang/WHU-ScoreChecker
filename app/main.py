"""
Main app.

This is the CORE part of this project and should be the only file to be
executed when you are just a user. This file connects all the files needed.
"""

from auth import auth_procedure
from config import ConfigApp
from course import extract
from result import ResultApp


class ScoreCheckerApp(object):
    """
    Main app (ScoreChecker App).

    This is the main part to deal with everything.
    """

    def __init__(self, retries=3):
        """
        Initialization for the app.

        Just invoke this function to use it.
        """
        self.__retries = retries  # global retry counter
        print('Initializing configuration app ...')
        capp = ConfigApp()
        if capp.get_status():
            print('Fetching infomation for configuration app ...')
            _id, password, captcha_model, query_model = capp.get_credentials()
        else:
            return

        score_table = auth_procedure(_id, password, captcha_model,
                                     retries=self.__retries)
        if score_table:
            print('Authenticating successfully, querying ...')
            result_score_table = extract.extract(score_table, query_model)
            ResultApp(result_score_table)
            print('Querying successfully, see you next time.')

if __name__ == '__main__':
    app = ScoreCheckerApp()
