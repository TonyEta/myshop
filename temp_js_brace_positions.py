from pathlib import Path
import re
text = Path('static/js/main.js').read_text(encoding='utf-8')
# trim comments and strings roughly
pattern = re.compile(r'//.*?$|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^'\\])*\'|`(?:\\.|[^`\\])*`', re.S | re.M)
mask = []
for m in pattern.finditer(text):
    mask.append((m.start(), m.end()))
output = []
for i,ch in enumerate(text):
    if any(start <= i < end for start,end in mask):
        continue
    if ch in '()[]{}':
        output.append((ch, text.count('\n', 0, i)+1, i - text.rfind('\n', 0, i)))
for item in output[:200]:
    print(item)
print('total', len(output))
