from unittest import TestCase, expectedFailure

from tests.support import ParserSupport


class TablesTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_basic(self):
        tree = self.parse("""
TABLE
  TR
    TH
      r1c1
      
    TC
      r1c2
      
  TR
    TC
      r2c1
      
    TC
      r2c2
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <th>
      <p eId="table_1__p_1">r1c1</p>
    </th>
    <td>
      <p eId="table_1__p_2">r1c2</p>
    </td>
  </tr>
  <tr>
    <td>
      <p eId="table_1__p_3">r2c1</p>
    </td>
    <td>
      <p eId="table_1__p_4">r2c2</p>
    </td>
  </tr>
</table>
""", xml)

    def test_basic_attribs(self):
        tree = self.parse("""
TABLE{class my-table}
  TR
    TC{colspan 2}
      r1c1
    TC{rowspan 1 | colspan 3"}
      r1c2
  TR
    TC{|   |a}
      r2c1
    TC
      r2c2
""", 'table')
        self.assertEqual({
            'type': 'element',
            'name': 'table',
            'attribs': {'class': 'my-table'},
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
                    'attribs': {'a': ''},
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" class="my-table" eId="table_1">
  <tr>
    <td colspan="2">
      <p eId="table_1__p_1">r1c1</p>
    </td>
    <td colspan="3&quot;" rowspan="1">
      <p eId="table_1__p_2">r1c2</p>
    </td>
  </tr>
  <tr>
    <td a="">
      <p eId="table_1__p_3">r2c1</p>
    </td>
    <td>
      <p eId="table_1__p_4">r2c2</p>
    </td>
  </tr>
</table>
""", xml)

    def test_broken_tables(self):
        tree = self.parse("""
SECTION 1.

  SUBSECTION (a)
  
    TABLE
      TR
  bar
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
                        'value': 'TABLE',
                    }]
                }, {
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'TR',
                    }]
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'bar',
                }]
            }]
        }, tree.to_dict())

    def test_empty_cells(self):
        tree = self.parse("""
TABLE
  TR
    TC
    TC
    TC
      x
  TR
    TC
    TH
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
        tree = self.parse("""
SECTION 1.

  TABLE
    TR
      TC
        BLOCKLIST
          ITEM (a)
            item a
            BLOCKLIST
              ITEM (i)
                item a-i
              ITEM (ii)
                item a-ii
          ITEM (b)
            item b
""", 'hier_element')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="sec_1">
  <num>1.</num>
  <content>
    <table eId="sec_1__table_1">
      <tr>
        <td>
          <blockList eId="sec_1__table_1__list_1">
            <item eId="sec_1__table_1__list_1__item_a">
              <num>(a)</num>
              <p eId="sec_1__table_1__list_1__item_a__p_1">item a</p>
              <blockList eId="sec_1__table_1__list_1__item_a__list_1">
                <item eId="sec_1__table_1__list_1__item_a__list_1__item_i">
                  <num>(i)</num>
                  <p eId="sec_1__table_1__list_1__item_a__list_1__item_i__p_1">item a-i</p>
                </item>
                <item eId="sec_1__table_1__list_1__item_a__list_1__item_ii">
                  <num>(ii)</num>
                  <p eId="sec_1__table_1__list_1__item_a__list_1__item_ii__p_1">item a-ii</p>
                </item>
              </blockList>
            </item>
            <item eId="sec_1__table_1__list_1__item_b">
              <num>(b)</num>
              <p eId="sec_1__table_1__list_1__item_b__p_1">item b</p>
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
TABLE
  TR
    TC
      one
      
      two
      
    TC
    
      three
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
                        }]
                    }, {
                        'type': 'content',
                        'name': 'p',
                        'children': [{
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <td>
      <p eId="table_1__p_1">one</p>
      <p eId="table_1__p_2">two</p>
    </td>
    <td>
      <p eId="table_1__p_3">three</p>
    </td>
  </tr>
</table>
""", xml)

    @expectedFailure
    def test_empty_attribs(self):
        # TODO: empty rowSpan and colSpan should not be allowed
        tree = self.parse("""
TABLE
  TR
    TC{rowSpan}
      one
    TC{colSpan}
      two
""", 'table')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<table xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="table_1">
  <tr>
    <td>
      <p eId="table_1__p_1">one</p>
    </td>
    <td>
      <p eId="table_1__p_2">two</p>
    </td>
  </tr>
</table>
""", xml)
