# Vim Lint
# Author:       Daan Bakker
# HomePage:     http://github.com/dbakker/vim-lint
# Version:      1.0

import re
import ex
import excontrol
import exmap
import argparse
import options
import os.path


line_checkers = [exmap.check, ex.check_exists, options.check_cmd, ex.check_semi]
file_checkers = [excontrol.check]


def lint(lines):
    lines = map(lambda x: x.rstrip("\n\r"), lines) + ['']
    result = []

    commands = list(ex.read_ex_commands(lines))

    for checker in line_checkers:
        for cmd in commands:
            messages = checker(cmd)
            if messages is not None:
                if isinstance(messages, ex.LintMessage):
                    messages = [messages]
                for message in messages:
                    if message.line is None:
                        message.line = cmd.startline

                result += messages

    for checker in file_checkers:
        messages = checker(commands)
        if messages is not None:
            if isinstance(messages, ex.LintMessage):
                messages = [messages]
            result += messages

    for message in result:
        if message.col is None:
            indent = re.match('(\s*)', lines[message.line - 1]).group(1)
            message.col = len(indent) + 1
        else:
            while message.col > len(lines[message.line - 1]) and message.line + 1 < len(lines):
                message.col -= len(lines[message.line - 1])
                message.line += 1
                continuation = re.match('(\s*\\\\)', lines[message.line - 1])
                if not continuation:
                    break
                message.col += len(continuation.group(1))

    result = sorted(result, key=lambda x: x.line)

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple linter for Vimscript')
    parser.add_argument('files', metavar='file', help='Vimscript to lint', nargs='+')
    args = parser.parse_args()

    for filename in args.files:
        if os.path.isdir(filename) or '%' in filename:
            continue

        with open(filename) as f:
            lines = f.readlines()
            res = lint(lines)
            res = map(lambda x: '%s:%s:%s: %s: %s' % (filename, x.line, x.col, 'Warning' if x.warning else 'Error', x.msg), res)
            for r in res:
                print(r)
