import sys
import re
import yaml

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, content):
        lines = content.split('\n')
        result = {}
        in_multiline_comment = False
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith('REM'):
                continue
            elif line.startswith('/*'):
                in_multiline_comment = True
                continue
            elif in_multiline_comment:
                if line.endswith('*/'):
                    in_multiline_comment = False
                continue
            elif line.startswith('const'):
                match = re.match(r'const\s+([a-z][a-z0-9_]*)\s*=\s*(.*)', line)
                if match:
                    name, value = match.groups()
                    result[name] = self.parse_value(value)
                    self.constants[name] = result[name]
                else:
                    raise ValueError(f"Invalid const declaration at line {line_number}: {line}")
            elif line.startswith('!{'):
                match = re.match(r'!\{([a-z][a-z0-9_]*)\}', line)
                if match:
                    name = match.group(1)
                    if name in self.constants:
                        result[name] = self.constants[name]
                    else:
                        raise ValueError(f"Undefined constant at line {line_number}: {name}")
                else:
                    raise ValueError(f"Invalid constant reference at line {line_number}: {line}")
            elif line.startswith('(list'):
                match = re.match(r'\(list\s+(.*)\s*\)', line)
                if match:
                    values = match.group(1).split()
                    result['list'] = [self.parse_value(v) for v in values]
                else:
                    raise ValueError(f"Invalid list declaration at line {line_number}: {line}")
            else:
                raise ValueError(f"Unknown syntax at line {line_number}: {line}")
        return result

    def parse_value(self, value):
        if value.isdigit():
            return int(value)
        elif value.startswith('!{'):
            match = re.match(r'!\{([a-z][a-z0-9_]*)\}', value)
            if match:
                name = match.group(1)
                if name in self.constants:
                    return self.constants[name]
                else:
                    raise ValueError(f"Undefined constant: {name}")
            else:
                raise ValueError(f"Invalid constant reference: {value}")
        else:
            return value  # Возвращаем строковое значение

def main():
    if len(sys.argv) != 2:
        print("Usage: python config_parser.py <path_to_config_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        content = file.read()

    parser = ConfigParser()
    try:
        result = parser.parse(content)
        print(yaml.dump(result, default_flow_style=False))
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
