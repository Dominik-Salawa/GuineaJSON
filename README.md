# `GuineaJSON`
Hello There! GuineaJSON is a Python module built for handling conversion between JSON arrays/objects to Pythons lists/dictionaries.

## Features
GuineaJSON is built to be as minimal as possible for the user. Only requiring a line for fetching a JSON file, and another line for saving a JSON file.<br>

GuineaJSON gives you the ability to customise on how it handles errors (throws them or doesn't) and some safety features for overwriting.<br>

GuineaJSON will default on using pathlib for file handling, but if you do not have it installed it will default to Pythons original file I/O. So it is compatible for all Python Versions.<br>

GuineaJSON returns the `__default__` value if it stumbles upon a Malformed JSON file (if throws_errors == False, then there will be no errors).<br>

## BEFORE YOU CONTINUE!!! 
Container = list/dictionary<br>

For GuineaJSON to work, it is recommended you use valid JSON files and try to use them according to their purpose.<br>

If you do not have pathlib available, you will **need** to give an absolute address. 
<br>(Full addresses like `"C:\\stuff\\example.json"`, not just `"example.json"`)<br>

**IF YOU ENCOUNTER ANY BUGS OR HAVE ANY RECOMMENDATIONS, PLEASE LET ME KNOW :)**

--------------------------------------------------------------------------

# `Installation`
Open up the terminal/command prompt and run<br>
```
pip install guineajson
```
And now, you'll be able to import GuineaJSON to any script.<br>

--------------------------------------------------------------------------

**There are 5 functions and 1 variable GuineaJSON currently brings in Ver1.0:**

# `GuineaJSON.__default__`
`__default__` allows us to default to a value, if fetching goes wrong, you are able to change this and its `None` by default.<br>

## EXAMPLE:
```
import guineajson as G

G.__default__ = []
# Instead of `None`

x = G.fetch("example.json", False)
# If its malformed or failed, it will return `[]` now instead of `None`
```

--------------------------------------------------------------------------

# `GuineaJSON.fetch(address, throws_errors=True, return__default__if_empty=False)`
`fetch()` allows us to go and find a file, extract the JSON, and then convert it into a Python Container.
NOTE: It must be a [.json] file or else it will result in an error.

**How it works:**<br>
Parameters<br>
--------------<br>
*1* | `address`                      **(string)**  -  **REQUIRED**,        it an absolute address (harddrive ->-> final location) and has to be a valid address, with the file being a [.json].<br>
*2* | `throws_errors`                  **(bool)**  -  **DEFAULT = TRUE**,  if *True*, then it *will throw errors for you to handle*, you can turn it to *False* if you want to *Lazy Handle* (not deal with real errors).<br>
*3* | `return__default__if_empty`      **(bool)**  -  **DEFAULT = FALSE**, if *True*, then it *will return `__default__` if empty*, if its *False* then it *will return `None`*.<br>

## EXAMPLE:
```
import guineajson as G

x = G.fetch("example.json", False)
# Go get `example.json` and do not throw any errors

y = G.fetch("example.json")
# Go get `example.json` and do throw errors (we never stated throws_errors) 
```

--------------------------------------------------------------------------

# `GuineaJSON.stringfetch(string, throws_errors=True)`
`stringfetch()` allows us to transform a JSON string, into a Python container.

**How it works:**<br>
Parameters<br>
--------------<br>
*1* | `string`                       **(string)**  -  **REQUIRED**,       a *JSON String* to *convert into* a *Python container*<br>
*2* | `throws_errors`                  **(bool)**  -  **DEFAULT = TRUE**, same as before, if *True*, then it will *throw errors for you to handle*, *turn it to False* if you want to *Lazy Handle* (not deal with real errors).<br>
*3* | `return__default__if_empty`      **(bool)**  -  **DEFAULT = FALSE**, same as `fetch()`, if *True*, then it *will return `__default__` if empty*, if its *False* then it *will return `None`*.<br>

## EXAMPLE:
```
import guineajson as G

x = G.stringfetch('[21, null, "Hello, World!"]', False)
# Converts the string into a python container and do not throw any errors

y = G.stringfetch('[21, null, "Hello, World!"]')
# Converts the string into a python container and do throw errors (we never stated throws_errors) 
```

--------------------------------------------------------------------------

# `GuineaJSON.tojson(container, throws_errors=True, space_count=1)`
`tojson()` allows us to transform a Python container, into a JSON string.

**How it works:**<br>
Parameters<br>
--------------<br>
*1* | `container`                 **(list/dict)**  -  **REQUIRED**,        a Python container to convert into a JSON string<br>
*2* | `throws_errors`                  **(bool)**  -  **DEFAULT = TRUE**,  okay, by now you should know what 'throws_errors' is<br>
*3* | `space_count`                 **(integer)**  -  **DEFAULT = 1**,     the amount of space between <,> and the next instance, it has to be >= 0!<br>

## EXAMPLE:
```
import guineajson as G

x = G.tojson([21, None, "Hello, World!"], False)
# Converts the python container into a JSON string and does not throw any errors

y = G.tojson([21, None, "Hello, World!"])
# Converts the python container into a JSON string and does throw errors (we never stated throws_errors) 

z = G.tojson([21, None, "Hello, World!"], space_count=10)
# Converts the python container into a JSON string (with the space_count of 10) and does throw errors (we never stated throws_errors) 
```

--------------------------------------------------------------------------

# `GuineaJSON.save(container/string, address, overwrite=False, space_count=1, throws_errors=True, dont_save_if_malformed_JSON=True)`
`save()` allows us to transform either a Python container or a JSON string and save it into a JSON file.
NOTE: It must be a [.json] file or else it will result in an error.

**How it works:**<br>
Parameters<br>
--------------<br>
*1* | `container/string`   **(list/dict/string)**  -  **REQUIRED**,        a *Python list/dict* to *convert into a JSON string*<br>
*2* | `address`                      **(string)**  -  **REQUIRED**,        a *valid address* to where to *save/overwrite*<br>
*3* | `overwrite`                      **(bool)**  -  **DEFAULT = FALSE**, if *True*, then it *will overwrite* files, if *False*, it *will not overwrite* any file<br>
*4* | `space_count`                 **(integer)**  -  **DEFAULT = 1**,     same logic as `tojson()`<br>
*5* | `throws_errors`                  **(bool)**  -  **DEFAULT = TRUE**,  don't need Sherlock for this one<br>
*6* | `dont_save_if_malformed_JSON`    **(bool)**  -  **DEFAULT = TRUE**,  if you have *given* a *Malformed/Invalid JSON*, either **you save (FALSE)** or **do not save (TRUE)**<br>

## EXAMPLE:
```
import guineajson as G

G.save([1,2,3,4,5], "numbers.json", True)
# Save the array in "numbers.json" and overwrite (throws_errors and dont_save_if_malformed_JSON is automatically True)

G.save('{"name": "Dominik-Salawa", "favourite-number": 5}', "numbers.json", False, False, True)
# Also accepts JSON strings, at "numbers.json", do not overwrite, do not throw errors and do not save if its malformed string
```

--------------------------------------------------------------------------

# `GuineaJSON.ver(number=0)`
`ver()` returns a string/float giving you info of what Version/License/Model you are using.
Its by default set to 0 but you can change it.

**How it works:**<br>
Parameter<br>
--------------<br>
*1* | `Integer` **(0-5)**<br>
         |    0 - `Full versions`        **"GuineaJSON Ver1.0-Python MIT License"**<br>
         |    1 - `Version`              **"Ver1.0"**<br>
         |    2 - `Version in float`     **1.0**<br>
         |    3 - `Module Language`      **"Python"**<br>
         |    4 - `Verison + Language`   **"Ver1.0-Python"**<br>
         |    5 - `License`              **"MIT"**<br>
      All other numbers greater than or less than 0-5 will make ver() toss an error<br>

## EXAMPLE:
```
import guineajson as G
print(G.ver(2)) # Prints `1.0`
```

--------------------------------------------------------------------------

# `Arguements in Terminal`
Theres some commands you can run with `python -m guineajson` in the terminal<br>

**`python -m guineajson` by itself:**<br>
```
------------------------------------
GuineaJSON Ver1.0-Python MIT License
     | GitHub: Dominik-Salawa |
------------------------------------
```
**`--version`:**<br>
```
Ver1.0
```
**`--model`:**<br>
```
Python
```
**`--license`:**<br>
```
MIT
```
**`--version+model`:**<br>
```
Ver1.0-Python
```
**`--full-version`:**<br>
```
Ver1.0-Python MIT License
```
**NOTE:** It will *not* always be Python or Ver1.0, it will always depend on what type of GuineaJSON you have got installed.<br>

--------------------------------------------------------------------------

Thank you for taking your time to read GuineaJSON, hope it will benefit you :)