# Credit to: https://www.youtube.com/playlist?list=PL_2VhOvlMk4UHGqYCLWc6GO8FaPl8fQTh
from parser.parser import Parser
from runtime.interpreter import evaluate
from runtime.env import setup_global_scope
from utils.common_bug_check import check
check()
global_env = setup_global_scope()

while True:
    # Takes the input
    inpt = input(">>> ")
    
    par = Parser(inpt)
    ast_node = par.parse_module()
    
    for i in ast_node.body:
        val = evaluate(i, global_env)
        if val is not None:
            print(val)

# Comment guidelines (in general)
# Note that this is initially written about 1 or 2 years ago so...a lot has changed regarding me and this thing since then

# ! (Red): Usually use to explain an error that is going to be thrown and a grasp why is it thrown
# ! This tag is initially bold
# Error: Alias for !
# Red: Alias for !, usually use only for the color rather than the tag's original purpose

# @ (Orange): Must-read texts
# @ Initially used exclusively for deprecation notices, now expanded
# Deprecated: Alias for @, use for its initial purpose
# README: Alias for @, use for its new, extended purpose
# Orange: Alias for @, usually use only for the color rather than the tag's original purpose
# Peach: Alias for @, usually use only for the color rather than the tag's original purpose

# TODO: (Orange, bold) ...Do I need to explain this one?

# ~ (Yellow): Temporary hacks, known bugs or warnings for the future
# Warning: Alias for ~
# Bug: Alias for ~
# Known Bug: Alias for ~
# Hack: Alias for ~
# Yellow: Alias for ~, usually use only for the color rather than the tag's original purpose

# $ (Green): Context headers of a code section, function, or a comment
# $ Ideally, it should be at the beginning of the section
# $ May act as ? sometimes
# Context: Alias for $
# Lime: Alias for $, usually use only for the color rather than the tag's original purpose
# $ Note that before the color reassignment of the * tag, this tag's color is called "Lime"
# Green: Alias for $, usually use only for the color rather than the tag's original purpose

# > (Teal): Cross-references
# > Initially for desicions in the process of making code
# Teal: Alias for >, usually use only for the color rather than the tag's original purpose

# * (Sky): Solutions to a problem that is express in a comment chain
# * Initially for simple affirmations
# * This tag is initially assigned as a green darker than $, but has been changed for theme consistency.
# Sky: Alias for *, usually use only for the color rather than the tag's original purpose

# % (Sapphire): Initially performance metrics, currently unused.
# % I just didn't use it enough, so I just scrap the original idea
# Sapphire: Alias for %, usually use only for the color rather than the tag's original purpose

# ? (Blue): Explaination of a code snippet, or reasons for a desicion that is noted in comments
# ? This initially takes the place of $ before it becomes a thing
# Explanation: Alias for ?
# Blue: Alias for ?, usually use only for the color rather than the tag's original purpose

# & (Lavender): Currently use as notes, mostly in an informal tone
# & May have other purposes in the past since this noting purpose is just getting adopted on (2025-6-22 (YYYY-MM-DD))
# & And I also forgot its former use :sob:
# Note: Alias for &, made for its new purpose
# Lavender: Alias for &, usually use only for the color rather than the tag's original purpose

# ^ (Purple): Use as a category division
# Category: Alias for ^
# Mauve: Alias for ^, usually use only for the color rather than the tag's original purpose
# Purple: Alias for ^, usually use only for the color rather than the tag's original purpose

# # (White): Standard Comments
# White: Alias for #, usually use only for the color rather than the tag's original purpose

# // (Gray, Strikethrough): Scraped code

# (Gray): When I don't feel like assign a tag to the comment
# Or when it is a temporary comment