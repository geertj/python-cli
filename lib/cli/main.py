#
# This file is part of python-cli. python-cli is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# python-cli is copyright (c) 2011 by the python-cli authors. See the
# file "AUTHORS" for a complete overview.

import sys
import textwrap
from argparse import ArgumentParser, FileType

from cli.object import create
from cli.settings import Settings
from cli.context import ExecutionContext
from cli.command import *


class TestContext(ExecutionContext):

    name = 'cli-test'
    welcome = textwrap.dedent("""\
        Welcome to cli-test. This is a test driver for the python-cli.
        Type 'exit' to exit or 'help' for help.
        """)
    goodbye = 'Goodbye!'

    def setup_commands(self):
        """Add commands."""
        self.add_command(SetCommand)
        self.add_command(SaveCommand)
        self.add_command(HelpCommand)
        self.add_command(StatusCommand)
        self.add_command(CdCommand)
        self.add_command(ClearCommand)
        self.add_command(PwdCommand)
        self.add_command(ExitCommand)


def main():
    """Test driver for python-cli."""
    parser = create(ArgumentParser)
    parser.add_argument('-f', '--file', type=FileType('r'), default=sys.stdin,
                        help='execute commands from FILE')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='enable debugging mode')
    parser.add_argument('-v', '--verbose', action='store_const',
                        dest='verbosity', default=0, const=10,
                        help='be verbose')
    parser.add_argument('command', nargs='*')
    args = parser.parse_args()

    context = create(TestContext, args.file)
    context.settings['cli:debug'] = args.debug
    context.settings['cli:verbosity'] = args.verbosity

    if args.command:
        command = ' '.join(args.command) + '\n'
        context.execute_string(command)
    else:
        context.execute_loop()

    sys.exit(context.status)
