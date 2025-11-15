__default__ = None

def stringfetch(text, throws_errors=True, return__default__if_empty=True):
    def lexing(text):
        err = False
        def error(msg):
            nonlocal err
            nonlocal throws_errors
            if (throws_errors): raise SyntaxError(f"ERROR! {msg}")
            else:               print(f"\033[0;31mERROR! {msg}\033[0m")
            err = True
            return [] # Since this is lexing and these are tokens, return no tokens

        tokens   = []
        special  = "',[]{}: "
    
        doing_string = False
        doing_escape = False
        token        = ""
    
        escape_sequences = {
            '"' : '"',
            '\'': '\'',
            '\\': '\\',
            'b' : '\b',
            'f' : '\f',
            'n' : '\n',
            'r' : '\r',
            't' : '\t' 
        }
        sequences = ["\n", "\t", "\b", "\f", "\r"]

        def flush():
            nonlocal token
            nonlocal tokens
            if (token == ""): return
            tokens.append(token)
            token = ""
        def flushchar(char):
            nonlocal tokens
            if (char == ""): return
            tokens.append(char)
        
        for char in text:
            if   (doing_escape):
                if (char in escape_sequences):
                    token += escape_sequences[char]
                    doing_escape = False
                else: return error(f"Invalid escape sequence. <\\{char}>")
            elif (doing_string):
                if (char == '\\'):
                    doing_escape = True
                elif (char == '"'):
                    token += char
                    flush()
                    doing_string = False
                else: token += char
            elif (not doing_string and char == '"'):
                flush()
                token += char
                doing_string = True
            elif (char in special):
                flush()
                if (char != ' '): flushchar(char)
            elif (char in sequences): continue
            else: token += char
        flush()

        return tokens
    def parsing(tokens):
        nonlocal return__default__if_empty

        if (len(tokens) == 0):
            if (return__default__if_empty):  return __default__
            else:                            return None
                
        err = False
        def error(msg):
            nonlocal err
            nonlocal throws_errors
            if (throws_errors): raise SyntaxError(f"ERROR! {msg}")
            else:               print(f"\033[0;31mERROR! {msg}\033[0m")
            err = True
            return __default__
            
        final    = None
        on_index = 0
        
        def is_legal_string(s):
            return s[0] + s[-1] == '""'
        def is_string(s):
            return s[0] == '"'
        def is_int(n):
            for char in n:
                if (not char in "0123456789"):
                    return False
            return True
        def is_flt(f):
            num_of_dots = 0
            for char in f:
                if (char == '.'): 
                    num_of_dots += 1
                    continue
                if (not char in "0123456789"):
                    return False
            if (f[-1] == '.'):    return False
            if (num_of_dots > 1): return False
            return True
        
        layer = 0
        def interpret_array():
            nonlocal on_index
            nonlocal tokens
            nonlocal err
            nonlocal layer
            
            layer += 1

            personal_i  = 0
            local_final = []
            current     = tokens[on_index]
            
            def add(val):
                nonlocal local_final
                local_final.append(val)
            
            def upd():
                nonlocal on_index
                nonlocal personal_i
                on_index   += 1
                personal_i += 1
            
            while (current != ']'):
                if (err): return __default__
                upd()
                if (on_index == len(tokens)):
                    return error("Array has no end!")
                current = tokens[on_index]
                #print(current, layer, "array")

                if (personal_i % 2 == 0):
                    if (current == ']'):
                        #print("end of object")
                        layer -= 1
                        break

                    if (current != ','): 
                        return error(f"The Array is missing a <,>! <{current}>")
                    else: 
                        try:
                            if (tokens[on_index + 1] != '}'): continue
                            else: return error("Theres a trailing comma! <[..." + f"{tokens[on_index - 1]}, (Nothing after)" + "]>")
                        except IndexError:
                            return error("Theres a trailing comma and there is no end! <[..." + f"{tokens[on_index - 1]}(comma goes here){current}" + "]>")

                if   (current == '['):
                    add(interpret_array())
                elif (current == '{'):
                    add(interpret_map())
                elif (is_string(current)):
                    if (is_legal_string(current)):
                        add(current[1:(len(current)-1)])
                    else:
                        return error(f"Invalid string! <{current}>")
                elif (is_int(current)):
                    add(int(current))
                elif (is_flt(current)):
                    add(float(current))
                elif (current == "true" or current == "false"):
                    add(current == "true")
                elif (current == "null"):
                    add(None)
                else:
                    if (current == ']'):
                        #print("end of Array")
                        layer -= 1
                        break

                    return error(f"Unrecognised value! <{repr(current)}>")
                    
            return local_final
        def interpret_map():
            nonlocal on_index
            nonlocal tokens
            nonlocal err
            nonlocal layer
            
            layer += 1

            personal_i  = 0
            on_what     = 0
            local_final = {}
            current     = tokens[on_index]
            key         = ""
                
            def add(val):
                nonlocal local_final
                nonlocal key
                local_final.update({key: val})
                key = ""
            
            def upd():
                nonlocal on_index
                nonlocal personal_i
                nonlocal on_what
                on_index   += 1
                personal_i += 1     
                on_what    += 1
            
            while (current != '}'):
                if (err): return __default__
                upd()
                if (on_index == len(tokens)):
                    return error("Object has no end!")
                current = tokens[on_index]
                #print(current, layer, "object")
                if  on_what == 4:
                    if (current == '}'):
                        #print("end of object")
                        layer -= 1
                        break

                    if (current != ','): 
                        return error(f"The Object is missing a <,>! <{current}>")
                    else: 
                        try:
                            if (tokens[on_index + 1] != '}'): 
                                on_what = 0 # NOTE: upd() sets this back to 1 for the next iteration
                                continue
                            else: return error("Theres a trailing comma! <{..." + f"{tokens[on_index - 1]}, (Nothing after)" + "}>")
                        except IndexError:
                            return error("Theres a trailing comma and there is no end! <{..." + f"{tokens[on_index - 1]}(comma goes here){current}" + "}>")
                elif (on_what == 3):
                    if   (current == '['):
                        add(interpret_array())
                    elif (current == '{'):
                        add(interpret_map())
                    elif (is_string(current)):
                        if (is_legal_string(current)):
                            add(current[1:(len(current)-1)])
                        else:
                            return error(f"Invalid string! [{current}]")
                    elif (is_int(current)):
                        add(int(current))
                    elif (is_flt(current)):
                        add(float(current))
                    elif (current == "true" or current == "false"):
                        add(current == "true")
                    elif (current == "null"):
                        add(None)
                    elif (current == '}'):
                        return error(f"Object ends with an empty key! <{current}>")
                    else:
                        return error(f"Unrecognised value! <{repr(current)}>")
                elif (on_what == 2):
                    if (current != ':'):
                        return error("Theres a missing colon! <{..." + f"{tokens[on_index - 1]}(colon <:> goes here){current}" + "}>")
                elif (on_what == 1):
                    if (not is_legal_string(current)):
                        return error("Key must be a valid string!")
                    else: key = current[1:(len(current) - 1)]
                        
                if current == '}':
                    #print("end of object")
                    layer -= 1
                    break

            return local_final
        
        if   (tokens[0] == '['):
            final = interpret_array()
        elif (tokens[0] == '{'):
            final = interpret_map()
        else: return error("This JSON does not start with an array/object!")
                
        try:
            if (err): return __default__
            val = tokens[on_index + 1]
            return error(f"This JSON has extra stuff after the array/object! <{val}>")
        except IndexError: return final
    
    return parsing(lexing(text))
def fetch(file_location, throws_errors=True, return__default__if_empty=True):
    def error(msg, err_type):
        nonlocal throws_errors
        if (throws_errors): raise err_type(f"ERROR! {msg}")
        else:               print(f"\033[0;31mERROR! {msg}\033[0m")
        return __default__
    
    if (not file_location.lower().endswith(".json")):
        return error("File must have the extension [.json]!", ValueError)

    try:
        from pathlib import Path
        import inspect

        file_path = Path(file_location)
        base_path = Path(inspect.stack()[1].filename).parent # Get the caller scripts location

        if (not file_path.is_absolute()):
            file_path = (base_path / file_path).resolve()

        try:
            with file_path.open('r', encoding="utf-8") as f:
                return stringfetch(f.read(), throws_errors, return__default__if_empty)
        except FileNotFoundError:
            return error(f"Destination [{file_location}] does not exist!", FileNotFoundError)
    except (ModuleNotFoundError, ImportError):
        try:
            with open(file_location, 'r', encoding="utf-8") as f:
                return stringfetch(f.read(), throws_errors, return__default__if_empty)
        except FileNotFoundError:
            return error(f"Destination [{file_location}] does not exist!", FileNotFoundError)
def load(file_location, return_raw=False, throws_errors=True):
    def error(msg, err_type):
        nonlocal throws_errors
        if (throws_errors): raise err_type(f"ERROR! {msg}")
        else:               print(f"\033[0;31mERROR! {msg}\033[0m")
        return __default__
    
    if (not file_location.lower().endswith(".json")):
        return error("File must have the extension [.json]!", ValueError)

    try:
        from pathlib import Path
        import inspect

        file_path = Path(file_location)
        base_path = Path(inspect.stack()[1].filename).parent # Get the caller scripts location

        if (not file_path.is_absolute()):
            file_path = (base_path / file_path).resolve()

        try:
            with file_path.open('r', encoding="utf-8") as f:
                if (not return_raw):
                    return f.read()
                
                final = ""
                for char in f.read():
                    if (not char in ['\n', '\t', '\b', '\f', '\r', ' ']): final += char

                return final
        except FileNotFoundError:
            return error(f"Destination [{file_location}] does not exist!", FileNotFoundError)
    except (ModuleNotFoundError, ImportError):
        try:
            with open(file_location, 'r', encoding="utf-8") as f:
                if (not return_raw):
                    return f.read()
                
                final = ""
                for char in f.read():
                    if (not char in ['\n', '\t', '\b', '\f', '\r', ' ']): final += char

                return final
        except FileNotFoundError:
            return error(f"Destination [{file_location}] does not exist!", FileNotFoundError)
def tojson(object, throws_errors=True, space_count=1, indent=-1):
    def error(msg, err_type, return_val=None):
        nonlocal throws_errors
        if (throws_errors): raise err_type(f"ERROR! {msg}")
        else:       print(f"\033[0;31mERROR! {msg}\033[0m")

        if return_val != None: return return_val

        try:
            x = tojson(__default__, True)
            return x
        except Exception as e:
            return ''

    final = ""
    layer = -1

    if space_count < 0:
        if (throws_errors): return error(f"<indent> must be >= -1 <indent={space_count}>! Throwing an error...", ValueError)
        else:               space_count = error(f"<indent> must be >= -1 <indent={space_count}>! Reverting to -1...", ValueError, 1)

    if indent < -1:
        if (throws_errors): return error(f"<indent> must be >= -1 <indent={space_count}>! Throwing an error...", ValueError)
        else:               indent = error(f"<indent> must be >= -1 <indent={space_count}>! Reverting to -1...", ValueError, -1)

    escape_sequences = {
        '\b':'b',
        '\f':'f',
        '\n':'n',
        '\r':'r',
        '\t':'t',
        '\\':'\\',
        '\"':'"',
    }

    def process_string(string):
        new_string = ""

        for char in string:
            if    char in escape_sequences:
                new_string += f'\\{escape_sequences[char]}'
            else: new_string += char

        return ('"' + new_string + '"')
    def process_array(array):
        nonlocal layer
        nonlocal indent
        nonlocal space_count
        local_final = ""

        layer += 1

        def add(val):
            nonlocal local_final
            local_final += val

        is_indent = (indent > -1)

        for item in array:
            if is_indent: add((" " * indent) * (layer + 1))
            i = type(item)
            if   i == list:
                add(process_array(item))
            elif i == dict:
                add(process_map(item))
            elif i == str:
                add(process_string(item))
            elif i == int or i == float:
                add(str(item))
            elif i == bool:
                if item == True:
                    add("true")
                else:
                    add("false")
            elif item == None:
                add("null")
            if is_indent:  add("," + "\n")
            else:          add("," + (" " * space_count))

        if is_indent:  local_final = local_final[0:(len(local_final) - 2)] # Remove the <,\n> at the end
        else:          local_final = local_final[0:(len(local_final) - (space_count + 1))] # Remove the last <,>

        layer -= 1

        if is_indent:
            return "[\n" + local_final + "\n" + ((" " * indent) * (layer + 1)) + "]"
        return f"[{local_final}]"
    def process_map(map):
        nonlocal layer
        nonlocal indent
        nonlocal space_count
        local_final = ""

        layer += 1

        def add(val):
            nonlocal local_final
            local_final += val

        is_indent = (indent > -1)
        
        for key in map:
            if is_indent: add((" " * indent) * (layer + 1))
            item = map[key]
            if type(key) != str: 
                return error("Keys in dictionaries can only be strings! (JSON rule)")
            
            add(process_string(key) + ": ")

            i = type(item)
            if   i == list:
                add(process_array(item))
            elif i == dict:
                add(process_map(item))
            elif i == str:
                add(process_string(item))
            elif i == int or i == float:
                add(str(item))
            elif i == bool:
                if item == True:  add("true")
                else:            add("false")
            elif item == None:
                add("null") # Has to be null now
            else:
                return error("Data " + str(i) + " is not a valid JSON! Please make sure your Python list/dict has valid JSON data. \n<" + str(item) + ">", ValueError)
            if is_indent:  add("," + "\n")
            else:          add("," + (" " * space_count))

        if is_indent:  local_final = local_final[0:(len(local_final) - 2)] # Remove the <,\n> at the end
        else:          local_final = local_final[0:(len(local_final) - (space_count + 1))] # Remove the last <,>

        layer -= 1

        # FINISH
        if is_indent:
            return "{\n" + local_final + "\n" + ((" " * indent) * (layer + 1)) + "}"
        return "{" + local_final + "}"

    if   type(object) == list:
        final = process_array(object)
    elif type(object) == dict:
        final = process_map(object)
    else: return error("<tojson(object)> function only accepts arrays and dictionaries/objects! <type fed: " + str(type(object)) + ">", ValueError)

    return final
def save(object, file_location, overwrite=False, space_count=1, indent=-1, throws_errors=True, dont_save_if_malformed_JSON=True):
    def error(msg, err_type):
        nonlocal throws_errors
        if (throws_errors): raise err_type(f"ERROR! {msg}")
        else:               print(f"\033[0;31mERROR! {msg}\033[0m")
    
    if (not file_location.lower().endswith(".json")):
        return error("File must have the extension [.json]!", ValueError)
    
    content = object
    err     = False

    try: # Check if its invalid or malformed
        if   (type(object) == str):                            tojson(stringfetch(object, True), True, space_count, indent)
        elif (type(object) == list or type(object) == dict):   content = tojson(object, True, space_count, indent)
        else:
            err = True
            return error(f"\033[0;31mInvalid data type while trying to save! <{type(object)}>\033[0m", ValueError) # No matter what, it WILL NOT save if its not an array or map
    except Exception as e:
        if (err): return __default__
        if (dont_save_if_malformed_JSON):   
            return error("An error has been occurred while saving! <" + str(e) + ">\nAborting save...",                              ValueError)
        else:                             
            print("\033[0;31mAn error has been occurred while saving! <" + str(e) + ">\nWill continue saving as assigned...\033[0m", ValueError)

    def s(c, f): # save
        f.write(c)
        f.close()

    try:
        from pathlib import Path
        import inspect

        file_path = Path(file_location)
        base_path = Path(inspect.stack()[1].filename).parent # Get the caller scripts location

        if (not file_path.is_absolute()):   
            file_path = (base_path / file_path).resolve()

        if (not overwrite and file_path.exists()): 
            return error(f"Overwrite is not enabled! Please change 'Parameter 3' to be True if you want to overwrite files.", Exception)

        try:
            with file_path.open('x', encoding="utf-8") as f:
                s(content, f)
        except FileExistsError:
            with file_path.open('w', encoding="utf-8") as f:
                s(content, f)
    except (ModuleNotFoundError, ImportError):
        import os

        if (not overwrite and os.path.exists(file_location)): 
            return error(f"Overwrite is not enabled! Please change 'Parameter 3' to be True if you want to overwrite files.", Exception)

        try:
            with open(file_location, 'x', encoding="utf-8") as f:
                s(content, f)
        except FileExistsError:
            with open(file_location, 'w', encoding="utf-8") as f:
                s(content, f)




# EXTRA
def ver(return_type=0):
    _VER     = "Ver1.1.0"
    _MODEL   = "Python"
    _LICENSE = "MIT"

    r = [
        f"{_VER[3:6]}-{_MODEL} {_LICENSE} License",
        _VER[0:6],
        _VER,
        float(_VER[3:6]),
        _MODEL,
        f"{_VER[0:6]}-{_MODEL}",
        _LICENSE
    ]

    if return_type in range(7):              return r[return_type]
    else: raise ValueError("ERROR! You can only put numbers 0-6.")