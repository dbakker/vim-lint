import re
import data


class LintMessage(object):
    def __init__(self, msg, col=None, line=None, warning=False):
        self.msg = msg
        self.col = col
        self.line = line
        self.warning = warning


class ExCommand():
    def __init__(self, plain, lines, startline, endline):
        self.plain = plain
        self.lines = lines
        self.startline = startline
        self.endline = endline


def read_ex_commands(lines):
    endmarker = None
    chunk = []
    for i in range(0, len(lines)):
        line = lines[i]
        if endmarker:
            if endmarker in line:
                endmarker = None
                chunk = []
            continue

        embedded_lang = re.match('\s*\w+\s*<<\s*(\w+)', lines[i - 1])
        if embedded_lang:
            endmarker = embedded_lang.group(1)
            continue

        if chunk and re.match('\s*\\\\', line):
            line = re.sub('^\s*\\\\', '', line, count=1)

        if i + 1 < len(lines) and re.match('^\s*\\\\', lines[i + 1]):
            chunk += [line]
            continue
        else:
            chunk += [line]

        end = i
        start = end - (len(chunk) - 1)
        for cmd in create_ex(chunk, start + 1, end + 1):
            yield cmd

        chunk = []


quoted_ex = frozenset(['echo', 'echoerr', 'execute'])
barred_ex = frozenset(['autocmd', 'command', 'windo', 'bufdo', 'tabdo'])


def get_plain(lines):
    """
    Joins the given lines into a single string, removes all comments and
    continuation markers, and splits the string again for every `|` separated
    command.
    """

    if len(lines) == 0 or re.match('\s*:*[A-Z]', lines[0]):
        # Skip user defined commands
        return

    joined_lines = "\n".join(lines)
    line = list(joined_lines)
    cancel = False
    comment = False
    lastword = ''
    lastch = ''
    lastnonspace = ''
    quoted = None

    cmd = linecmd(joined_lines)
    mapping = cmd and 'map' in cmd and 'unmap' not in cmd
    splitbars = cmd not in barred_ex and not mapping
    firstword = ''

    for i in range(0, len(line)):
        ch = line[i]

        if ch == "\n":
            cancel = False
            comment = False
            ch = ''

        elif comment:
            ch = ' '

        elif cancel:
            cancel = False

        elif ch == '\\':
            cancel = True

        elif quoted and ch != quoted:
            pass

        elif ch == "'":
            quoted = ch if quoted is None else None

        elif ch == '"':
            last_exword = expand(lastword) if expand(lastword) else lastword

            if quoted:
                quoted = None

            elif ((lastnonspace == '' or re.match('[a-zA-Z0-9\]})\'";/]', lastnonspace))
                    and last_exword not in quoted_ex
                    and not mapping) or \
                    (expand(firstword) and expand(firstword).startswith('set') and lastch != '='):
                comment = True
                ch = ' '

            else:
                quoted = '"'

        elif ch == '|' and lastch != '|' and i < len(line) - 1 and line[i + 1] != '|':
            if splitbars:
                yield ''.join(line[0:i])
                for j in range(0, i):
                    line[j] = ' '
                ch = ' '
                firstword = ''

        if ch not in ["", " ", "\t"]:
            lastnonspace = ch
            if lastch in [" ", "\t", "|", ":", "%"]:
                if not firstword:
                    firstword = lastword
                lastword = ''
            lastword += ch

        line[i] = ch
        lastch = ch

    yield ''.join(line)


def create_ex(lines, start, end):
    for plain in get_plain(lines):
        if re.match('^\s*$', plain):
            continue

        yield ExCommand(plain, lines, start, end)


exaliases = {}


def expand(excmd):
    global exaliases
    if not exaliases:
        for line in data.lines('excommands.txt'):
            line = line[1:].rstrip()
            if '[' not in line:
                exaliases[line] = line
            else:
                current, _, end = line.partition('[')
                complete = current + end.rstrip(']')
                for ch in list(end):
                    exaliases[current] = complete
                    current += ch

    return exaliases.get(excmd.lower(), None)


def linecmd(line):
    try:
        cmd = re.match('\s*:*%?([a-z]+|!)', line).group(1)
        expanded = expand(cmd)
        return expanded if expanded else cmd.lower()
    except:
        pass

    return None


def check_exists(cmd):
    type = linecmd(cmd.plain)
    if type and expand(type) is None and re.match('[a-z]', type):
        return LintMessage("Unknown ex command '%s'" % type)


def check_semi(cmd):
    if re.match('\s*:', cmd.plain):
        return LintMessage("Prefixing ex commands with ':' is not required", warning=True)
