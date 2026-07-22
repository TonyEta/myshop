from pathlib import Path
import re
text = Path('static/js/main.js').read_text(encoding='utf-8')
output = []
state = 'normal'
quote = ''
escape = False
comment = False
line = 1
col = 0
def push_line(ch):
    global line, col
    if ch == '\n':
        line += 1
        col = 0
    else:
        col += 1
    return line, col
for ch in text:
    if state == 'normal':
        if ch == '\\':
            state = 'escape'
            push_line(ch)
            continue
        if ch == '"' or ch == "'":
            quote = ch
            state = 'string'
            push_line(ch)
            continue
        if ch == '`':
            state = 'template'
            push_line(ch)
            continue
        if ch == '/':
            # possible comment start
            next_char = ''
            # can't peek easily without index, so skip
            pass
    if state == 'escape':
        state = 'normal'
        push_line(ch)
        continue
    if state == 'string':
        if ch == '\\':
            state = 'escape'
            push_line(ch)
            continue
        if ch == quote:
            state = 'normal'
            quote = ''
            push_line(ch)
            continue
        push_line(ch)
        continue
    if state == 'template':
        if ch == '\\':
            state = 'escape'
            push_line(ch)
            continue
        if ch == '`':
            state = 'normal'
            push_line(ch)
            continue
        push_line(ch)
        continue
    push_line(ch)

# fallback: use a simpler method to find braces with no comments/strings removed
print('done')
