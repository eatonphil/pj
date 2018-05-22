from .constants import *

JSON_QUOTE = '"'
JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
               JSON_LEFTBRACE, JSON_RIGHTBRACE]

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
    er = 'Invalid Number'
    # Flags to take care of number symbols
    exp_done = 0
    fp_done = 0
    sign_done = 0
    dgt_done = 0
    
    for c in string:
        if c in number_characters:
            if c == 'e':
                if not dgt_done:
                    raise Exception(er)
                elif exp_done:
                    raise Exception(er)
                
                exp_done = 1
                fp_done = 1 # Exponential must be integral
                sign_done = 0 # Exponential has its own sign so reset
                dgt_done = 0
            
            elif c == '.':
                if not dgt_done:
                    raise Exception(er)
                if fp_done:
                    raise Exception(er)
                
                fp_done = 1
            
            elif c == '-':
                if sign_done:
                    raise Exception(er)
                
                sign_done = 1
            
            elif not dgt_done: # A digit encountered 
                sign_done = 1 # A positive number
                dgt_done = 1
              
            json_number += c
        
        else:
            break

    rest = string[len(json_number):]

    if not len(json_number):
        return None, string

    if not dgt_done:
        raise Exception(er)
    
    if fp_done:
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
