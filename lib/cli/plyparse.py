#
# This file is part of python-cli. python-cli is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# python-cli is copyright (c) 2011 by the python-cli authors. See the
# file "AUTHORS" for a complete overview.

import inspect
import logging

from ply import lex, yacc


class PLYParser(object):
    """Wrapper object for PLY lexer/parser."""

    def _table_name(self, suffix, relative=False):
        """Return the module name for PLY's parsetab file."""
        mname = inspect.getmodule(self.__class__).__name__ + '_' + suffix
        if relative:
            mname = mname.split('.')[-1]
        return mname

    def _write_tables(self):
        """Write parser table (for distribution purposes)."""
        tabname = self._table_name('lex', relative=True)
        lex.lex(object=self, lextab=tabname, optimize=True, debug=False)
        tabname = self._table_name('tab', relative=True)
        yacc.yacc(module=self, tabmodule=tabname, optimize=True, debug=False)

    def parse(self, input, fname=None, debug=False):
        optimize = not debug
        tabname = self._table_name('lex')
        lexer = lex.lex(object=self, lextab=tabname,
                        optimize=optimize, debug=debug)
        if hasattr(input, 'read'):
            input = input.read()
        lexer.input(input)
        tabname = self._table_name('tab')
        parser = yacc.yacc(module=self, tabmodule=tabname,
                           optimize=optimize, debug=debug)
        if debug:
            logger = logging.getLogger()
        else:
            logger = yacc.NullLogger()
        parsed = parser.parse(lexer=lexer, tracking=True, debug=logger)
        return parsed
