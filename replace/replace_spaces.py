import sys

def replace_spaces_with_tabs(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            content = infile.read()

        modified_content = content.replace('    ', '\t')

        with open(output_file, 'w') as outfile:
            outfile.write(modified_content)

        print(f"Замена выполнена успешно. Результат записан в файл {output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <входной_файл> <выходной_файл>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        replace_spaces_with_tabs(input_file, output_file)
