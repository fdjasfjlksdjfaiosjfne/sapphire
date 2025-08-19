import typing

from backend import errors

def asserting_config_dict(conf: dict) -> None:
    """Act as additional validations to a given config dict.
    
    Note that the function assumes that it has been check by the config schema.

    If any validation fails, throw errors.ConfigError.
    """
    try:
        _assert_integer_bases(conf)
        _assert_matching_values(conf)
    except AssertionError as e:
        raise errors.ConfigError(*e.args)

def _assert_integer_bases(conf: dict):
    cust: dict = conf.get("customization", conf.get("customisation", {}))
    literals: dict = cust.get("literals", {})
    numbers: dict = literals.get("numbers", {})
    int_bases: dict = numbers.get("integer_base_literals", {})
    assert not (int_bases.values() and not any(int_bases.values())), "At least 1 of the integer bases should be allowed"

def _assert_matching_values(conf: dict) -> None:
    pass