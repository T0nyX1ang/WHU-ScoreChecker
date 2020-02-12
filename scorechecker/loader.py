"""
Model validation and loader.

Validate a captcha model or a query model and load the model.
Available functions are load_captcha_model and load_query_model.
Models are loaded based on their filenames.
"""

from .util.check import type_check, range_check


def load_captcha_model(filename):
    """
    Load a captcha model.

    This function loads a captcha model from Keras.
    The model should be HDF5 format with full structure and weights.
    """
    from keras.models import load_model
    try:
        print('Trying to load the captcha model ...')
        model = load_model(filename)
        print('Model is loaded successfully ...')
        return model
    except Exception as e:
        print('Failed to load the model:', e)
        return None


def validate_single_key_value(key, value):
    """
    Single key-value validation.

    Including type_check and range_check,
    and range check is a subset of type_check.
    This function is used to validate the query model.
    """
    allowed_query = {
        'start_year': lambda val: type_check(val, [list]),
        'stop_year': lambda val: type_check(val, [list]),
        'score_come_out': lambda val: type_check(val, [bool]),
        'min_score': lambda val: range_check(val, 0.0, 100.0),
        'max_score': lambda val: range_check(val, 0.0, 100.0),
        'min_credit': lambda val: range_check(val, 0.0, 8.0),
        'max_credit': lambda val: range_check(val, 0.0, 8.0),
        'study_type': lambda val: type_check(val, [list]),
        'course_type': lambda val: type_check(val, [list]),
        'course_academy': lambda val: type_check(val, [list]),
        'course_name': lambda val: type_check(val, [list]),
    }

    if key not in allowed_query:
        raise KeyError('Your key [%s] is not in the allowed list.' % key)
    elif not allowed_query[key](value):
        raise ValueError(
            'Your key-value pair [%s: %s] does not pass the check.' %
            (key, value))


def validate_query_model(model):
    """
    Validate query model.

    Validate the 'query' key in query model.
    """
    for item in model['query'].keys():
        for each_key in model['query'][item].keys():
            validate_single_key_value(
                each_key,
                model['query'][item][each_key]
            )  # type and range checks


def validate_display_model(model):
    """
    Validate query model.

    Validate the 'display' key in query model.
    'display' keys should be in the 'query' keys
    """
    if model.get('display') and model['display'] not in model['query'].keys():
        raise KeyError(
            'Your display score table name [%s] must append in the query keys.'
            % model['display'])


def load_query_model(filename):
    """
    Load and validate a query model.

    This function loads a query model from disk.
    The model should be JSON format with at least 'query' key.
    """
    import json
    try:
        print('Trying to load the query model ...')
        with open(filename, 'r', encoding='utf-8') as f:
            fin = f.read()
            model = json.loads(fin)
        validate_query_model(model)
        validate_display_model(model)
        print('Model is loaded successfully ...')
        return model
    except Exception as e:
        print('Failed to load the model:', e)
        return None
