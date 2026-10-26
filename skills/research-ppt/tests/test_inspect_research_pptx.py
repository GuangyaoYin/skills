import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_research_pptx.py"
spec = importlib.util.spec_from_file_location('research_inspector', SCRIPT)
inspector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspector)
P = inspector.NS['p']
A = inspector.NS['a']
R = inspector.NS['r']
PR = inspector.NS['pr']
M = inspector.NS['m']
A14 = inspector.NS['a14']


def fixture(path, kind='native', note_type='body', order=(1,)):
    with ZipFile(path, 'w') as z:
        ids = ''.join(f'<p:sldId id="{255+n}" r:id="rId{n}"/>' for n in order)
        z.writestr('ppt/presentation.xml', f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst>{ids}</p:sldIdLst></p:presentation>')
        rels = ''.join(f'<Relationship Id="rId{n}" Type="{R}/slide" Target="slides/slide{n}.xml"/>' for n in order)
        z.writestr('ppt/_rels/presentation.xml.rels', f'<Relationships xmlns="{PR}">{rels}</Relationships>')
        for n in order:
            if kind == 'native':
                content = '<a14:m><m:oMathPara><m:oMath><m:f><m:num><m:r><m:t>x</m:t></m:r></m:num><m:den><m:r><m:t>y</m:t></m:r></m:den></m:f></m:oMath></m:oMathPara></a14:m>'
            elif kind == 'empty':
                content = '<a14:m><m:oMathPara><m:oMath/></m:oMathPara></a14:m>'
            else:
                content = '<a:r><a:t>x/y</a:t></a:r>'
            picture = '<p:pic/>' if kind == 'picture' else ''
            z.writestr(f'ppt/slides/slide{n}.xml', f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:a14="{A14}" xmlns:m="{M}"><p:cSld><p:spTree>{picture}<p:sp><p:txBody><a:bodyPr/><a:lstStyle/><a:p>{content}</a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>')
            z.writestr(f'ppt/slides/_rels/slide{n}.xml.rels', f'<Relationships xmlns="{PR}"><Relationship Id="n1" Type="{R}/notesSlide" Target="../notesSlides/notesSlide{n}.xml"/></Relationships>')
            z.writestr(f'ppt/notesSlides/notesSlide{n}.xml', f'<p:notes xmlns:p="{P}" xmlns:a="{A}"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:nvPr><p:ph type="{note_type}"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>Notes for discussion</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>')


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'case.pptx'

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(self.path), *args], capture_output=True, text=True, encoding='utf-8')
        return result, json.loads(result.stdout) if result.stdout else None

    def test_native_structure_and_notes(self):
        fixture(self.path)
        result, report = self.run_cli('--expected-slides', '1', '--expected-equations', '1', '--require-notes')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report['native_equation_candidates'], 1)
        self.assertNotIn('Notes for discussion', result.stdout)

    def test_non_equations_are_not_counted(self):
        for kind in ('picture', 'text', 'empty'):
            with self.subTest(kind=kind):
                fixture(self.path, kind=kind)
                result, report = self.run_cli('--expected-equations', '1')
                self.assertEqual(result.returncode, 1)
                self.assertEqual(report['native_equation_candidates'], 0)

    def test_slide_number_does_not_satisfy_notes(self):
        fixture(self.path, note_type='sldNum')
        result, report = self.run_cli('--require-notes')
        self.assertEqual(result.returncode, 1)
        self.assertFalse(report['slides'][0]['has_nonempty_notes_body'])

    def test_slide_order_uses_relationships(self):
        fixture(self.path, order=(2, 1))
        report = inspector.inspect_pptx(self.path)
        self.assertEqual([s['part'] for s in report['slides']], ['ppt/slides/slide2.xml', 'ppt/slides/slide1.xml'])

    def test_slide_count_mismatch(self):
        fixture(self.path)
        result, report = self.run_cli('--expected-slides', '2')
        self.assertEqual(result.returncode, 1)
        self.assertTrue(report['errors'])

    def test_invalid_package_reports_failure(self):
        self.path.write_text('not a zip', encoding='utf-8')
        result, report = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(report['structural_checks_ok'])

    def test_json_cannot_replace_input(self):
        fixture(self.path)
        original = self.path.read_bytes()
        result, _ = self.run_cli('--json-out', str(self.path))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.path.read_bytes(), original)


if __name__ == '__main__':
    unittest.main(verbosity=2)
