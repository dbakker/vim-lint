import re
import ex


map_modifiers = frozenset(['<buffer>', '<silent>', '<special>', '<unique>', '<expr>', '<script>'])


def check(cmd):
    type = ex.linecmd(cmd.plain)
    if not type or 'map' not in type or 'unmap' in type:
        return

    sp = re.split('\s+', cmd.plain.lstrip("\t :"), maxsplit=1)
    if len(sp) == 1:
        return ex.LintMessage('Missing {lhs}')

    typestr, rest = sp

    modifiers = set()
    while True:
        if rest.isspace():
            return ex.LintMessage('Missing {lhs}')

        sp = re.split('\s+', rest, maxsplit=1)
        if len(sp) == 1:
            return ex.LintMessage("Missing {rhs}")
        val, rest = sp

        if val.lower() in map_modifiers:
            modifiers.add(val.lower())

        elif re.match('(<\w+>)+', val):
            all_match = True
            for m in re.findall('<\w+>', val.lower()):
                if m not in map_modifiers:
                    all_match = False
                    break
                modifiers.add(m)

            if not all_match:
                break

        else:
            break

    lhs = val
    rhs = rest

    if rhs.isspace():
        return ex.LintMessage("Missing {rhs}")

    if type in ['vnoremap', 'vmap'] and re.match('([^<^]|<leader>|<space>)', lhs, re.IGNORECASE):
        return ex.LintMessage("Consider using xnoremap or xmap for visual mappings", warning=True)

    if type in ['nnoremap', 'nmap', 'noremap', 'map'] \
            and '<buffer>' not in modifiers \
            and lhs.lower() in ['<c-i>', '<tab>']:
        return ex.LintMessage("It's generally better not to remap <Tab> or <C-i>", warning=True)

    if 'remap' in type and re.match('<plug>', rhs, re.IGNORECASE):
        return ex.LintMessage("Use a normal 'map' command to make use of <Plug>")

    # if re.match(':call\s', rhs, re.IGNORECASE):
    #     return ex.LintMessage("Consider using ':<C-U>call' instead to prevent range errors", warning=True, col=cmd.plain.index(':') + 1)

    if re.match('.*\s+$', rhs):
        return ex.LintMessage("Use <space> instead of trailing spaces in mappings", warning=True, col=len(cmd.plain))
