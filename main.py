def parse_yaml_to_object(text):
    lines = text.split('\n')
    root = {}
    stack = [(-1, root)]
    
    for line in lines:
        if not line.strip() or line.strip().startswith('#'):
            continue
            
        indent = len(line) - len(line.lstrip())
        content = line.strip()
        
        while stack and indent <= stack[-1][0]:
            stack.pop()
            
        current_container = stack[-1][1]
        
        if content.startswith('-'):
            if not isinstance(current_container, list):
                continue
            
            item_content = content[1:].strip()
            
            if ':' in item_content:
                key, val = item_content.split(':', 1)
                new_obj = {key.strip(): val.strip().strip('"')}
                current_container.append(new_obj)
                stack.append((indent, new_obj))
            else:
                current_container.append(item_content.strip('"'))
                
        elif ':' in content:
            key, val = content.split(':', 1)
            key = key.strip()
            val = val.strip()
            
            if val == '' or val == '[]':
                new_val = [] if val == '[]' else {}
                if isinstance(current_container, dict):
                    current_container[key] = new_val
                stack.append((indent, new_val))
            else:
                if isinstance(current_container, dict):
                    current_container[key] = val.strip('"')
                    
    return root

with open('schedule.yaml', 'r', encoding='utf-8') as f:
    yaml_text = f.read()

schedule_object = parse_yaml_to_object(yaml_text)
