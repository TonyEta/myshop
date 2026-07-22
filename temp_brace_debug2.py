from pathlib import Path
text = Path('static/js/main.js').read_text(encoding='utf-8')
stack = []
pairs = {'(': ')', '[': ']', '{': '}'}
line = 1
col = 0
for i, ch in enumerate(text):
    if ch == '\n':
        line += 1
        col = 0
        continue
    col += 1
    if ch in pairs:
        stack.append((ch, line, col))
    elif ch in pairs.values():
        if not stack:
            print('unmatched closing', ch, 'at', line, col)
            break
        opening, ol, oc = stack.pop()
        if pairs[opening] != ch:
            print('mismatch', opening, 'at', ol, oc, 'with', ch, 'at', line, col)
            break
else:
    if stack:
        opening, ol, oc = stack[-1]
        print('unmatched opening', opening, 'at', ol, oc)
    else:
        print('balanced')
