from unittest import TestCase

from lxml import etree
from bluebell.xml import to_xml, ids
from .support import ParserSupport


class SubflowsTestCase(TestCase, ParserSupport):
    maxDiff = None

    def setUp(self):
        ids.reset()

    def test_basic(self):
        tree = self.parse("""
{|
! r1c1
| r1c2
|-
| r2c1
| r2c2
|}
""", 'table')
        self.assertEqual({
            'type': 'element',
            'name': 'table',
            'children': [{
                'type': 'element',
                'name': 'tr',
                'children': [{
                    'type': 'element',
                    'name': 'th',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r1c1',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r1c2',
                        }]
                    }]
                }]
            }, {
                'type': 'element',
                'name': 'tr',
                'children': [{
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r2c1',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r2c2',
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <th>
      <p>r1c1</p>
    </th>
    <td>
      <p>r1c2</p>
    </td>
  </tr>
  <tr>
    <td>
      <p>r2c1</p>
    </td>
    <td>
      <p>r2c2</p>
    </td>
  </tr>
</table>
""", xml)

    def test_basic_attribs(self):
        tree = self.parse("""
{|
| colspan="2" | r1c1
|  rowspan="1"  colspan='3"' | r1c2
|-
|a="b'"| r2c1
|a="b"c="d"  | r2c2
|}
""", 'table')
        self.assertEqual({
            'type': 'element',
            'name': 'table',
            'children': [{
                'type': 'element',
                'name': 'tr',
                'children': [{
                    'type': 'element',
                    'name': 'td',
                    'attribs': {'colspan': '2'},
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r1c1',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'attribs': {'colspan': '3"', 'rowspan': '1'},
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r1c2',
                        }]
                    }]
                }]
            }, {
                'type': 'element',
                'name': 'tr',
                'children': [{
                    'type': 'element',
                    'name': 'td',
                    'attribs': {'a': "b'"},
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r2c1',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'attribs': {'a': 'b', 'c': 'd'},
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'r2c2',
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <td colspan="2">
      <p>r1c1</p>
    </td>
    <td rowspan="1" colspan="3&quot;">
      <p>r1c2</p>
    </td>
  </tr>
  <tr>
    <td a="b'">
      <p>r2c1</p>
    </td>
    <td a="b" c="d">
      <p>r2c2</p>
    </td>
  </tr>
</table>
""", xml)

    def test_multi_line_content(self):
        tree = self.parse("""
{|
| foo
bar

baz
|
 one
two

 three
|
  four

|-
|}
""", 'table')
        # TODO: this isn't right, see XML later
        self.assertEqual({
            'type': 'element',
            'name': 'table',
            'children': [{
                'type': 'element',
                'name': 'tr',
                'children': [{
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'foo',
                        }, {
                            'type': 'text',
                            'value': 'line 2',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'line 3',
                        }, {
                            'type': 'text',
                            'value': 'line 4',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'four',
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <td>
      <p>foo<eol/>bar<eol/>baz</p>
    </td>
    <td>
      <p>one<eol/>two<eol/><eol/>three</p>
    </td>
    <td>
      <p>four</p>
    </td>
  </tr>
</table>
""", xml)
