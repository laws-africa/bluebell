from unittest import TestCase

from tests.support import ParserSupport


class RTLTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_explicit_rtl_class(self):
        tree = self.parse("""
PREAMBLE

P{class rtl} טקסט כלשהו
""", 'preamble')
        self.assertEqual({
            'name': 'preamble',
            'type': 'element',
            'children': [{
                'name': 'p',
                'type': 'content',
                'attribs': {'class': 'rtl'},
                'children': [{
                    'type': 'text',
                    'value': 'טקסט כלשהו',
                }]
            }]
        }, tree.to_dict())

    def test_unparse(self):
        xml = '<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" class="rtl" foo="bar">טקסט כלשהו</p>'
        actual = self.parser.unparse(xml)
        self.assertEqual('''P{class rtl|foo bar} טקסט כלשהו

''', actual)
