import pickle

def printf(*args, **kwargs):
    newline = kwargs.get('newline', True)
    if newline:
        end = '\n'
    else:
        end = ''
    if args:
        print(*args, end=end)
    else:
        if newline:
            print()


def str2unicode(value):
    """convert a str to unicode"""
    return value