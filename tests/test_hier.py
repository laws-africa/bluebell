from unittest import TestCase

from lxml import etree
from .support import ParserSupport


class HierTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_hier_plain(self):
        tree = self.parse("""
hello

there
""", 'hierarchical_structure')

        self.assertEqual({
            'type': 'element',
            'name': 'hierarchicalStructure',
            'children': [{
                'type': 'element',
                'name': 'body',
                'children': [{
                    'type': 'element',
                    'name': 'hcontainer',
                    'attribs': {'name': 'hcontainer'},
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

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1">
  <body>
    <hcontainer name="hcontainer" eId="hierarchicalStructure_1__hcontainer_1">
      <p>hello</p>
      <p>there</p>
    </hcontainer>
  </body>
</hierarchicalStructure>
""", xml)

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

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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

    def test_num_incremented(self):
        tree = self.parse("""
PART

  DIVISION I. - Introduction

    Some standalone text.

  DIVISION - Next heading

    Some more text.

""", 'hier_element_block')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_I">
  <division eId="part_I__dvs_I">
    <num>I.</num>
    <heading>Introduction</heading>
    <content>
      <p>Some standalone text.</p>
    </content>
  </division>
  <division eId="part_I__dvs_2">
    <heading>Next heading</heading>
    <content>
      <p>Some more text.</p>
    </content>
  </division>
  </part>
""", xml)
