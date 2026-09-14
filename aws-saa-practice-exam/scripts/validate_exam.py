#!/usr/bin/env python3
"""Validate the published JSON schema and cross-field exam invariants."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit('Thiếu jsonschema. Chạy: python -m pip install -r requirements.txt')

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = (30, 26, 24, 20)
TASK_COUNTS = (3, 2, 5, 4)


def allocate(count):
    """Largest remainders, ties resolved by ascending domain number."""
    if type(count) is not int or count < 1:
        raise ValueError('Số câu phải là số nguyên dương.')
    result = [count * weight // 100 for weight in WEIGHTS]
    order = sorted(range(4), key=lambda i: (-(count * WEIGHTS[i] % 100), i))
    for index in order[:count - sum(result)]:
        result[index] += 1
    return {i + 1: value for i, value in enumerate(result)}


def normalize(value):
    return ' '.join(value.casefold().split())


def validate_exam(data):
    schema = json.loads((ROOT / 'schemas/exam.schema.json').read_text(encoding='utf-8'))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [f'{"/".join(map(str, error.absolute_path)) or "$"}: {error.message}'
              for error in validator.iter_errors(data)]
    if errors:
        return errors  # Safe to inspect typed fields only after schema validation.
    questions = data['questions']
    if data['question_count'] != len(questions):
        errors.append('question_count không khớp số câu thực tế.')
    ids, stems = set(), set()
    for question in questions:
        qid = question['id']
        if qid in ids:
            errors.append(f'{qid}: ID câu trùng.')
        ids.add(qid)
        stem = normalize(question['stem'])
        if stem in stems:
            errors.append(f'{qid}: nội dung câu trùng.')
        stems.add(stem)
        # JSON Schema integers include integral JSON numbers such as 1.0.
        domain = int(question['primary_domain'])
        valid_tasks = {f'{domain}.{i}' for i in range(1, TASK_COUNTS[domain - 1] + 1)}
        if question['task_id'] not in valid_tasks:
            errors.append(f'{qid}: task_id không thuộc domain hoặc không tồn tại.')
        options = question['options']
        option_ids = [option['id'] for option in options]
        if len(set(option_ids)) != len(option_ids):
            errors.append(f'{qid}: ID lựa chọn trùng.')
        if len({normalize(option['text']) for option in options}) != len(options):
            errors.append(f'{qid}: nội dung lựa chọn trùng.')
        correct = set(question['correct_option_ids'])
        if not correct.issubset(option_ids):
            errors.append(f'{qid}: đáp án tham chiếu lựa chọn không tồn tại.')
        if len(correct) >= len(options):
            errors.append(f'{qid}: phải có ít nhất một phương án sai.')
        for source in question['sources']:
            url = urlsplit(source['url'])
            if (url.scheme != 'https' or url.hostname not in {'docs.aws.amazon.com', 'aws.amazon.com'}
                    or url.username is not None or url.password is not None
                    or url.netloc != url.hostname or not url.path.strip('/')):
                errors.append(f'{qid}: nguồn phải là URL HTTPS trang cụ thể trên docs.aws.amazon.com hoặc aws.amazon.com.')
            if date.fromisoformat(source['verified_on']) > date.today():
                errors.append(f'{qid}: ngày xác minh không được ở tương lai.')
    actual = Counter(question['primary_domain'] for question in questions)
    if data['scope'] == 'mixed' and dict(sorted((d, actual[d]) for d in range(1, 5))) != allocate(len(questions)):
        errors.append(f'Phân bổ mixed không đúng: thực tế {dict(actual)}, cần {allocate(len(questions))}.')
    return errors


def load_exam(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    errors = validate_exam(data)
    if errors:
        raise ValueError('\n'.join(errors))
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('input', nargs='?', type=Path)
    group.add_argument('--allocate', type=int, metavar='N')
    args = parser.parse_args()
    try:
        if args.allocate is not None:
            print(json.dumps(allocate(args.allocate)))
        else:
            data = load_exam(args.input)
            print(f'Hợp lệ: {len(data["questions"])} câu, {data["mode"]}, {data["scope"]}. Chưa xác minh ngữ nghĩa/URL bằng validator.')
    except (OSError, ValueError) as error:
        print(f'Lỗi: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
