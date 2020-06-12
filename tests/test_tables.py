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

    def test_broken_tables(self):
        tree = self.parse("""
SECTION 1.
      
      {|
      |
  bar
      |}
""", 'hier_element')

        self.assertEqual({
            'type': 'hier',
            'name': 'section',
            'num': '1.',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': '{|',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': '|',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'bar',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': '|}',
                }]
            }]
        }, tree.to_dict())

    def test_empty_cells(self):
        tree = self.parse("""
{|
|
|
| x
|-
|
!
|-
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
                    'children': [],
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [],
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'x',
                        }],
                    }],
                }],
            }, {
                'type': 'element',
                'name': 'tr',
                'children': [{
                    'type': 'element',
                    'name': 'td',
                    'children': [],
                }, {
                    'type': 'element',
                    'name': 'th',
                    'children': [],
                }],
            }]
        }, tree.to_dict())

    def test_nested_blocks(self):
        tree = self.parse("""
SECTION 1.

    {|
    |
        (a) item a
              (i) item a-i
        (b) item b
    |-
    |}
""", 'hier_element')

        self.assertEqual({
            'type': 'hier',
            'name': 'section',
            'num': '1.',
            'children': [{
                'type': 'element',
                'name': 'table',
                'children': [{
                    'type': 'element',
                    'name': 'tr',
                    'children': [{
                        'type': 'element',
                        'name': 'td',
                        'children': [{
                            'type': 'block',
                            'name': 'blockList',
                            'children': [{
                                'type': 'block',
                                'name': 'item',
                                'num': '(a)',
                                'children': [{
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'item a',
                                    }],
                                }, {
                                    'type': 'block',
                                    'name': 'blockList',
                                    'children': [{
                                        'type': 'block',
                                        'name': 'item',
                                        'num': '(i)',
                                        'children': [{
                                            'type': 'content',
                                            'name': 'p',
                                            'children': [{
                                                'type': 'text',
                                                'value': 'item a-i',
                                            }]
                                        }]
                                    }]
                                }]
                            }, {
                                'type': 'block',
                                'name': 'item',
                                'num': '(b)',
                                'children': [{
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'item b',
                                    }]
                                }]
                            }]
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="sec_1">
  <num>1.</num>
  <content>
    <table eId="sec_1__table_1">
      <tr>
        <td>
          <blockList eId="list_1">
            <item eId="list_1__item_a">
              <num>(a)</num>
              <p>item a</p>
              <blockList eId="list_1__item_a__list_1">
                <item eId="list_1__item_a__list_1__item_i">
                  <num>(i)</num>
                  <p>item a-i</p>
                </item>
              </blockList>
            </item>
            <item eId="list_1__item_b">
              <num>(b)</num>
              <p>item b</p>
            </item>
          </blockList>
        </td>
      </tr>
    </table>
  </content>
</section>
""", xml)

    def test_linebreaks(self):
        tree = self.parse("""
{|
| foo
bar
|
foo
|}
""", 'table')

        # TODO: this isn't quite right yet
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
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'foo',
                        }, {
                            'type': 'marker',
                            'name': 'br',
                        }, {
                            'type': 'text',
                            'value': 'bar',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'marker',
                            'name': 'br',
                        }, {
                            'type': 'text',
                            'value': 'foo',
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <td>
      <p>foo<br>bar</p>
    </td>
      <td><br>foo</p>
    </td>
  </tr>
</table>
""", xml)
