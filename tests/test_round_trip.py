import os.path
from unittest import TestCase

from tests.support import print_with_lines, ParserSupport


class RoundTripTestCase(ParserSupport, TestCase):
    def roundtrip(self, prefix, root):
        dir = os.path.join(os.path.dirname(__file__), 'roundtrip')

        fname = os.path.join(dir, f'{prefix}.txt')
        with open(fname, 'rt') as f:
            input = f.read()

        text = self.parser.pre_parse(input)
        try:
            xml = self.parser.parse_to_xml(text, root)
        except:
            print_with_lines(text)
            raise

        actual = self.parser.unparse(xml)

        self.assertMultiLineEqual(input, actual)

    def test_act(self):
        self.roundtrip('act', 'act')

    def test_judgment(self):
        self.roundtrip('judgment', 'judgment')

    def test_judgment_attachments(self):
        self.roundtrip('judgment-attachments', 'judgment')

    def test_act_footnotes(self):
        self.roundtrip('act-footnotes', 'act')
