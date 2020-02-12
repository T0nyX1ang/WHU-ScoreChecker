# WHU-ScoreChecker

![WHU-ScoreChecker App](https://github.com/T0nyX1ang/WHU-ScoreChecker/workflows/WHU-ScoreChecker%20App/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/31549674927500a089ca/maintainability)](https://codeclimate.com/github/T0nyX1ang/WHU-ScoreChecker/maintainability)
[![codecov](https://codecov.io/gh/T0nyX1ang/WHU-ScoreChecker/branch/master/graph/badge.svg)](https://codecov.io/gh/T0nyX1ang/WHU-ScoreChecker)
![License](https://img.shields.io/github/license/T0nyX1ang/WHU-ScoreChecker?color=blue)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/T0nyX1ang/WHU-ScoreChecker)

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

* Some query models is included this project on Github. They are inside the `./static` directory.
* If you just want to check all of your scores, load the `./static/default.json` model.
* If you want to do different jobs, take a look at the `./static/example.json` model, it includes all you need.
* The query model parser is under construction and can't deal with very difficult jobs at this time.

### Installation

* If you want to use pip:
```bash
	# Note that query model examples are not included when using pip
	pip install WHU-ScoreChecker
```

* If you want to build from codes:
```bash
	# clone this repository, or download it from the release page
	git clone https://github.com/T0nyX1ang/WHU-ScoreChecker.git
	# change your directory
	cd WHU-ScoreChecker
	# install dependencies (pip on Windows, pip3 on Linux)
	pip3/pip install -r requirements.txt
	# install the app
	python3/py -3 setup.py install
```

### Run the app

* The app should be in your `$PATH$` first. If it is, just type the following line in your shell:
```bash
	scorechecker
```

### Integration and contribution

* Integration and contribution are warmly welcomed.
* If you want to integrate our codes in your project, just import some of the following to continue:
```python
	import scorechecker
	import scorechecker.course
	import scorechecker.image
	import scorechecker.net
	import scorechecker.util
```
* If you want to validate your query model without invoking the graphical interface:
```python
	from scorechecker.loader import load_query_model
	load_query_model('your-model-name.json')
```

## License

This project uses `MIT License`. Please refer to `LICENSE` for more details.
