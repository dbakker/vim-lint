import ex
import re
import data


variants = {}
types = {}


for line in data.lines('options.txt'):
    aliases, type = re.match('(\S+)\s(\S+)', line).groups()
    aliases = aliases.split(':')
    base = aliases[0]
    for alias in aliases:
        variants[alias] = base
    types[base] = type


def parse(optionstr):
    options = []
    option = ''
    skipnext = False
    quoted = None
    for ch in list(optionstr):
        if skipnext:
            option += ch
            skipnext = False
        elif ch == '\\':
            option += ch
            skipnext = True
        elif ch in list('\'"'):
            if quoted:
                if ch == quoted:
                    quoted = None
            else:
                quoted = ch
            option += ch
        elif ch in [' ', "\t"] and not quoted:
            if option:
                options += [option]
            option = ''
        else:
            option += ch

    if option:
        options += [option]

    return options


def check_cmd(cmd):
    type = ex.linecmd(cmd.plain)
    if type not in ['set', 'setlocal', 'setglobal']:
        return

    sp = re.match('\s*:*set\S*\s+(.+$)', cmd.plain)
    if not sp:
        return ex.LintMessage('Missing options list')

    for option in parse(sp.group(1)):
        msg = check_option(option)
        if msg:
            if msg.col is None:
                msg.col = cmd.plain.index(option) + 1
            return msg


def check_option(option):
    option = option.strip()

    if option[-1] in ['&', '<', '?'] \
            or option.endswith('&vi') or option.endswith('&vim'):
        return

    if option in ['all', 'termcap']:
        return

    if '=' in option:
        key, value = re.split('[+-^]?[=:]', option, maxsplit=1)
        key, value = key.strip(), value.strip()

        if key not in variants:
            return ex.LintMessage('Unknown option "%s"' % key)
        key = variants[key]

        if types[key] == "boolean":
            return ex.LintMessage('Option "%s" is a boolean (use "set %s" or "set no%s" instead)' % (key, key, key))

        if types[key] == "number" and not re.match('-?\d+$', value):
            return ex.LintMessage('Option "%s" can only be set to an integer', key)

    else:
        option = re.sub('^(no|inv)', '', option, re.IGNORECASE)
        option = re.sub('!$', '', option)

        if option not in variants:
            return ex.LintMessage('Unknown option "%s"' % option)
        option = variants[option]

        if types[option] != "boolean":
            return ex.LintMessage('Option "%s" can not be used as a boolean' % option)
