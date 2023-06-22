from unittest import TestCase

from lxml import etree

from tests.support import ParserSupport


class BulletListTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_bullets_simple(self):
        tree = self.parse("""
BULLETS
  * item 1
  *  item 2
  * item 3
""", 'bullet_list')
        self.assertEqual({
            'type': 'block',
            'name': 'ul',
            'children': [{
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item 1',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item 2',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item 3',
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<ul xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="ul_1">
  <li eId="ul_1__li_1">
    <p eId="ul_1__li_1__p_1">item 1</p>
  </li>
  <li eId="ul_1__li_2">
    <p eId="ul_1__li_2__p_1">item 2</p>
  </li>
  <li eId="ul_1__li_3">
    <p eId="ul_1__li_3__p_1">item 3</p>
  </li>
</ul>
""", xml)

    def test_bullets_with_attr(self):
        tree = self.parse("""
BULLETS{class spiffy}
  * item 1
  * item 2
""", 'bullet_list')
        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<ul xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" class="spiffy" eId="ul_1">
  <li eId="ul_1__li_1">
    <p eId="ul_1__li_1__p_1">item 1</p>
  </li>
  <li eId="ul_1__li_2">
    <p eId="ul_1__li_2__p_1">item 2</p>
  </li>
</ul>
""", xml)

    def test_ul_nested(self):
        tree = self.parse("""
BULLETS
  * item 1
  * item 2
    BULLETS
      * item 2a
      * item 2b
  * item 3
""", 'bullet_list')
        self.assertEqual({
            'type': 'block',
            'name': 'ul',
            'children': [{
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item 1',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item 2',
                    }]
                }, {
                    'type': 'block',
                    'name': 'ul',
                    'children': [{
                        'name': 'li',
                        'type': 'element',
                        'children': [{
                            'name': 'p',
                            'type': 'content',
                            'children': [{
                                'type': 'text',
                                'value': 'item 2a',
                            }]
                        }]
                    }, {
                        'name': 'li',
                        'type': 'element',
                        'children': [{
                            'name': 'p',
                            'type': 'content',
                            'children': [{
                                'type': 'text',
                                'value': 'item 2b',
                            }]
                        }]
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'item 3',
                    }]
                }]
            }, ]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<ul xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="ul_1">
  <li eId="ul_1__li_1">
    <p eId="ul_1__li_1__p_1">item 1</p>
  </li>
  <li eId="ul_1__li_2">
    <p eId="ul_1__li_2__p_1">item 2</p>
    <ul eId="ul_1__li_2__ul_1">
      <li eId="ul_1__li_2__ul_1__li_1">
        <p eId="ul_1__li_2__ul_1__li_1__p_1">item 2a</p>
      </li>
      <li eId="ul_1__li_2__ul_1__li_2">
        <p eId="ul_1__li_2__ul_1__li_2__p_1">item 2b</p>
      </li>
    </ul>
  </li>
  <li eId="ul_1__li_3">
    <p eId="ul_1__li_3__p_1">item 3</p>
  </li>
</ul>
""", xml)

    def test_mixed_items(self):
        tree = self.parse("""
BULLETS
  * bullet 1
  * bullet 2
    With multiple
    Lines
  *
  * an empty item (valid)
  *
    an item that starts empty
""", 'bullet_list')
        self.assertEqual({
            'type': 'block',
            'name': 'ul',
            'children': [{
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'bullet 1',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'bullet 2',
                    }]
                }, {
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'With multiple',
                    }]
                }, {
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'Lines',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': []
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'an empty item (valid)',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': []
                }, {
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'an item that starts empty',
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<ul xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="ul_1">
  <li eId="ul_1__li_1">
    <p eId="ul_1__li_1__p_1">bullet 1</p>
  </li>
  <li eId="ul_1__li_2">
    <p eId="ul_1__li_2__p_1">bullet 2</p>
    <p eId="ul_1__li_2__p_2">With multiple</p>
    <p eId="ul_1__li_2__p_3">Lines</p>
  </li>
  <li eId="ul_1__li_3">
    <p eId="ul_1__li_3__p_1"/>
  </li>
  <li eId="ul_1__li_4">
    <p eId="ul_1__li_4__p_1">an empty item (valid)</p>
  </li>
  <li eId="ul_1__li_5">
    <p eId="ul_1__li_5__p_1"/>
    <p eId="ul_1__li_5__p_2">an item that starts empty</p>
  </li>
</ul>
""", xml)

    def test_non_starred_items(self):
        tree = self.parse("""
BULLETS
  * bullet 1
    with multiple lines
  no star 1

  no star 2
    with indent
  * a star

  no star 3
""", 'bullet_list')
        self.assertEqual({
            'type': 'block',
            'name': 'ul',
            'children': [{
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'bullet 1',
                    }]
                }, {
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'with multiple lines',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'no star 1',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'no star 2',
                    }]
                }, {
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'with indent',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'a star',
                    }]
                }]
            }, {
                'name': 'li',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'no star 3',
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<ul xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="ul_1">
  <li eId="ul_1__li_1">
    <p eId="ul_1__li_1__p_1">bullet 1</p>
    <p eId="ul_1__li_1__p_2">with multiple lines</p>
  </li>
  <li eId="ul_1__li_2">
    <p eId="ul_1__li_2__p_1">no star 1</p>
  </li>
  <li eId="ul_1__li_3">
    <p eId="ul_1__li_3__p_1">no star 2</p>
    <p eId="ul_1__li_3__p_2">with indent</p>
  </li>
  <li eId="ul_1__li_4">
    <p eId="ul_1__li_4__p_1">a star</p>
  </li>
  <li eId="ul_1__li_5">
    <p eId="ul_1__li_5__p_1">no star 3</p>
  </li>
</ul>
""", xml)

    def test_bad_bullets_with_hier(self):
        tree = self.parse("""
  BULLETS

    PARA 24.

      SUBPARA i.

        Bar
""", 'judgment')

        self.assertEqual({
            'attribs': {'name': 'judgment'},
            'children': [
                {'name': 'header', 'type': 'element'},
                {'children': [{
                    'children': [{
                        'children': [{
                            'children': [{
                                'children': [{'type': 'text', 'value': 'PARA 24.'}],
                                'name': 'p',
                                'type': 'content'
                            }, {
                                'children': [{'type': 'text', 'value': 'SUBPARA i.'}],
                                'name': 'p',
                                'type': 'content'
                            }, {
                                'children': [{'type': 'text', 'value': 'Bar'}],
                                'name': 'p',
                                'type': 'content'
                            }],
                            'name': 'li',
                            'type': 'element'
                        }],
                        'name': 'ul',
                        'type': 'block'}
                    ],
                    'name': 'arguments',
                    'type': 'element'}
                ],
                    'name': 'judgmentBody',
                    'type': 'element'}],
            'name': 'judgment',
            'type': 'element'
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<judgment xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="judgment">
  <header/>
  <judgmentBody>
    <arguments>
      <ul eId="arguments__ul_1">
        <li eId="arguments__ul_1__li_1">
          <p eId="arguments__ul_1__li_1__p_1">PARA 24.</p>
          <p eId="arguments__ul_1__li_1__p_2">SUBPARA i.</p>
          <p eId="arguments__ul_1__li_1__p_3">Bar</p>
        </li>
      </ul>
    </arguments>
  </judgmentBody>
</judgment>
""", xml)
