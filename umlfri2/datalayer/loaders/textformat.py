import re

SPACES = re.compile('\\s+')


def format_text(text):
    current_text = []
    current_line = []
    for line in text.splitlines():
        line = SPACES.sub(' ', line.strip())
        if line:
            current_line.append(line)
        elif current_line:
            current_text.append(' '.join(current_line))
            current_line = []
    return '\n'.join(current_text)
