import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import workflow


class Records(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'evidence.txt').write_text('synthetic pass', encoding='utf-8')
        self.data = workflow.create(self.root, 'test', ['evidence.txt'])
        self.data.update(run_status='completed', checks=[{
            'name':'sample', 'criterion':'synthetic marker present',
            'status':'pass', 'evidence':'evidence.txt'}])

    def test_completed_record_with_checks(self):
        self.assertEqual(workflow.review(self.root,self.data), {
            'record_valid':True,'validation':'reported_checks_passed','issues':[]})

    def test_tampering_invalidates_pass(self):
        (self.root/'evidence.txt').write_text('changed',encoding='utf-8')
        result = workflow.review(self.root,self.data)
        self.assertFalse(result['record_valid'])
        self.assertEqual(result['validation'],'not_established')

    def test_noncompleted_never_passes(self):
        for status in ('running','stopped','failed','not_started','unknown'):
            self.data['run_status'] = status
            self.assertEqual(workflow.review(self.root,self.data)['validation'],'not_established')

    def test_no_checks_never_passes(self):
        self.data['checks'] = []
        self.assertEqual(workflow.review(self.root,self.data)['validation'],'not_established')

    def test_failure_is_not_record_corruption(self):
        self.data['checks'][0]['status'] = 'fail'
        result = workflow.review(self.root,self.data)
        self.assertTrue(result['record_valid'])
        self.assertEqual(result['validation'],'reported_checks_failed')

    def test_missing_evidence(self):
        for value in ('missing.txt', [], None):
            self.data['checks'][0]['evidence'] = value
            self.assertFalse(workflow.review(self.root,self.data)['record_valid'])

    def test_paths_cannot_escape(self):
        for path in ('../private.txt', '/tmp/private', 'C:/private', 'folder\\private'):
            with self.assertRaises(ValueError):
                workflow.contained(self.root,path)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside)/'private.txt'
            target.write_text('private',encoding='utf-8')
            try:
                (self.root/'link').symlink_to(target)
            except OSError:
                self.skipTest('Creating symlinks is unavailable on this platform')
            with self.assertRaises(ValueError):
                workflow.contained(self.root,'link')

    def test_malformed_fields_do_not_crash(self):
        for field in ('files','parameters','checks','limitations'):
            data = copy.deepcopy(self.data)
            data[field] = None
            result = workflow.review(self.root,data)
            self.assertFalse(result['record_valid'])
            self.assertIn('invalid',workflow.handoff(data,result))
        self.assertFalse(workflow.review(self.root,[])['record_valid'])

    def test_units_required(self):
        self.data['parameters'] = [{'name':'current','value':1}]
        self.assertFalse(workflow.review(self.root,self.data)['record_valid'])

    def test_cli_handoff_and_no_overwrite(self):
        manifest = self.root/'manifest.json'
        manifest.write_text(json.dumps(self.data),encoding='utf-8')
        output = self.root/'report.md'
        cmd = [sys.executable,str(ROOT/'workflow.py'),'handoff',str(manifest),'--output',str(output)]
        self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
        content = output.read_bytes()
        self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,2)
        self.assertEqual(content,output.read_bytes())

    def test_shipped_examples(self):
        for name, expected in [('success','reported_checks_passed'),('failure','reported_checks_failed'),('stopped','not_established')]:
            folder = ROOT/'examples'/f'synthetic-{name}'
            data = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
            result = workflow.review(folder,data)
            self.assertTrue(result['record_valid'])
            self.assertEqual(result['validation'],expected)


if __name__ == '__main__':
    unittest.main()
