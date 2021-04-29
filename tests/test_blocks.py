from unittest import TestCase

from lxml import etree

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

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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
        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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
        xml = etree.tostring(self.generator.xml_from_dict(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<blockList xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="list_1">
  <listIntroduction eId="list_1__intro_1">some intro with <authorialNote marker="1" placement="bottom" eId="list_1__intro_1__authorialNote_1"><p eId="list_1__intro_1__authorialNote_1__p_1">footnote 1</p></authorialNote> and <authorialNote marker="2" placement="bottom" eId="list_1__intro_1__authorialNote_2"><p eId="list_1__intro_1__authorialNote_2__p_1">footnote 2</p></authorialNote></listIntroduction>
  <item eId="list_1__item_a">
    <num>(a)</num>
    <p eId="list_1__item_a__p_1">item a</p>
  </item>
  <listWrapUp eId="list_1__wrapup_1">wrap up with <authorialNote marker="3" placement="bottom" eId="list_1__wrapup_1__authorialNote_1"><p eId="list_1__wrapup_1__authorialNote_1__p_1">footnote 3</p></authorialNote> and <authorialNote marker="4" placement="bottom" eId="list_1__wrapup_1__authorialNote_2"><p eId="list_1__wrapup_1__authorialNote_2__p_1">footnote 4</p></authorialNote></listWrapUp>
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
        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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
        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

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
        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_A">
  <num>A</num>
  <content>
    <p eId="part_A__p_1">some text</p>
    <p eId="part_A__p_2" class="foo bar">text with classes</p>
    <p eId="part_A__p_3" style="text-align: center">text with style tag</p>
  </content>
</part>
""", xml)
