import sys

if sys.version_info.major == 2:
    from .py2 import printf, pickle
else:
    from .py3 import printf, pickle