"""
Data checker.

Perform type_check and range_check for data types.
"""


def type_check(val, _type):
    """
    Data type validation.

    Check a value's type ('val') in a type list ('_type').
    """
    return True if type(val) in _type else False


def range_check(val, lb, ub):
    """
    Data range validation.

    'val' should have attribute __lt__ and __gt__.
    'lb', 'ub' should be of the same type as 'val'.
    'lb' means lowerbound and 'ub' means upperbound.
    """
    return True if hasattr(val, '__lt__') and hasattr(val, '__gt__') and \
                   type(val) == type(lb) and type(val) == type(ub) and \
                   lb <= val <= ub else False
