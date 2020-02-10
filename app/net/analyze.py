"""
Analyze the page to extract important infomation.

Almost all of the functions are based on BeautifulSoup.
Although lxml library is not explicitly imported, it's needed.
Information extracted is: captcha_id, login_id, csrf_token, score_table.
"""

import bs4


def get_captcha_id(content):
    """
    Get the captcha ID from HTML page.

    The captcha ID is extracted by filtering non-displaying image tags.
    """
    try:
        print('Extracting captcha ID ...')
        b = bs4.BeautifulSoup(content, features='lxml')
        styles = b.style.get_text()
        # As the captcha image is exclusive, the result is ONLY one.
        search_string = [
            '#captcha-img1', '#captcha-img2', '#captcha-img3', '#captcha-img4',
            '#captcha-img'
        ]
        result = [b.select(val) for val in search_string if val not in styles]
        if len(result) != 1:
            raise ValueError('')
        captcha_id = result[0][0]['src']
        print('Captcha ID is set to:', captcha_id)
        return captcha_id
    except Exception as e:
        print('Failed to extract captcha ID:', e)
        return None


def get_login_id(content):
    """
    Get the login ID from HTML page.

    The login ID is extracted from [POST] form hyperlink.
    """
    print('Extracting login ID ...')
    try:
        b = bs4.BeautifulSoup(content, features='lxml')
        login_box = b.find(id='loginBox')
        login_id = login_box.form['action']
        print('Login ID is set to:', login_id)
        return login_id
    except Exception as e:
        print('Failed to extract login ID:', e)
        return None


def get_csrf_token(content):
    """
    Get the CSRF token from HTML page.

    The CSRF token is extracted when the user logs in successfully.
    """
    print('Extracting CSRF token ...')
    try:
        b = bs4.BeautifulSoup(content, features='lxml')
        csrf_prefetch = str(b.find(id='system'))
        start = csrf_prefetch.find('csrftoken=')
        if start == -1:
            raise ValueError('Unable to find a CSRF token in this page.')
        csrf_token = csrf_prefetch[start + 10:start + 46]
        print('CSRF token is set to:', csrf_token)
        return csrf_token
    except Exception as e:
        print('Failed to extract CSRF token:', e)
        return None


def _convert_to_float(score):
    """
    Convert a string ('score') to float.

    If the string is empty, return None.
    If the string is float-like, return its float.
    """
    if len(score) == 0:
        return None
    else:
        return float(score)


def get_score_table(content):
    """
    Get the score table from HTML page.

    The score table is a refined version of the raw score table.
    It contains a set of tuples, which makes it easy to calculate further.
    The items are: course_name (str), course_type (str), credit (float),
                   course_academy (str), study_type (str), year (int),
                   semester (int) and score (float).
    """
    print('Fetching raw score table ...')
    try:
        b = bs4.BeautifulSoup(content, features='lxml')
        score_table = set()
        raw_score_table = [
            item.get_text().replace('\n', '').replace('\r', '').replace(
                ' ', '').replace('\t', '') for item in b.find_all('td')
        ]
        total_course = len(raw_score_table) // 12
        for i in range(0, total_course):
            score_table.add(
                (raw_score_table[i * 12], raw_score_table[i * 12 + 1],
                 _convert_to_float(raw_score_table[i * 12 + 4]),
                 raw_score_table[i * 12 + 6], raw_score_table[i * 12 + 7],
                 int(raw_score_table[i * 12 + 8]),
                 int(raw_score_table[i * 12 + 9]),
                 _convert_to_float(raw_score_table[i * 12 + 10])))
        print('Score table has been fetched successfully ...')
        return score_table
    except Exception as e:
        print('Failed to fetch the score table:', e)
        return None
