# Comment styling
In this codebase, there are certain comment styling which exists to make comments look not as dull to read.
This is incorporate with a extension to color comments (like the Better Comments extension):
```py
# <tag> Comment Content
```
## Cheat Sheet
### Error (!)
This tag is used for annotating errors that are present in the line after the comment, and (usually), the reason of throwing.
```py
# ! No more edge cases
# ! Throw an error if the code reached this point
raise errors.InternalError
```

> [!warning]
> To prevent any possible confusion to a [shebang](https://en.wikipedia.org/wiki/Shebang_%28Unix%29), always add an extra space inbetween the `#` and the `!`.
> ```py
> # ! Do this
> #! Not this
> ```
## Technical Restrictions
Due to a limitation in the extension, if a `#` is followed by a supported tag in a string, it will still color the rest of the line.
To prevent this, separate the 
```py
# From:
"#*"
# To:
"#" "*"
```

# Argument
# Error
## InternalError
Any error that is resulted from a error inside the program