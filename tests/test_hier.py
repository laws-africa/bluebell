from unittest import TestCase

from lxml import etree
from bluebell.xml import to_xml, ids
from .support import ParserSupport


class HierTestCase(TestCase, ParserSupport):
    maxDiff = None

    def setUp(self):
        ids.reset()

    def test_hier_with_block_lists(self):
        tree = self.parse("""
PART

  (a) item a

    indent

      indent
""", 'hier_element_block')
        self.assertEqual({
            'name': 'part',
            'type': 'hier',
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
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'indent',
                        }],
                    }, {
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'indent',
                        }],
                    }]
                }]
            }]
        }, tree.to_dict())

    def test_hier_nested_indents(self):
        tree = self.parse("""
PART

  indent
  
    indent
      
      indent
""", 'hier_element_block')
        self.assertEqual({
            'name': 'part',
            'type': 'hier',
            'children': [{
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'indent',
                }],
            }, {
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'indent',
                }],
            }, {
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'indent',
                }],
            }]
        }, tree.to_dict())

    def test_mixed_hier_content(self):
        tree = self.parse("""
PART

  some intro text
  
  SECTION 1
  
    section 1 text
    
  some interstitial text
    
  SECTION 2
  
    section 2 text
    
  conclusion
""", 'hier_element_block')

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_1">
  <intro>
    <p>some intro text</p>
  </intro>
  <section eId="part_1__sec_1">
    <num>1</num>
    <content>
      <p>section 1 text</p>
    </content>
  </section>
  <container name="container" eId="part_1__container_1">
    <p>some interstitial text</p>
  </container>
  <section eId="part_1__sec_2">
    <num>2</num>
    <content>
      <p>section 2 text</p>
    </content>
  </section>
  <wrapUp>
    <p>conclusion</p>
  </wrapUp>
</part>
""", xml)

    def test_intro_wrapup(self):
        tree = self.parse("""
PART

  some intro text

  SECTION 1

    section 1 text

  SECTION 2

    section 2 text

  conclusion
""", 'hier_element_block')

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_1">
  <intro>
    <p>some intro text</p>
  </intro>
  <section eId="part_1__sec_1">
    <num>1</num>
    <content>
      <p>section 1 text</p>
    </content>
  </section>
  <section eId="part_1__sec_2">
    <num>2</num>
    <content>
      <p>section 2 text</p>
    </content>
  </section>
  <wrapUp>
    <p>conclusion</p>
  </wrapUp>
</part>
""", xml)

    def test_only_hier_children(self):
        tree = self.parse("""
PART

  SECTION 1

    section 1 text

  SECTION 2

    section 2 text
""", 'hier_element_block')

        xml = etree.tostring(to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_1">
  <section eId="part_1__sec_1">
    <num>1</num>
    <content>
      <p>section 1 text</p>
    </content>
  </section>
  <section eId="part_1__sec_2">
    <num>2</num>
    <content>
      <p>section 2 text</p>
    </content>
  </section>
</part>
""", xml)
