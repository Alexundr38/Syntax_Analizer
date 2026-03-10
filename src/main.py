import sys
import json
from Syntax_Analizer.src.tokenizer import tokenize
from Syntax_Analizer.src.parser import Parser

def main():
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
    else:
        input_filename = 'data/queries.txt'

    output_filename = 'data/parsed.txt'

    if output_filename:
        sys.stdout = open(output_filename, 'w', encoding='utf-8')

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл {input_filename} не найден.")
        return

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        print(f"Запрос {idx}: {line}")
        try:
            tokens = tokenize(line)
            parser = Parser(tokens)
            tree = parser.parse_query()
            print("Дерево разбора:")
            print(json.dumps(tree, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"Результат: ОШИБКА")
            print(f"Детали: {e}")
        print("-" * 60)

    if output_filename:
        sys.stdout.close()

if __name__ == '__main__':
    main()