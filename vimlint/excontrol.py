import ex

control_structures = [
    ['if', ['else', 'elseif'], 'endif'],
    ['while', ['break', 'continue'], 'endwhile'],
    ['for', ['break', 'continue'], 'endfor'],
    ['try', ['catch', 'finally'], 'endtry'],
    ['function', ['return'], 'endfunction'],

    # Support for vim-spec. Instead of `end` we use `endif` as that is the
    # proper expansion.
    ['describe', [], 'endif'],
    ['before', [], 'endif'],
    ['after', [], 'endif'],
    ['it', [], 'endif'],
]

starts = set()
checks = {}
ends = {}

for start, mids, end in control_structures:
    starts.add(start)

    for mid in mids:
        checks[mid] = checks.get(mid, []) + [start]

    ends[end] = ends.get(end, []) + [start]


def check(commands):
    messages = []
    control_stack = []

    for cmd in commands:
        type = ex.linecmd(cmd.plain)

        if type in starts:
            control_stack += [(type, cmd)]

        elif type in checks:
            nested = False
            for start, _ in control_stack:
                if start in checks[type]:
                    nested = True
            if not nested:
                messages += [ex.LintMessage('Statement not nested in the appropriate control structure', line=cmd.startline)]

        elif type in ends:
            if not control_stack:
                messages += [ex.LintMessage('There is nothing open to close', line=cmd.startline)]
            else:
                start, _ = control_stack[-1]
                if start in ends[type]:
                    control_stack.pop()
                else:
                    messages += [ex.LintMessage('Unmatched closing statement', line=cmd.startline)]

    for type, cmd in control_stack:
        messages += [ex.LintMessage('Missing closing statement', line=cmd.startline)]

    return messages
