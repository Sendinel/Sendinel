import re

def authenticate(number):
    try:
        number = format_number(number)
        return True
    except ValueError:
        return False


def format_number(number):
    regex = re.compile('(\/|\+|-| )')
    new_number = regex.sub('', number)
    try:
        if is_number(new_number):
            return new_number
        else:
            raise NoNumberError
    except ValueError:
        pass
        raise ValueError
        
        
def is_number(s):
    for f in [int, ]:
        return f(s)
    