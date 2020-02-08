# WHU-ScoreChecker

![WHU-ScoreChecker App](https://github.com/T0nyX1ang/WHU-ScoreChecker/workflows/WHU-ScoreChecker%20App/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/31549674927500a089ca/maintainability)](https://codeclimate.com/github/T0nyX1ang/WHU-ScoreChecker/maintainability)
[![License](https://img.shields.io/github/license/T0nyX1ang/WHU-ScoreChecker?color=blue)](github.com/T0nyX1ang/WHU-ScoreChecker/blob/master/LICENSE)

A simple, open-source and model-driven score checker for WHU.

## Important notice

* __Although enough freedom is given, you should be check your score carefully.__
* __This project uses Python 3.7, and works fine with Python 3.5-3.7.__

## Usage

### Captcha model download

* Please download the captcha model [here](https://github.com/T0nyX1ang/WHU-ScoreChecker/releases/tag/model-v1).
* The model is in `HDF5` format, which is a training result with over 2400000 entries and over 95% accuracy.
* You'd better put the downloaded model in the `./static` directory of this repository.

### Query model

* Some query models is included this project. They are inside the `./static` directory.
* If you just want to check all of your scores, load the `./static/default.json` model.
* If you want to do different jobs, take a look at the `./static/example.json` model, it includes all you need.
* The query model parser is under construction and can't deal with very difficult jobs at this time.

### App side (For users)

* Do the following things:
```bash
	# clone this repository, or download it from the release page
	git clone https://github.com/T0nyX1ang/WHU-ScoreChecker.git
	# change your directory
	cd WHU-ScoreChecker
	# install dependencies (pip on Windows, pip3 on Linux)
	pip3/pip install -r requirements.txt
	# run the app
	python3/py -3 main.py
	# enter your credentials and load models needed to continue ...
```

### Dev side (For developers)

* Some of the codes here can be utilized and applied in your own project, we recommend these:
	1. `./image` and `./model` tools with captcha model could be implemented in captcha recognition.
	2. `./net` tools works like a session, and could be implemented in similar condition.
	3. `./course` tools could be implemented in course querying situation.
* Functions initialized with `__` are private, and can't be used publicly.

## License

This project uses `MIT License`. Please refer to `LICENSE` for more details.
