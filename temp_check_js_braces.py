from pathlib import Path
import re
text = Path('static/js/main.js').read_text(encoding='utf-8')
# Remove JS comments (single-line and block) for cleaner brace matching
text_no_comments = re.sub(r'//.*|/\*.*?\*/', '', text, flags=re.S)
stack = []
pairs = {'(': ')', '[': ']', '{': '}'}
line = 1
col = 0
for ch in text_no_comments:
    if ch == '\n':
        line += 1
        col = 0
        continue
    col += 1
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
else:
    if stack:
        opening, ol, oc = stack[-1]
        print('unmatched opening', opening, 'line', ol, 'col', oc)
    else:
        print('balanced')
