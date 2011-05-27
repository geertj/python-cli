#
# This file is part of python-cli. python-cli is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# python-cli is copyright (c) 2011 by the python-cli authors. See the
# file "AUTHORS" for a complete overview.

import os
import os.path


def get_home_dir():
    """Return the user's home directory."""
    home = os.environ.get('HOME')
    if home is not None:
        return home
    try:
        pw = pwd.getpwuid(os.getuid())
    except Keyerror:
        return None
    return pw.pw_dir

def local_settings_file(name):
    """"Return the local settings file for `name'."""
    home = get_home_dir()
    if home is None:
        return
    name = name.replace('-', '').replace('_', '')
    fname = os.path.join(home, '.%src' % name)
    return fname
