import cPickle as pickle

def printf(*args, **kwargs):
    end = kwargs.get('end', '\n')
    newline = (end == "\n")
    if args:
        if not newline:
            for i in args:
                print i,
        else:
            for i in args[:-1]:
                print i,
            print args[-1]
        print end
    else:
        print end


def str2unicode(value):
    """convert a str to unicode"""
    return value.decode('utf8')

