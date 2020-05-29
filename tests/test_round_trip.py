import os.path
from unittest import TestCase

from bluebell.parser import parse_with_failure, unparse, parse_tree_to_xml, pre_parse
from tests.support import print_with_lines


class RoundTripTestCase(TestCase):
    def roundtrip(self, prefix, root):
        dir = os.path.join(os.path.dirname(__file__), 'roundtrip')

        fname = os.path.join(dir, f'{prefix}.txt')
        with open(fname, 'rt') as f:
            input = f.read()

        text = pre_parse(input, indent='{', dedent='}')
        try:
            tree = parse_with_failure(text, root)
            xml = parse_tree_to_xml(tree)
        except:
            print_with_lines(text)
            raise

        actual = unparse(xml)

        self.assertMultiLineEqual(actual, input)

    def test_act(self):
        self.roundtrip('act', 'act')

    def test_judgment(self):
        self.roundtrip('judgment', 'judgment')

    def test_judgment_attachments(self):
        self.roundtrip('judgment-attachments', 'judgment')

    def test_act_footnotes(self):
        self.roundtrip('act-footnotes', 'act')
