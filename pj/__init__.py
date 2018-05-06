JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTPAREN = '['
JSON_RIGHTPAREN = ']'
JSON_LEFTBRACKET = '{'
JSON_RIGHTBRACKET = '}'
JSON_QUOTE = '"'

JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTPAREN, JSON_RIGHTPAREN,
               JSON_LEFTBRACKET, JSON_RIGHTBRACKET]

FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')


def lex_string(string):
    json_string = ''

    if string[0] == JSON_QUOTE:
        string = string[1:]
    else:
        return None, string

    for c in string:
        if c == JSON_QUOTE:
            return json_string, string[len(json_string)+1:]
        else:
            json_string += c

    raise Exception('Expected end-of-string quote')


def lex_number(string):
    json_number = ''

    number_characters = [str(d) for d in range(0, 10)] + ['-', 'e', '.']

    for c in string:
        if c in number_characters:
            json_number += c
        else:
            break

    rest = string[len(json_number):]

    if not len(json_number):
        return None, string

    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest


def lex_bool(string):
    string_len = len(string)

    if string_len >= TRUE_LEN and \
         string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and \
         string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]

    return None, string


def lex_null(string):
    string_len = len(string)

    if string_len >= NULL_LEN and \
         string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN]

    return None, string


def lex(string):
    tokens = []

    while len(string):
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(None)
            continue

        c = string[0]

        if c in JSON_WHITESPACE:
            # Ignore whitespace
            string = string[1:]
        elif c in JSON_SYNTAX:
            tokens.append(c)
            string = string[1:]
        else:
            raise Exception('Unexpected character: {}'.format(c))

    return tokens


def parse_array(tokens):
    json_array = []

    t = tokens[0]
    if t == JSON_RIGHTPAREN:
        return json_array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        t = tokens[0]
        if t == JSON_RIGHTPAREN:
            return json_array, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after object in array')
        else:
            tokens = tokens[1:]


def parse_object(tokens):
    json_object = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception('Expected string key, got: {}'.format(json_key))

        if tokens[0] != JSON_COLON:
            raise Exception('Expected colon after key in object, got: {}'.format(t))

        json_value, tokens = parse(tokens[1:])

        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after pair in object, got: {}'.format(t))

        tokens = tokens[1:]
        

def parse(tokens, is_root=False):
    t = tokens[0]

    if is_root and t != JSON_LEFTBRACKET:
        raise Exception('Root must be an object')

    if t == JSON_LEFTPAREN:
        return parse_array(tokens[1:])
    elif t == JSON_LEFTBRACKET:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]


def from_string(string):
    tokens = lex(string)
    return parse(tokens, is_root=True)[0]


def to_string(json):
    json_type = type(json)
    if json_type is dict:
        string = '{'
        dict_len = len(json)

        for i, (key, val) in enumerate(json.items()):
            string += '"{}": {}'.format(key, to_string(val))

            if i < dict_len - 1:
                string += ', '
            else:
                string += '}'

        return string
    elif json_type is list:
        string = '['
        list_len = len(json)

        for i, val in enumerate(json):
            string += to_string(val)

            if i < list_len - 1:
                string += ', '
            else:
                string += ']'

        return string
    elif json_type is str:
        return '"{}"'.format(json)
    elif json_type is bool:
        return 'true' if json else 'false'
    elif json_type is None:
        return 'null'

    return str(json)
