import typing

ALTERNATE_SPELLING = "Both the American ({}) and the British ({}) spelling of a config option are present"
def assert_alternate_spelling(conf: dict):
    cust: dict = conf.get("customization", conf.get("customisation", {}))
    uncat: dict = cust.get("uncategorized", {})
    objects: dict = cust.get("objects", {})
    functions: dict = objects.get("functions", {})
    fn_arguments: dict = functions.get("arguments", {})

    for american, british, location in [("customization", "customisation", conf),
                              ("mutableValueAssignmentBehavior", "mutableValueAssignmentBehaviour", uncat),
                              ("mutableValueAsDefaultBehavior", "mutableValueAsDefaultBehaviour", fn_arguments)]:
        assert not (american in conf and british in conf), ALTERNATE_SPELLING.format(american, british)

def assert_integer_bases(conf: dict):
    cust: dict = conf.get("customization", conf.get("customisation", {}))
    literals: dict = cust.get("literals", {})
    numbers: dict = literals.get("numbers", {})
    int_bases: dict = numbers.get("integer_base_literals", {})
    assert int_bases.values() and not any(int_bases.values()), "At least 1 of the integer bases should be allowed"

def assert_matching_values(conf: dict) -> None:
    pass

def asserting_config_dict(conf: dict) -> None:
    assert_alternate_spelling(conf)
    assert_integer_bases(conf)
    assert_matching_values(conf)