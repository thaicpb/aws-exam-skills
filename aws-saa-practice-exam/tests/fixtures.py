"""Synthetic data for software tests ONLY; not an AWS question bank."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_exam import allocate


def make_exam(count=15, mode='practice'):
    questions = []
    for domain, size in allocate(count).items():
        for _ in range(size):
            index = len(questions)
            multiple = index % 5 == 1
            questions.append({
                'id': f'q{index}', 'stem': f'Fixture kỹ thuật {index + 1}; không dùng để học AWS.',
                'primary_domain': domain, 'task_id': f'{domain}.1', 'service_tags': ['TEST_ONLY'],
                'type': 'multiple' if multiple else 'single',
                'options': [{'id': letter, 'text': f'Lựa chọn {letter}', 'explanation': f'Giải thích kiểm thử {letter}'}
                            for letter in ('ABCDE' if multiple else 'ABCD')],
                'correct_option_ids': ['A', 'C'] if multiple else ['B'],
                'sources': [{'title': 'Nguồn fixture — không xác minh nội dung câu',
                             'url': 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html',
                             'verified_on': '2026-09-14'}]
            })
    data = {'schema_version': 1, 'exam_code': 'SAA-C03', 'title': f'Kiểm thử {count} câu — không dùng ôn thi',
            'language': 'vi', 'mode': mode, 'scope': 'mixed', 'question_count': count, 'questions': questions}
    if mode == 'exam':
        data['duration_minutes'] = 130
    return data


if __name__ == '__main__':
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for mode in ('practice', 'exam'):
        for count in (15, 65):
            (out / f'{mode}-{count}.json').write_text(json.dumps(make_exam(count, mode), ensure_ascii=False), encoding='utf-8')
