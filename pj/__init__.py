JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTPAREN = '['
JSON_RIGHTPAREN = ']'
JSON_LEFTBRACKET = '{'
JSON_RIGHTBRACKET = '}'
JSON_QUOTE = '"'

FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')


def parse_string(string):
    json_string = ''

    for c in string:
        if c == JSON_QUOTE:
            return json_string, string[len(json_string)+1:]
        else:
            json_string += c

    raise Exception('Expected end-of-string quote')


def parse_array(string):
    json_array = []

    c = string[0]
    if c == JSON_RIGHTPAREN:
        return json_array, string[1:]

    while True:
        json, string = parse(string)
        json_array.append(json)

        c = string[0]
        if c == JSON_RIGHTPAREN:
            return json_array, string[1:]
        elif c != JSON_COMMA:
            raise Exception('Expected comma after object in array')
        else:
            string = string[1:]


def parse_object(string):
    json_object = {}

    c = string[0]
    if c == JSON_RIGHTBRACKET:
        return json_object, string[1:]

    while True:
        if string[0] != JSON_QUOTE:
            raise Exception('Expected string key, got: {}'.format(c))

        json_key, string = parse_string(string[1:])

        if string[0] != JSON_COLON:
            raise Exception('Expected colon after key in object, got: {}'.format(c))

        json_value, string = parse(string[1:])

        json_object[json_key] = json_value

        c = string[0]
        if c == JSON_RIGHTBRACKET:
            return json_object, string[1:]
        elif c != JSON_COMMA:
            raise Exception('Expected comma after pair in object, got: {}'.format(c))

        string = string[1:]
        


def parse_number(string):
    json_number = ''

    number_characters = [str(d) for d in range(0, 10)] + ['-', 'e', '.']

    for c in string:
        if c in number_characters:
            json_number += c
        else:
            break

    rest = string[len(json_number):]

    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest


def parse(string, is_root=False):
    string_len = len(string)

    c = string[0]
    if is_root and c != JSON_LEFTBRACKET:
        raise Exception('Root must be an object')

    if c == JSON_QUOTE:
        return parse_string(string[1:])
    elif c == JSON_LEFTPAREN:
        return parse_array(string[1:])
    elif c == JSON_LEFTBRACKET:
        return parse_object(string[1:])
    elif string_len >= TRUE_LEN and \
         string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and \
         string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]
    elif string_len >= NULL_LEN and \
         string[:NULL_LEN] == 'null':
        return None, string[NULL_LEN]
    else:
        return parse_number(string)


def from_string(string):
    return parse(string, is_root=True)[0]


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
