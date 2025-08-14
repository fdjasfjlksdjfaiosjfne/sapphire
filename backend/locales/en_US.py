def __getattr__(name):
    return MISSING_LOCALE.format(name)

MISSING_LOCALE = "<MISSING LOCALE ID ('{0}')>"
