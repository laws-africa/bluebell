from unittest import TestCase

from lxml import etree
from tests.support import ParserSupport


class InlineTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_remark(self):
        tree = self.parse("""
[[a remark]]
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [{
                'type': 'inline',
                'name': 'remark',
                'attribs': {'status': 'editorial'},
                'children': [{
                    'type': 'text',
                    'value': '[a remark]',
                }]
            }],
        }, tree.to_dict())

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <remark status="editorial">[a remark]</remark>
</p>
""", xml)

    def test_remark_with_inlines(self):
        tree = self.parse("""
[[[a link](https://example.com)]]
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [{
                'type': 'inline',
                'name': 'remark',
                'attribs': {'status': 'editorial'},
                'children': [{
                    'type': 'text',
                    'value': '[',
                }, {
                    'type': 'inline',
                    'name': 'ref',
                    'attribs': {'href': 'https://example.com'},
                    'children': [{
                        'type': 'text',
                        'value': 'a link',
                    }]
                }, {
                    'type': 'text',
                    'value': ']',
                }]
            }],
        }, tree.to_dict())

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <remark status="editorial">[<ref href="https://example.com">a link</ref>]</remark>
</p>
""", xml)
