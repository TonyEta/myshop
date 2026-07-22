from pathlib import Path
text = Path('static/js/main.js').read_text(encoding='utf-8').splitlines()
for i in range(360, min(len(text), 420)):
    print(f'{i+1:04d}: {text[i]}')
