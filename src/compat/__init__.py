import sys

if sys.version_info.major == 2:
    from .py2 import printf, pickle, str2unicode
else:
    from .py3 import printf, pickle, str2unicode