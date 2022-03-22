from unittest import TestCase

from tests.support import ParserSupport


class BlocksTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_blocklist_simple(self):
        tree = self.parse("""
BLOCKLIST

  ITEM (a)

    item a

  ITEM (b)

    item b

""", 'block_list')
        self.assertEqual({
            'type': 'block',
            'name': 'blockList',
            'children': [{
                'name': 'item',
                'type': 'block',
                'num': '(a)',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item a',
                    }]
                }]
            }, {
                'name': 'item',
                'type': 'block',
                'num': '(b)',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item b',
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<blockList xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="list_1">
  <item eId="list_1__item_a">
    <num>(a)</num>
    <p eId="list_1__item_a__p_1">item a</p>
  </item>
  <item eId="list_1__item_b">
    <num>(b)</num>
    <p eId="list_1__item_b__p_1">item b</p>
  </item>
</blockList>
""", xml)

    def test_blocklist_intro_wrapup(self):
        tree = self.parse("""
BLOCKLIST

  some intro

  ITEM (a) - heading

    item a

  ITEM (b)
    SUBHEADING subheading

    item b

  and a wrap up
""", 'block_list')
        self.assertEqual({
            'type': 'block',
            'name': 'blockList',
            'children': [{
                'name': 'listIntroduction',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some intro',
                }]
            }, {
                'name': 'item',
                'type': 'block',
                'heading': [{'type': 'text', 'value': 'heading'}],
                'num': '(a)',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item a',
                    }]
                }]
            }, {
                'name': 'item',
                'type': 'block',
                'num': '(b)',
                'subheading': [{'type': 'text', 'value': 'subheading'}],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item b',
                    }]
                }]
            }, {
                'name': 'listWrapUp',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'and a wrap up',
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<blockList xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="list_1">
  <listIntroduction eId="list_1__intro_1">some intro</listIntroduction>
  <item eId="list_1__item_a">
    <num>(a)</num>
    <heading>heading</heading>
    <p eId="list_1__item_a__p_1">item a</p>
  </item>
  <item eId="list_1__item_b">
    <num>(b)</num>
    <subheading>subheading</subheading>
    <p eId="list_1__item_b__p_1">item b</p>
  </item>
  <listWrapUp eId="list_1__wrapup_1">and a wrap up</listWrapUp>
</blockList>
""", xml)

    def test_blocklist_nested(self):
        tree = self.parse("""
BLOCKLIST

  some intro

  ITEM (a)

    BLOCKLIST{foo bar}
    
      item a
    
      ITEM (i)
      
        item a(i)
        
      and a wrap up

  ITEM (b)

    item b
""", 'block_list')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<blockList xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="list_1">
  <listIntroduction eId="list_1__intro_1">some intro</listIntroduction>
  <item eId="list_1__item_a">
    <num>(a)</num>
    <blockList eId="list_1__item_a__list_1" foo="bar">
      <listIntroduction eId="list_1__item_a__list_1__intro_1">item a</listIntroduction>
      <item eId="list_1__item_a__list_1__item_i">
        <num>(i)</num>
        <p eId="list_1__item_a__list_1__item_i__p_1">item a(i)</p>
      </item>
      <listWrapUp eId="list_1__item_a__list_1__wrapup_1">and a wrap up</listWrapUp>
    </blockList>
  </item>
  <item eId="list_1__item_b">
    <num>(b)</num>
    <p eId="list_1__item_b__p_1">item b</p>
  </item>
</blockList>
""", xml)

    def test_blocklist_footnotes(self):
        tree = self.parse("""
BLOCKLIST

  some intro with {{FOOTNOTE 1}} and {{FOOTNOTE 2}}

  FOOTNOTE 1

    footnote 1

  FOOTNOTE 2

    footnote 2

  ITEM (a)

    item a

  wrap up with {{FOOTNOTE 3}} and {{FOOTNOTE 4}}

  FOOTNOTE 3

    footnote 3

  FOOTNOTE 4

    footnote 4
""", 'block_list')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<blockList xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="list_1">
  <listIntroduction eId="list_1__intro_1">some intro with <authorialNote eId="list_1__intro_1__authorialNote_1" marker="1" placement="bottom"><p eId="list_1__intro_1__authorialNote_1__p_1">footnote 1</p></authorialNote> and <authorialNote eId="list_1__intro_1__authorialNote_2" marker="2" placement="bottom"><p eId="list_1__intro_1__authorialNote_2__p_1">footnote 2</p></authorialNote></listIntroduction>
  <item eId="list_1__item_a">
    <num>(a)</num>
    <p eId="list_1__item_a__p_1">item a</p>
  </item>
  <listWrapUp eId="list_1__wrapup_1">wrap up with <authorialNote eId="list_1__wrapup_1__authorialNote_1" marker="3" placement="bottom"><p eId="list_1__wrapup_1__authorialNote_1__p_1">footnote 3</p></authorialNote> and <authorialNote eId="list_1__wrapup_1__authorialNote_2" marker="4" placement="bottom"><p eId="list_1__wrapup_1__authorialNote_2__p_1">footnote 4</p></authorialNote></listWrapUp>
</blockList>
""", xml)

    def test_blocklist_single_intro(self):
        tree = self.parse("""
PART A

  BLOCKLIST
  
    foo
    
    second intro line isn't allowed, so blocklist doesn't match at all

    ITEM a

      item a
""", 'hier_element_block')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <content>
    <p eId="part_A__p_1">BLOCKLIST</p>
    <p eId="part_A__p_2">foo</p>
    <p eId="part_A__p_3">second intro line isn't allowed, so blocklist doesn't match at all</p>
    <p eId="part_A__p_4">ITEM a</p>
    <p eId="part_A__p_5">item a</p>
  </content>
</part>
""", xml)

    def test_blocklist_single_wrapup(self):
        tree = self.parse("""
PART A

  BLOCKLIST

    ITEM a

      item a

    foo

    second wrapup line isn't allowed, so blocklist doesn't match at all
""", 'hier_element_block')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <content>
    <p eId="part_A__p_1">BLOCKLIST</p>
    <p eId="part_A__p_2">ITEM a</p>
    <p eId="part_A__p_3">item a</p>
    <p eId="part_A__p_4">foo</p>
    <p eId="part_A__p_5">second wrapup line isn't allowed, so blocklist doesn't match at all</p>
  </content>
</part>
""", xml)

    def test_blocklist_broken(self):
        tree = self.parse("""
BLOCKLIST

  ITEM (a)
""", 'block_list')
        self.assertEqual({
            'type': 'block',
            'name': 'blockList',
            'children': [{
                'name': 'item',
                'type': 'block',
                'num': '(a)',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': []
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<blockList xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="list_1">
  <item eId="list_1__item_a">
    <num>(a)</num>
    <p eId="list_1__item_a__p_1"/>
  </item>
</blockList>
""", xml)

    def test_explicit_p_tag(self):
        tree = self.parse("""
PART A

  P some text
  P{class foo bar} text with classes
  P{style text-align: center} text with style tag
""", 'hier_element_block')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <content>
    <p eId="part_A__p_1">some text</p>
    <p class="foo bar" eId="part_A__p_2">text with classes</p>
    <p eId="part_A__p_3" style="text-align: center">text with style tag</p>
  </content>
</part>
""", xml)

    def test_block_attrs(self):
        tree = self.parse("""
PART A

  P.baz{class foo bar} text with classes
  P{style text-align: center} text with style tag
  P..{style text-align: center} text with style tag and empty classes
  P..bar. text with empty classes
  P.foo text with a class
""", 'hier_element_block')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <content>
    <p class="foo bar baz" eId="part_A__p_1">text with classes</p>
    <p eId="part_A__p_2" style="text-align: center">text with style tag</p>
    <p eId="part_A__p_3" style="text-align: center">text with style tag and empty classes</p>
    <p class="bar" eId="part_A__p_4">text with empty classes</p>
    <p class="foo" eId="part_A__p_5">text with a class</p>
  </content>
</part>
""", xml)

    def test_block_attrs_unparse(self):
        xml = '''<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <content>
    <p a="b" class="one" foo="bar" baz="boom">text</p>
    <p class="one two three">text</p>
    <p a="b">text</p>
  </content>
</part>
'''
        actual = self.parser.unparse(xml)
        self.assertEqual('''PART A

  P.one{a b|foo bar|baz boom} text

  P.one.two.three text

  P{a b} text

''', actual)

    def test_longtitles(self):
        tree = self.parse("""
PART A

  LONGTITLE test

  LONGTITLE
""", 'hier_element_block')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <content>
    <longTitle eId="part_A__longTitle_1">
      <p eId="part_A__longTitle_1__p_1">test</p>
    </longTitle>
  </content>
</part>
""", xml)

    def test_crossheading(self):
        tree = self.parse("""
PART A

  CROSSHEADING test

  CROSSHEADING
""", 'hier_element_block')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <crossHeading eId="part_A__crossHeading_1">test</crossHeading>
</part>
""", xml)
