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
                        'type': 'element',
                        'name': 'content',
                        'children': [{
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'hello',
                            }]}, {
                                'type': 'content',
                                'name': 'p',
                                'children': [{
                                    'type': 'text',
                                    'value': 'there',
                                }]
                            }]
                    }]
                }]
            }],
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_1" name="hcontainer">
      <content>
        <p eId="hierarchicalStructure_1__hcontainer_1__p_1">hello</p>
        <p eId="hierarchicalStructure_1__hcontainer_1__p_2">there</p>
      </content>
    </hcontainer>
  </body>
</hierarchicalStructure>
""", xml)

    def test_hier_top_level_crossHeading_1(self):
        tree = self.parse("""
CROSSHEADING test crossheading

text
""", 'hierarchical_structure')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_1" name="hcontainer">
      <crossHeading eId="hierarchicalStructure_1__hcontainer_1__crossHeading_1">test crossheading</crossHeading>
    </hcontainer>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_2" name="hcontainer">
      <content>
        <p eId="hierarchicalStructure_1__hcontainer_2__p_1">text</p>
      </content>
    </hcontainer>
  </body>
</hierarchicalStructure>
""", xml)

    def test_hier_top_level_crossHeading_2(self):
        tree = self.parse("""
text 1

CROSSHEADING test crossheading

text 2
""", 'hierarchical_structure')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_1" name="hcontainer">
      <content>
        <p eId="hierarchicalStructure_1__hcontainer_1__p_1">text 1</p>
      </content>
    </hcontainer>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_2" name="hcontainer">
      <crossHeading eId="hierarchicalStructure_1__hcontainer_2__crossHeading_1">test crossheading</crossHeading>
    </hcontainer>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_3" name="hcontainer">
      <content>
        <p eId="hierarchicalStructure_1__hcontainer_3__p_1">text 2</p>
      </content>
    </hcontainer>
  </body>
</hierarchicalStructure>
""", xml)

    def test_hier_top_level_crossHeading_3(self):
        tree = self.parse("""
CROSSHEADING test crossheading

PART 1
  test
""", 'hierarchical_structure')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_1" name="hcontainer">
      <crossHeading eId="hierarchicalStructure_1__hcontainer_1__crossHeading_1">test crossheading</crossHeading>
    </hcontainer>
    <part eId="hierarchicalStructure_1__part_1">
      <num>1</num>
      <content>
        <p eId="hierarchicalStructure_1__part_1__p_1">test</p>
      </content>
    </part>
  </body>
</hierarchicalStructure>
""", xml)

    def test_hier_top_level_crossHeading_4(self):
        tree = self.parse("""
CROSSHEADING crossheading one
CROSSHEADING crossheading two

text
""", 'hierarchical_structure')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_1" name="hcontainer">
      <crossHeading eId="hierarchicalStructure_1__hcontainer_1__crossHeading_1">crossheading one</crossHeading>
      <crossHeading eId="hierarchicalStructure_1__hcontainer_1__crossHeading_2">crossheading two</crossHeading>
    </hcontainer>
    <hcontainer eId="hierarchicalStructure_1__hcontainer_2" name="hcontainer">
      <content>
        <p eId="hierarchicalStructure_1__hcontainer_2__p_1">text</p>
      </content>
    </hcontainer>
  </body>
</hierarchicalStructure>
""", xml)

    def test_hier_crossHeading_with_blocks_1(self):
        # crossheading after block elements requires block elements to be in an intro block
        tree = self.parse("""
SEC
  ITEMS
    ITEM
      item 1
        
  CROSSHEADING crossheading one
""", 'hierarchical_structure')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <section eId="hierarchicalStructure_1__sec_nn_1">
      <intro>
        <blockList eId="hierarchicalStructure_1__sec_nn_1__intro__list_1">
          <item eId="hierarchicalStructure_1__sec_nn_1__intro__list_1__item_nn_1">
            <p eId="hierarchicalStructure_1__sec_nn_1__intro__list_1__item_nn_1__p_1">item 1</p>
          </item>
        </blockList>
      </intro>
      <crossHeading eId="hierarchicalStructure_1__sec_nn_1__crossHeading_1">crossheading one</crossHeading>
    </section>
  </body>
</hierarchicalStructure>
""", xml)

    def test_hier_crossHeading_with_blocks_2(self):
        # crossheading before block elements requires block elements to be in a wrapUp block
        tree = self.parse("""
SEC
  CROSSHEADING crossheading one
  
  ITEMS
    ITEM
      item 1
""", 'hierarchical_structure')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<hierarchicalStructure xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="hierarchicalStructure_1" name="hierarchicalStructure">
  <body>
    <section eId="hierarchicalStructure_1__sec_nn_1">
      <crossHeading eId="hierarchicalStructure_1__sec_nn_1__crossHeading_1">crossheading one</crossHeading>
      <wrapUp>
        <blockList eId="hierarchicalStructure_1__sec_nn_1__wrapup__list_1">
          <item eId="hierarchicalStructure_1__sec_nn_1__wrapup__list_1__item_nn_1">
            <p eId="hierarchicalStructure_1__sec_nn_1__wrapup__list_1__item_nn_1__p_1">item 1</p>
          </item>
        </blockList>
      </wrapUp>
    </section>
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

    def test_empty_body(self):
        tree = self.parse("""
PREFACE
  the preface
BODY
""", 'act')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<act xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="act">
  <preface>
    <p eId="preface__p_1">the preface</p>
  </preface>
  <body>
    <hcontainer eId="hcontainer_1" name="hcontainer">
      <content>
        <p eId="hcontainer_1__p_1"/>
      </content>
    </hcontainer>
  </body>
</act>
""", xml)

    def test_empty_preface_and_preamble(self):
        tree = self.parse("""
PREFACE
PREAMBLE
BODY
  test
""", 'act')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<act xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="act">
  <body>
    <hcontainer eId="hcontainer_1" name="hcontainer">
      <content>
        <p eId="hcontainer_1__p_1">test</p>
      </content>
    </hcontainer>
  </body>
</act>
""", xml)

    def test_num_hypen(self):
        tree = self.parse("""
PART

  SEC 1-
    no escape no heading

  SEC 1\-
    escape no heading

  SEC 1 \-
    escape no heading
    
  SEC 2\- - heading
    with heading
    
  SEC 2 \- - heading
    with heading
    
  SEC 3\- -
    empty heading
    
  SEC 3 \- -
    empty heading
    
  SEC 4\- 5
    escaped slash no heading
    
  SEC 4 \- 5
    escaped slash no heading
    
  SEC 5\- 6 - with - heading
    escaped slash with heading
    
  SEC 5 \- 6 - with - heading
    escaped slash with heading
    
  SEC \-6
    preceding slash
    
  SEC \- 6
    preceding slash
    
  SEC 6\-\-7
    multi
""", 'hier_element_block')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_nn_1">
  <section eId="part_nn_1__sec_1">
    <num>1-</num>
    <content>
      <p eId="part_nn_1__sec_1__p_1">no escape no heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_1_2">
    <num>1-</num>
    <content>
      <p eId="part_nn_1__sec_1_2__p_1">escape no heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_1_3">
    <num>1 -</num>
    <content>
      <p eId="part_nn_1__sec_1_3__p_1">escape no heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_2">
    <num>2-</num>
    <heading>heading</heading>
    <content>
      <p eId="part_nn_1__sec_2__p_1">with heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_2_2">
    <num>2 -</num>
    <heading>heading</heading>
    <content>
      <p eId="part_nn_1__sec_2_2__p_1">with heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_3">
    <num>3-</num>
    <content>
      <p eId="part_nn_1__sec_3__p_1">empty heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_3_2">
    <num>3 -</num>
    <content>
      <p eId="part_nn_1__sec_3_2__p_1">empty heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_4-5">
    <num>4- 5</num>
    <content>
      <p eId="part_nn_1__sec_4-5__p_1">escaped slash no heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_4-5_2">
    <num>4 - 5</num>
    <content>
      <p eId="part_nn_1__sec_4-5_2__p_1">escaped slash no heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_5-6">
    <num>5- 6</num>
    <heading>with - heading</heading>
    <content>
      <p eId="part_nn_1__sec_5-6__p_1">escaped slash with heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_5-6_2">
    <num>5 - 6</num>
    <heading>with - heading</heading>
    <content>
      <p eId="part_nn_1__sec_5-6_2__p_1">escaped slash with heading</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_6">
    <num>-6</num>
    <content>
      <p eId="part_nn_1__sec_6__p_1">preceding slash</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_6_2">
    <num>- 6</num>
    <content>
      <p eId="part_nn_1__sec_6_2__p_1">preceding slash</p>
    </content>
  </section>
  <section eId="part_nn_1__sec_6-7">
    <num>6--7</num>
    <content>
      <p eId="part_nn_1__sec_6-7__p_1">multi</p>
    </content>
  </section>
</part>
""", xml)
