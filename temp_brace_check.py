from pathlib import Path
text = Path('static/js/main.js').read_text(encoding='utf-8')
state = 'normal'
quote_char = None
escape = False
line = 1
col = 0
stack = []
pairs = {'(': ')', '[': ']', '{': '}'}
for ch in text:
    if ch == '\n':
        line += 1
        col = 0
    else:
        col += 1
    if state == 'normal':
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch in ('"', "'"):
            quote_char = ch
            state = 'string'
            continue
        if ch == '`':
            state = 'template'
            continue
        if ch == '/':
            # comment start? need peek next char
            continue
        if ch in pairs:
            stack.append((ch, line, col))
        elif ch in pairs.values():
            if not stack:
                print('unmatched closing', ch, 'line', line, 'col', col)
                break
            opening, ol, oc = stack.pop()
            if pairs[opening] != ch:
                print('mismatch', opening, 'line', ol, 'col', oc, 'with', ch, 'line', line, 'col', col)
                break
    elif state == 'string':
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == quote_char:
            state = 'normal'
            quote_char = None
            continue
    elif state == 'template':
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '`':
            state = 'normal'
            continue
else:
    if stack:
        opening, ol, oc = stack[-1]
        print('unmatched opening', opening, 'line', ol, 'col', oc)
    else:
        print('balanced')
