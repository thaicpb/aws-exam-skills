#!/usr/bin/env python3
"""Build a validated exam as a self-contained offline HTML file."""
import argparse
import html
import json
from pathlib import Path
import re
import sys

from validate_exam import ROOT, load_exam


def build_exam(input_path, output_path):
    input_path, output_path = Path(input_path), Path(output_path)
    if input_path.resolve() == output_path.resolve():
        raise ValueError('Đường dẫn output phải khác input.')
    data = load_exam(input_path)
    # JSON is embedded in a script element; prevent closing the element with input text.
    payload = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    payload = payload.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    template = (ROOT / 'assets/quiz-template.html').read_text(encoding='utf-8')
    # Substitute in one pass so user text cannot be interpreted as another placeholder.
    replacements = {'TITLE': html.escape(data['title']), 'LANG': html.escape(data['language'], quote=True),
                    'ENGINE': (ROOT / 'assets/quiz-engine.js').read_text(encoding='utf-8'), 'DATA': payload}
    rendered = re.sub(r'@@(TITLE|LANG|ENGINE|DATA)@@', lambda match: replacements[match[1]], template)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding='utf-8')
    return output_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(build_exam(args.input, args.output))
    except (OSError, ValueError) as error:
        print(f'Lỗi: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
