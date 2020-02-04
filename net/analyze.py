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

def get_score_table(content):
	# get score table
	if content is None:
		return None
	print('Fetching score table ...')
	score_table = []
	try:
		b = bs4.BeautifulSoup(content, features='lxml')
		table_row = b.find_all('td')
		single, rec = [], 0
		for current in table_row:
			item = current.get_text().replace('\n','').replace('\r','').replace(' ','').replace('\t','')
			if rec in [0, 1, 4, 6, 7, 8, 9, 10]:
				single.append(item)
			rec += 1
			if (rec == 12):
				score_table.append(single)
				single, rec = [], 0
		score_table.sort(key=lambda stat:(stat[5], stat[6]))
		print('Score table has been fetched successfully ...')
		return score_table
	except Exception as e:
		print('Failed to fetch the score table.')
		return None
