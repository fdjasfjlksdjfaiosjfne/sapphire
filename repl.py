# Credit to: https://www.youtube.com/playlist?list=PL_2VhOvlMk4UHGqYCLWc6GO8FaPl8fQTh
from parser.lexer import tokenize
from parser.parser import produce_program_ast
from runtime.interpreter import evaluate
from runtime.env import setup_global_scope

global_env = setup_global_scope()

while True:
    # Takes the input
    inpt = input(">>> ")
    
    # Process it
    tkns = tokenize(inpt, {})
    # print(tkns, end = "\n\n")
    ast_node = produce_program_ast(tkns)
    # print(ast_node, end = "\n\n")
    for i in ast_node.body:
        val = evaluate(i, global_env)
        if val is not None:
            print(val.__sap_props__["__str__"](val))

# Comment guidelines (in general)
# Note that this is initially written about 1 or 2 years ago so...a lot has changed regarding me and this thing since then
# ! (Red, Bold): Explain an error that is going to be thrown or (inclusive) its condition
# @ (Orange): Deprecation notices
# TODO (Orange, bold): ...Do I need to explain this one?
# ~ (Yellow): Temporary hacks, known bugs or warnings
# $ (Lime): Context headers of a code section/function. Might act as ? sometimes because...uh...yes
# * (Green): Not really used much as of now, initially for affirming confirmation and stuff
# > (Teal): Not really used much as of now, initially for desicions in the process of making code
# % (Sapphire): Initially performance metrics, now unassigned because I don't 
# % care about performance enough to give a dedicated color to it :melting_face:
# ? (Blue): Explaination of a code snippet. Initially takes the place of $ when it doesn't exist
# & (Lavender): I forgot :<
# ^ (Purple): Category divider
# # (White): Standard Comments
# // (Gray, Strikethrough): Scraped code
# (Gray): When I don't feel like assign a tag to the comment

# Bonus: Adding ` (backtick) before a tag or just use it as a tag inverts its background color and text color
# Not used for anything, past me just feel like making it for no reason
# `! Red
# `@ Orange
# `~ Yellow
# `* Green
# `> Teal
# `$ Lime
# `% Sapphire
# `? Blue
# `& Lavender
# `^ Purple
# `# White
# `// Strikethrough
# ` Gray