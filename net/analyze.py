import bs4
import lxml

# Analyze the page to extract important infomation

def get_captcha_id(content):
    # get captcha ID 
    if content is None:
        return None
    print('Extracting captcha ID ...')
    b = bs4.BeautifulSoup(content, features='lxml')
    styles = b.style.get_text()
    # As the captcha image is exclusive, the result is ONLY one.
    search_string = ['#captcha-img1', '#captcha-img2', '#captcha-img3', '#captcha-img4', '#captcha-img']
    result = [b.select(val) for val in search_string if val not in styles]
    if len(result) != 1:
        print('Failed to extract captcha ID.')
        return None
    else:
        captcha_id = result[0][0]['src']
        print('Captcha ID is set to:', captcha_id)
    return captcha_id

def get_login_id(content):
    # get login id
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
        print('Failed to extract login ID.')
        return None

def get_csrf_token(content):
    # get CSRF token
    if content is None:
        return None
    print('Extracting CSRF token ...')
    try:
        b = bs4.BeautifulSoup(content, features='lxml')
        csrf_prefetch = str(b.find(id='system'))
        start = csrf_prefetch.find('csrftoken=') + 10
        csrf_token = csrf_prefetch[start: start + 36]
        print('CSRF token is set to:', csrf_token)
        return csrf_token
    except Exception as e:
        print('Failed to extract CSRF token.')
        return None

def __convert_to_float(score):
    if len(score) == 0:
        return None
    else:
        return float(score)

def get_raw_score_table(content):
    # get raw score table
    if content is None:
        return None
    print('Fetching raw score table ...')
    try:
        b = bs4.BeautifulSoup(content, features='lxml')
        raw_score_table = b.find_all('td')
        print('Raw score table has been fetched successfully ...')
        return raw_score_table
    except Exception as e:
        print('Failed to fetch the raw score table.')
        return None

def get_score_table(raw_score_table):
    print('Refining raw score table ...')
    score_table, single, rec = set(), [], 0
    for current in raw_score_table:
        item = current.get_text().replace('\n','').replace('\r','').replace(' ','').replace('\t','')
        single.append(item)
        rec += 1
        if (rec == 12):
            # convert data types
            refined_single = (single[0], single[1], __convert_to_float(single[4]), single[6], \
                              single[7], int(single[8]), int(single[9]), __convert_to_float(single[10]))
            score_table.add(refined_single)
            single, rec = [], 0
    return score_table
