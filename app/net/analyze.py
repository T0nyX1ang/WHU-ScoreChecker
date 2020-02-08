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
    if content is None:
        return None
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
        print('Failed to extract captcha ID.')
        return None
    else:
        captcha_id = result[0][0]['src']
        print('Captcha ID is set to:', captcha_id)
    return captcha_id


def get_login_id(content):
    """
    Get the login ID from HTML page.

    The login ID is extracted from [POST] form hyperlink.
    """
    if content is None:
        return None
    try:
        print('Extracting login ID ...')
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
    if content is None:
        return None
    print('Extracting CSRF token ...')
    try:
        b = bs4.BeautifulSoup(content, features='lxml')
        csrf_prefetch = str(b.find(id='system'))
        start = csrf_prefetch.find('csrftoken=') + 10
        csrf_token = csrf_prefetch[start:start + 36]
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


def get_raw_score_table(content):
    """
    Get the raw score table from HTML page.

    The raw score table is extracted by all '<td>' tags.
    """
    if content is None:
        return None
    print('Fetching raw score table ...')
    try:
        b = bs4.BeautifulSoup(content, features='lxml')
        raw_score_table = b.find_all('td')
        print('Raw score table has been fetched successfully ...')
        return raw_score_table
    except Exception as e:
        print('Failed to fetch the raw score table:', e)
        return None


def get_score_table(raw_score_table):
    """
    Get the score table from raw score table.

    The score table is a refined version of the raw score table.
    It contains a set of tuples, which makes it easy to calculate further.
    The items are: course_name (str), course_type (str), credit (float),
                   course_academy (str), study_type (str), year (int),
                   semester (int) and score (float).
    """
    print('Refining raw score table ...')
    score_table, single, rec = set(), [], 0
    for current in raw_score_table:
        item = current.get_text().replace('\n', '').replace('\r', '').replace(
            ' ', '').replace('\t', '')
        single.append(item)
        rec += 1
        if (rec == 12):
            # convert data types
            refined = (single[0], single[1], _convert_to_float(single[4]),
                       single[6], single[7], int(single[8]),
                       int(single[9]), _convert_to_float(single[10]))
            score_table.add(refined)
            single, rec = [], 0
    return score_table
