from unittest import TestCase

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
            'attribs': {'name': 'hierarchicalStructure'},
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_1" name="hcontainer">
      <p eId="hierarchicalStructure_1__hcontainer_1__p_1">hello</p>
      <p eId="hierarchicalStructure_1__hcontainer_1__p_2">there</p>
    </hcontainer>
  </body>
</hierarchicalStructure>
""", xml)

    def test_hier_with_block_lists(self):
        tree = self.parse("""
PART

  BLOCKLIST

    ITEM (a)

      item a

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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_nn_1">
  <intro>
    <p eId="part_nn_1__intro__p_1">some intro text</p>
  </intro>
  <section eId="part_nn_1__sec_1">
    <num>1</num>
    <content>
      <p eId="part_nn_1__sec_1__p_1">section 1 text</p>
    </content>
  </section>
  <hcontainer eId="part_nn_1__hcontainer_1" name="hcontainer">
    <content>
      <p eId="part_nn_1__hcontainer_1__p_1">some interstitial text</p>
    </content>
  </hcontainer>
  <section eId="part_nn_1__sec_2">
    <num>2</num>
    <content>
      <p eId="part_nn_1__sec_2__p_1">section 2 text</p>
    </content>
  </section>
  <wrapUp>
    <p eId="part_nn_1__wrapup__p_1">conclusion</p>
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_nn_1">
  <intro>
    <p eId="part_nn_1__intro__p_1">some intro text</p>
  </intro>
  <section eId="part_nn_1__sec_1">
    <num>1</num>
    <content>
      <p eId="part_nn_1__sec_1__p_1">section 1 text</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_2">
    <num>2</num>
    <content>
      <p eId="part_nn_1__sec_2__p_1">section 2 text</p>
    </content>
  </section>
  <wrapUp>
    <p eId="part_nn_1__wrapup__p_1">conclusion</p>
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_nn_1">
  <section eId="part_nn_1__sec_1">
    <num>1</num>
    <content>
      <p eId="part_nn_1__sec_1__p_1">section 1 text</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_2">
    <num>2</num>
    <content>
      <p eId="part_nn_1__sec_2__p_1">section 2 text</p>
    </content>
  </section>
</part>
""", xml)

    def test_hier_empty_heading_or_num(self):
        tree = self.parse("""
SEC 1.
  PART
    no num no heading
      
  PART 1. -
    no heading

  PART -
    no num no heading

  PART 2.
    no heading
      
  PART - heading
    no num
    
  PART 3-a - head-ing and - here
    dash in num and heading
    
  PART 4- -heading
    dash in num no heading
    
  PART -5 -heading
    dash in num no heading
    
  PART -6 heading
    dash in num no heading
    
  PART -6 - heading
    dash in num with heading
""", 'hier_element_block')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="sec_1">
  <num>1.</num>
  <part eId="sec_1__part_nn_1">
    <content>
      <p eId="sec_1__part_nn_1__p_1">no num no heading</p>
    </content>
  </part>
  <part eId="sec_1__part_1">
    <num>1.</num>
    <content>
      <p eId="sec_1__part_1__p_1">no heading</p>
    </content>
  </part>
  <part eId="sec_1__part_nn_2">
    <content>
      <p eId="sec_1__part_nn_2__p_1">no num no heading</p>
    </content>
  </part>
  <part eId="sec_1__part_2">
    <num>2.</num>
    <content>
      <p eId="sec_1__part_2__p_1">no heading</p>
    </content>
  </part>
  <part eId="sec_1__part_nn_3">
    <heading>heading</heading>
    <content>
      <p eId="sec_1__part_nn_3__p_1">no num</p>
    </content>
  </part>
  <part eId="sec_1__part_3-a">
    <num>3-a</num>
    <heading>head-ing and - here</heading>
    <content>
      <p eId="sec_1__part_3-a__p_1">dash in num and heading</p>
    </content>
  </part>
  <part eId="sec_1__part_4-heading">
    <num>4- -heading</num>
    <content>
      <p eId="sec_1__part_4-heading__p_1">dash in num no heading</p>
    </content>
  </part>
  <part eId="sec_1__part_5-heading">
    <num>-5 -heading</num>
    <content>
      <p eId="sec_1__part_5-heading__p_1">dash in num no heading</p>
    </content>
  </part>
  <part eId="sec_1__part_6heading">
    <num>-6 heading</num>
    <content>
      <p eId="sec_1__part_6heading__p_1">dash in num no heading</p>
    </content>
  </part>
  <part eId="sec_1__part_6">
    <num>-6</num>
    <heading>heading</heading>
    <content>
      <p eId="sec_1__part_6__p_1">dash in num with heading</p>
    </content>
  </part>
</section>
""", xml)

    def test_empty_subheading(self):
        tree = self.parse("""
PART 1 - Heading
  SUBHEADING

  text
""", 'hier_element_block')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_1">
  <num>1</num>
  <heading>Heading</heading>
  <content>
    <p eId="part_1__p_1">text</p>
  </content>
</part>
""", xml)

    def test_empty_elements(self):
        tree = self.parse("""
PART

  SEC 1 - heading

  SEC
    SUBHEADING subheading

  PART

  CHAPTER - heading
""", 'hier_element_block')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_nn_1">
  <section eId="part_nn_1__sec_1">
    <num>1</num>
    <heading>heading</heading>
  </section>
  <section eId="part_nn_1__sec_nn_1">
    <subheading>subheading</subheading>
  </section>
  <part eId="part_nn_1__part_nn_1"/>
  <chapter eId="part_nn_1__chp_nn_1">
    <heading>heading</heading>
  </chapter>
</part>
""", xml)
