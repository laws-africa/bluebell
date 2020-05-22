from unittest import TestCase

from lxml import etree
from bluebell.xml import to_xml, ids
from .support import ParserSupport


class JudgmentTestCase(TestCase, ParserSupport):
    maxDiff = None

    def setUp(self):
        ids.reset()

    def test_judgment_no_structure(self):
        tree = self.parse("""
hello

there
""", 'judgment')

        self.assertEqual({
            'type': 'element',
            'name': 'judgment',
            'children': [{
                'type': 'element',
                'name': 'judgmentBody',
                'children': [{
                    'type': 'element',
                    'name': 'arguments',
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'hello',
                        }]
                    }, {
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'there',
                        }]
                    }]
                }]
            }],
        }, tree.to_dict())

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<judgment xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <judgmentBody>
    <arguments>
      <p>hello</p>
      <p>there</p>
    </arguments>
  </judgmentBody>
</judgment>
""", xml)
