import itertools

from backend.config import CONFIG

def permutations(
    possible_strs: list[str],
    forbidden_matches: list[list[str]] | None = None
) -> list[str]:
    """Return all permutations of a given characters.

    The optional `forbidden_matches` argument accept a list of lists, each containing
     strings. This'll allow you to get rid of permutations that have all characters
     contain in each list containing in it.

    For example: 
    - With [["f", "t"]], the permutation "ptl" and "fap" are allowed, but not "wtf".
    - With [["f", "t"], ["d", "r"]], the permutation "rt", "df" are allowed, but not 
    "ft", not "dr".

    The optional `forbidden_matches` argument accept a list of strings. This'll allow
     you to get rid of permutatons that does not have all of the forced strings.
    """
    forbidden_matches = forbidden_matches or []
    res = []
    # Generate all non-empty permutations
    for n in range(1, len(possible_strs) + 1):
        # & itertools saves the day again
        for perm in itertools.permutations(possible_strs, n):
            skip = False
            
            # ? Check if this permutation contains all elements of any forbidden match
            for forbidden in forbidden_matches:
                if all(f in perm for f in forbidden):
                    skip = True
                    break
                    
            if not skip:
                prefix = ''.join(perm)
                if prefix not in res:
                    res.append(prefix)
    return res

def find_all_common_str_formats() -> list[str]:
    ls: list[str] = []
    str_config = CONFIG.customization.literals.strings
    
    return ls
import itertools

from backend.config import CONFIG

def permutations(
    possible_strs: list[str],
    forbidden_matches: list[list[str]] | None = None
) -> list[str]:
    """Return all permutations of a given characters.

    The optional `forbidden_matches` argument accept a list of lists, each containing
     strings. This'll allow you to get rid of permutations that have all characters
     contain in each list containing in it.

    For example: 
    - With [["f", "t"]], the permutation "ptl" and "fap" are allowed, but not "wtf".
    - With [["f", "t"], ["d", "r"]], the permutation "rt", "df" are allowed, but not 
    "ft", not "dr".

    The optional `forbidden_matches` argument accept a list of strings. This'll allow
     you to get rid of permutatons that does not have all of the forced strings.
    """
    forbidden_matches = forbidden_matches or []
    res = []
    # Generate all non-empty permutations
    for n in range(1, len(possible_strs) + 1):
        # & itertools saves the day again
        for perm in itertools.permutations(possible_strs, n):
            skip = False
            
            # ? Check if this permutation contains all elements of any forbidden match
            for forbidden in forbidden_matches:
                if all(f in perm for f in forbidden):
                    skip = True
                    break
            
            if not skip:
                prefix = ''.join(perm)
                if prefix not in res:
                    res.append(prefix)
    return res

def find_all_common_str_formats() -> list[str]:
    ls: list[str] = []
    str_config = CONFIG.customization.literals.strings
    for category in (str_config.interpolation,
                     str_config.multiline,
                     str_config.raw_string):
        pass
    return ls