import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from fixtures import make_exam
from validate_exam import ROOT, allocate, validate_exam
from build_exam import build_exam
from jsonschema import Draft202012Validator


class ExamTests(unittest.TestCase):
    def test_schema_and_sample(self):
        Draft202012Validator.check_schema(json.loads((ROOT / 'schemas/exam.schema.json').read_text()))
        self.assertEqual([], validate_exam(json.loads((ROOT / 'examples/sample-exam.json').read_text())))

    def test_allocations(self):
        self.assertEqual({1: 4, 2: 4, 3: 4, 4: 3}, allocate(15))
        self.assertEqual({1: 19, 2: 17, 3: 16, 4: 13}, allocate(65))
        self.assertEqual({1: 8, 2: 6, 3: 6, 4: 5}, allocate(25))  # tie goes to D1
        for count in range(1, 301):
            self.assertEqual(count, sum(allocate(count).values()))
        for count in (0, -1, True, 2.5):
            with self.assertRaises(ValueError): allocate(count)

    def test_valid_sizes_and_modes(self):
        for count in (1, 15, 65):
            for mode in ('practice', 'exam'):
                self.assertEqual([], validate_exam(make_exam(count, mode)))

    def test_schema_rejects_malformed_types(self):
        for bad in (None, [], {}, {'questions': 'bad'}):
            self.assertTrue(validate_exam(bad))
        for field, value in [('question_count', True), ('mode', 'review'), ('language', '"onclick=x'), ('title', '   ')]:
            data = make_exam(); data[field] = value
            self.assertTrue(validate_exam(data), field)

    def test_integral_domain_numbers_follow_json_schema(self):
        data = make_exam()
        for question in data['questions']:
            question['primary_domain'] = float(question['primary_domain'])
        self.assertEqual([], validate_exam(data))
        data['questions'][0]['primary_domain'] = 1.5
        self.assertTrue(validate_exam(data))

    def test_count_domain_task_and_scope(self):
        for field, value in [('question_count', 16), ('extra', 1)]:
            data = make_exam(); data[field] = value
            self.assertTrue(validate_exam(data))
        for task in ('1.4', '2.1'):
            data = make_exam(); data['questions'][0]['task_id'] = task
            self.assertTrue(validate_exam(data))
        data = make_exam()
        data['questions'][0].update(primary_domain=2, task_id='2.1')
        self.assertTrue(validate_exam(data))
        data.update(scope='focused', focus='Synthetic topic')
        self.assertEqual([], validate_exam(data))
        del data['focus']; self.assertTrue(validate_exam(data))

    def test_mode_duration(self):
        data = make_exam(mode='exam'); del data['duration_minutes']
        self.assertTrue(validate_exam(data))
        for value in (0, -1, 1.5, True):
            data['duration_minutes'] = value
            self.assertTrue(validate_exam(data))
        data = make_exam(); data['duration_minutes'] = 130
        self.assertTrue(validate_exam(data))

    def test_options_and_answers(self):
        mutations = [
            lambda q: q.update(correct_option_ids=['missing']),
            lambda q: q.update(correct_option_ids=['B', 'B']),
            lambda q: q['options'].pop(),
            lambda q: q['options'][1].update(id='A'),
            lambda q: q['options'][1].update(text='  LỰA CHỌN   A '),
            lambda q: q['options'][0].update(explanation=''),
        ]
        for mutate in mutations:
            data = make_exam(); mutate(data['questions'][0]); self.assertTrue(validate_exam(data))
        for answers in (['A'], ['A','B','C','D','E']):
            data = make_exam(); data['questions'][1]['correct_option_ids'] = answers
            self.assertTrue(validate_exam(data))
        data = make_exam(); data['questions'][1]['options'].pop()
        self.assertTrue(validate_exam(data))

    def test_duplicates(self):
        for field in ('id', 'stem'):
            data = make_exam(); data['questions'][1][field] = data['questions'][0][field]
            self.assertTrue(validate_exam(data))
        data = make_exam(); data['questions'][1]['stem'] = '  ' + data['questions'][0]['stem'].upper() + '\n'
        self.assertTrue(validate_exam(data))

    def test_source_validation(self):
        for url in ('javascript:alert(1)', 'https://docs.aws.amazon.com.evil.test/a', 'https://aws.amazon.com/',
                    'https://user@docs.aws.amazon.com/page', 'https://aws.amazon.com:443/path', 'http://aws.amazon.com/a'):
            data = make_exam(); data['questions'][0]['sources'][0]['url'] = url
            self.assertTrue(validate_exam(data), url)
        for day in ('2026-02-30', '2999-01-01', 'yesterday'):
            data = make_exam(); data['questions'][0]['sources'][0]['verified_on'] = day
            self.assertTrue(validate_exam(data))

    def test_build_modes_and_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'exam.json', Path(directory) / 'out.html'
            for count in (15, 65):
                for mode in ('practice', 'exam'):
                    data = make_exam(count, mode)
                    data['title'] = '<img src=x onerror=alert(1)> @@DATA@@'
                    data['questions'][0]['stem'] = '</script><script>window.pwned=1</script>\u2028'
                    source.write_text(json.dumps(data))
                    build_exam(source, target)
                    html = target.read_text()
                    self.assertNotIn('<script>window.pwned', html)
                    self.assertIn('&lt;img', html)
                    payload = html.split('<script id="exam-data" type="application/json">')[1].split('</script>')[0]
                    self.assertEqual(data, json.loads(payload))

    def test_invalid_build_preserves_output_and_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'exam.json', Path(directory) / 'out.html'
            source.write_text('{}'); target.write_text('existing')
            with self.assertRaises(ValueError): build_exam(source, target)
            self.assertEqual('existing', target.read_text())
            with self.assertRaises(ValueError): build_exam(source, source)
            self.assertEqual('{}', source.read_text())

    def test_cli_failures_and_allocate(self):
        script = ROOT / 'scripts/validate_exam.py'
        result = subprocess.run([sys.executable, str(script), '--allocate', '15'], capture_output=True, text=True)
        self.assertEqual(0, result.returncode)
        self.assertEqual({'1':4,'2':4,'3':4,'4':3}, json.loads(result.stdout))
        result = subprocess.run([sys.executable, str(script), '--allocate', '0'], capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
