def printf(*args, **kwargs):
    newline = kwargs.get('newline', True)
    if args:
        if not newline:
            for i in args:
                print i,
        else:
            for i in args[:-1]:
                print i,
            print args[-1]
    else:
        if newline:
            print '',
