from unittest import TestCase

from lxml import etree
from bluebell.xml import to_xml
from .support import ParserSupport


class TablesTestCase(TestCase, ParserSupport):
    maxDiff = None

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

  SUBSECTION (a)
      
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
                'type': 'hier',
                'name': 'subsection',
                'num': '(a)',
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
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [],
                    }],
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [],
                    }],
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
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [],
                    }],
                }, {
                    'type': 'element',
                    'name': 'th',
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [],
                    }],
                }],
            }]
        }, tree.to_dict())

    def test_nested_blocks(self):
        """ In future, we may want to support nested blocks in cells.
        For now, they aren't supported.
        """
        tree = self.parse("""
SECTION 1.

    {|
    |
        (a) item a
              (i) item a-i
              (ii) item a-ii
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
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': '(a) item a',
                            }, {
                                'type': 'marker',
                                'name': 'eol'
                            }, {
                                'type': 'text',
                                'value': '(i) item a-i',
                            }, {
                                'type': 'marker',
                                'name': 'eol'
                            }, {
                                'type': 'text',
                                'value': '(ii) item a-ii',
                            }, {
                                'type': 'marker',
                                'name': 'eol'
                            }, {
                                'type': 'text',
                                'value': '(b) item b',
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
          <p>(a) item a<eol/>(i) item a-i<eol/>(ii) item a-ii<eol/>(b) item b</p>
        </td>
      </tr>
    </table>
  </content>
</section>
""", xml)

    def test_linebreaks(self):
        tree = self.parse("""
{|
| one

two

|

three

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
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'one',
                        }, {
                            'type': 'marker',
                            'name': 'eol',
                        }, {
                            'type': 'marker',
                            'name': 'eol',
                        }, {
                            'type': 'text',
                            'value': 'two',
                        }]
                    }]
                }, {
                    'type': 'element',
                    'name': 'td',
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'three',
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <td>
      <p>one<eol/><eol/>two</p>
    </td>
    <td>
      <p>three</p>
    </td>
  </tr>
</table>
""", xml)

    def test_non_cells(self):
        tree = self.parse("""
{|
| one
|} two
|}
""", 'table')

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <td>
      <p>one</p>
    </td>
    <td>
      <p>} two</p>
    </td>
  </tr>
</table>
""", xml)
