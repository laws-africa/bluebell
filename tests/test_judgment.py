from unittest import TestCase

from tests.support import ParserSupport


class JudgmentTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_judgment_no_structure(self):
        tree = self.parse("""
hello

there
""", 'judgment')

        self.assertEqual({
            'type': 'element',
            'name': 'judgment',
            'attribs': {'name': 'judgment'},
            'children': [{
                'type': 'element',
                'name': 'header',
            }, {
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<judgment xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="judgment">
  <header/>
  <judgmentBody>
    <arguments>
      <p eId="arguments__p_1">hello</p>
      <p eId="arguments__p_2">there</p>
    </arguments>
  </judgmentBody>
</judgment>
""", xml)
