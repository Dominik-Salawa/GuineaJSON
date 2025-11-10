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
            return []

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
            if token == "": return
            tokens.append(token)
            token = ""
        def flushchar(char):
            nonlocal tokens
            if char == "": return
            tokens.append(char)
        
        for char in text:
            if   (doing_escape):
                if char in escape_sequences:
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
                if char != " ": flushchar(char)
            elif (char in sequences): continue
            else: token += char
        flush()

        return tokens
    def parsing(tokens):
        nonlocal return__default__if_empty

        if len(tokens) == 0:
            if return__default__if_empty: return __default__
            else:                         return None
                
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
                if not char in "0123456789":
                    return False
            return True
        def is_flt(f):
            num_of_dots = 0
            for char in f:
                if char == '.': 
                    num_of_dots += 1
                    continue
                if not char in "0123456789":
                    return False
            if f[-1] == '.':    return False
            if num_of_dots > 1: return False
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
            
            while current != ']':
                if err: return __default__
                upd()
                if on_index == len(tokens):
                    return error("Array has no end!")
                current = tokens[on_index]
                #print(current, layer, "array")

                if personal_i % 2 == 0:
                    if current == ']':
                        #print("end of object")
                        layer -= 1
                        break

                    if current != ",": 
                        return error(f"The Array is missing a <,>! <{current}>")
                    else: 
                        try:
                            if tokens[on_index + 1] != '}': continue
                            else: return error("Theres a trailing comma! <[..." + f"{tokens[on_index - 1]}, (Nothing after)" + "]>")
                        except IndexError:
                            return error("Theres a trailing comma and there is no end! <[..." + f"{tokens[on_index - 1]}(comma goes here){current}" + "]>")

                if   current == '[':
                    add(interpret_array())
                elif current == '{':
                    add(interpret_map())
                elif is_string(current):
                    if is_legal_string(current):
                        add(current[1:(len(current)-1)])
                    else:
                        return error(f"Invalid string! <{current}>")
                elif is_int(current):
                    add(int(current))
                elif is_flt(current):
                    add(float(current))
                elif current == "true" or current == "false":
                    add(current == "true")
                elif current == "null":
                    add(None)
                else:
                    if current == ']':
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
            
            while current != '}':
                if err: return __default__
                upd()
                if on_index == len(tokens):
                    return error("Object has no end!")
                current = tokens[on_index]
                #print(current, layer, "object")
                if  on_what == 4:
                    if current == '}':
                        #print("end of object")
                        layer -= 1
                        break

                    if current != ",": 
                        return error(f"The Object is missing a <,>! <{current}>")
                    else: 
                        try:
                            if tokens[on_index + 1] != '}': 
                                on_what = 0 # NOTE: upd() sets this back to 1 for the next iteration
                                continue
                            else: return error("Theres a trailing comma! <{..." + f"{tokens[on_index - 1]}, (Nothing after)" + "}>")
                        except IndexError:
                            return error("Theres a trailing comma and there is no end! <{..." + f"{tokens[on_index - 1]}(comma goes here){current}" + "}>")
                elif on_what == 3:
                    if   current == '[':
                        add(interpret_array())
                    elif current == '{':
                        add(interpret_map())
                    elif is_string(current):
                        if is_legal_string(current):
                            add(current[1:(len(current)-1)])
                        else:
                            return error(f"Invalid string! [{current}]")
                    elif is_int(current):
                        add(int(current))
                    elif is_flt(current):
                        add(float(current))
                    elif current == "true" or current == "false":
                        add(current == "true")
                    elif current == "null":
                        add(None)
                    elif current == "}":
                        return error(f"Object ends with an empty key! <{current}>")
                    else:
                        return error(f"Unrecognised value! <{repr(current)}>")
                elif on_what == 2:
                    if current != ':':
                        return error("Theres a missing colon! <{..." + f"{tokens[on_index - 1]}(colon <:> goes here){current}" + "}>")
                elif on_what == 1:
                    if not is_legal_string(current):
                        return error("Key must be a valid string!")
                    else: key = current[1:(len(current) - 1)]
                        
                if current == '}':
                    #print("end of object")
                    layer -= 1
                    break

            return local_final
        
        if   tokens[0] == "[":
            final = interpret_array()
        elif tokens[0] == "{":
            final = interpret_map()
        else: return error("This JSON does not start with an array/object!")
                
        try:
            if err: return __default__
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
    
    if not file_location.lower().endswith(".json"):
        return error("File must have the extension [.json]!", ValueError)
    
    try:
        from pathlib import Path    
        try:
            with Path(file_location).open("r", encoding="utf-8") as f:
                return stringfetch(f.read(), throws_errors, return__default__if_empty)
        except FileNotFoundError:
            return error(f"Destination [{file_location}] does not exist!", FileNotFoundError)
    except (ModuleNotFoundError, ImportError):
        try:
            with open(file_location, "r", encoding="utf-8") as f:
                return stringfetch(f.read(), throws_errors, return__default__if_empty)
        except FileNotFoundError:
            return error(f"Destination [{file_location}] does not exist!", FileNotFoundError)
def tojson(object, throws_errors=True, space_count=1):
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

    if space_count < 0:
        if (throws_errors): return error(f"<space_count> must be >= 0 <space_count={space_count}>!", ValueError)
        else:               space_count = error(f"<space_count> must be >= 0 <space_count={space_count}>! Reverting to 1...", ValueError, 1)

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
        nonlocal space_count
        local_final = ""

        def add(val):
            nonlocal local_final
            local_final += val

        for item in array:
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
            add("," + (" " * space_count))

        local_final = local_final[0:(len(local_final) - (space_count + 1))] # Remove the last <,>
        return f"[{local_final}]"
    def process_map(map):
        nonlocal space_count
        local_final = f""

        def add(val):
            nonlocal local_final
            local_final += val

        for key in map:
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
            else: add("null") # Has to be null now
            add("," + (" " * space_count))

        local_final = local_final[0:(len(local_final) - (space_count + 1))] # Remove the last <,>

        return "{" + local_final + "}"

    if   type(object) == list:
        final = process_array(object)
    elif type(object) == dict:
        final = process_map(object)
    else: return error("<tojson(object)> function only accepts arrays and dictionaries/objects! <type fed: " + str(type(object)) + ">", ValueError)

    return final
def save(object, file_location, overwrite=False, space_count=1, throws_errors=True, dont_save_if_malformed_JSON=True):
    def error(msg, err_type):
        nonlocal throws_errors
        if (throws_errors): raise err_type(f"ERROR! {msg}")
        else:               print(f"\033[0;31mERROR! {msg}\033[0m")
    
    if not file_location.lower().endswith(".json"):
        return error("File must have the extension [.json]!", ValueError, return_val=0)
    
    content = None
    err     = False

    try: # Check if its invalid or malformed
        if   type(object) == str:                            content = tojson(stringfetch(object, True), True, space_count)
        elif type(object) == list or type(object) == dict:   content = tojson(object, True, space_count)
        else:
            err = True
            return error(f"\033[0;31mInvalid data type while trying to save! <{type(object)}>\033[0m", ValueError) # No matter what, it WILL NOT save if its not an array or map
    except Exception as e:
        if err: return __default__
        if dont_save_if_malformed_JSON:   
            return error("An error has been occurred while saving!\nAborting save...",                              ValueError)
        else:                             
            print("\033[0;31mAn error has been occurred while saving!\nWill continue saving as assigned...\033[0m", ValueError)

    def s(c, f): # save
        f.write(c)
        f.close()

    try:
        from pathlib import Path
        try:
            with Path(file_location).resolve().open("w", encoding="utf-8") as f:
                if not overwrite: 
                    return error(f"Overwrite is not enabled! Please change 'Parameter 3' to be True if you want to overwrite files.", Exception)
                s(content, f)
        except FileNotFoundError:
            with Path(file_location).resolve().open("x", encoding="utf-8") as f:
                s(content, f)
    except (ModuleNotFoundError, ImportError):
        try:
            with open(file_location, "w", encoding="utf-8") as f:
                if not overwrite: 
                    return error(f"Overwrite is not enabled! Please change 'Parameter 3' to be True if you want to overwrite files.", Exception)
                s(content, f)
        except FileNotFoundError:
            with open(file_location, "x", encoding="utf-8") as f:
                s(content, f)




# EXTRA
def ver(Type=0):
    _VER     = "Ver1.0"
    _MODEL   = "Python"
    _LICENSE = "MIT"

    return_type = [
        f"{_VER}-{_MODEL} {_LICENSE} License",
        _VER,
        float(_VER[3:]),
        _MODEL,
        f"{_VER}-{_MODEL}",
        _LICENSE
    ]

    if (Type >= 0 and Type <= 5):         return return_type[Type]
    else: raise ValueError("ERROR! You can only put numbers 0-5.")