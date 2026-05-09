def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

def get_indent(line):
    return len(line) - len(line.lstrip())

def clean_line(line):
    comment_pos = line.find('#')
    if comment_pos != -1:
        line = line[:comment_pos]
    return line.rstrip()

def tokenize(text):
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    tokens = []
    for line in lines:
        cleaned = clean_line(line)
        if cleaned.strip() == '':
            continue
        tokens.append(cleaned)
    return tokens

def parse_yaml(tokens):
    schedule = {}
    i = 0
    while i < len(tokens):
        line = tokens[i]
        indent = get_indent(line)
        if indent != 0:
            raise Exception('Неверный отступ у имени дня')
        colon = line.find(':')
        if colon == -1:
            raise Exception('Нет двоеточия в имени дня')
        day_name = line[:colon].strip()
        i += 1
        body_lines = []
        while i < len(tokens) and get_indent(tokens[i]) > 0:
            body_lines.append(tokens[i])
            i += 1
        schedule[day_name] = parse_day_body(body_lines)
    return schedule

def parse_day_body(lines):
    body = {}
    if not lines:
        return body
    line0 = lines[0]
    if get_indent(line0) < 2:
        raise Exception('Слишком маленький отступ в теле дня')
    key, value = parse_key_value(line0)
    if key != 'date':
        raise Exception('Первым полем ожидалось date')
    body['date'] = value
    lessons = []
    for idx, line in enumerate(lines[1:], start=1):
        stripped = line.lstrip()
        if stripped.startswith('lessons:'):
            _, val = parse_key_value(line)
            if val == '[]':
                lessons = []
            else:
                base_indent = get_indent(line)
                lesson_lines = []
                j = idx + 1
                while j < len(lines) and get_indent(lines[j]) > base_indent:
                    lesson_lines.append(lines[j])
                    j += 1
                lessons = parse_lessons_list(lesson_lines)
            break
    body['lessons'] = lessons
    return body

def parse_key_value(line):
    colon = line.find(':')
    key = line[:colon].strip()
    value = line[colon+1:].strip()
    return key, value

def parse_lessons_list(lines):
    lessons = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if not stripped.startswith('- '):
            break
        base_indent = get_indent(line)
        lesson_lines = []
        i += 1
        while i < len(lines) and get_indent(lines[i]) > base_indent:
            lesson_lines.append(lines[i])
            i += 1
        lessons.append(parse_lesson(lesson_lines))
    return lessons

def parse_lesson(lines):
    props = {}
    for line in lines:
        key, value = parse_key_value(line)
        props[key] = value
    return props

if __name__ == '__main__':
    text = read_file('schedule.yaml')
    tokens = tokenize(text)
    data = parse_yaml(tokens)
    print(data)