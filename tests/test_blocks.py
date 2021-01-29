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