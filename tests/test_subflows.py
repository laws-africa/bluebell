from unittest import TestCase

from lxml import etree
from tests.support import ParserSupport


class SubflowsTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_quote(self):
        tree = self.parse("""
QUOTE

    some text
    
    (a) list item
    
    PART 1 - Heading
    
        part 1 text
""", 'embedded_structure')
        self.assertEqual({
            'name': 'embeddedStructure',
            'type': 'element',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some text',
                }]
            }, {
                'name': 'blockList',
                'type': 'block',
                'children': [{
                    'type': 'block',
                    'name': 'item',
                    'num': '(a)',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'list item',
                        }]
                    }]
                }]
            }, {
                'name': 'part',
                'type': 'hier',
                'num': '1',
                'heading': [{
                    'type': 'text',
                    'value': 'Heading',
                }],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'part 1 text',
                    }]
                }]
            }]
        }, tree.to_dict())

    def test_quote_in_block(self):
        tree = self.parse("""
INTRODUCTION

some text

QUOTE

  quoted
    
something else
""", 'introduction')
        self.assertEqual({
            'type': 'element',
            'name': 'introduction',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some text',
                }]
            }, {
                'name': 'embeddedStructure',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'quoted',
                    }]
                }],
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'something else',
                }]
            }],
        }, tree.to_dict())

    def test_footnote_content(self):
        tree = self.parse("""
FOOTNOTE 99a
  some text
  PART 1
    (a) item
""", 'footnote')

        self.assertEqual({
            'type': 'element',
            'name': 'displaced',
            'attribs': {'marker': '99a', 'name': 'footnote'},
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some text'
                }],
            }, {
                'type': 'hier',
                'name': 'part',
                'num': '1',
                'children': [{
                    'name': 'blockList',
                    'type': 'block',
                    'children': [{
                        'type': 'block',
                        'name': 'item',
                        'num': '(a)',
                        'children': [{
                            'name': 'p',
                            'type': 'content',
                            'children': [{
                                'type': 'text',
                                'value': 'item',
                            }]
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

    def test_footnote_marker(self):
        tree = self.parse("""
hello ++FOOTNOTE 9 9 ++ there
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [{
                'type': 'text',
                'value': 'hello '
            }, {
                'type': 'element',
                'name': 'authorialNote',
                'attribs': {
                    'marker': '9 9',
                    'placement': 'bottom',
                    'displaced': 'footnote',
                },
            }, {
                'type': 'text',
                'value': ' there'
            }],
        }, tree.to_dict())

    def test_footnote_marker_incomplete(self):
        tree = self.parse("""
hello ++FOOTNOTE ++ there
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [{
                'type': 'text',
                'value': 'hello ++FOOTNOTE ++ there'
            }],
        }, tree.to_dict())

        tree = self.parse("""
hello ++FOOTNOTE ++ ++ there
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [{
                'type': 'text',
                'value': 'hello ++FOOTNOTE ++ ++ there'
            }],
        }, tree.to_dict())

    def test_footnote_xml(self):
        tree = self.parse("""
PART 1
  this section [++FOOTNOTE 1++] uses a footnote.
  
  FOOTNOTE 1
  
    which isn't very interesting
 
  FOOTNOTE 2
  
    which is not used
""", 'hier_element')

        self.assertEqual({
            'type': 'hier',
            'name': 'part',
            'num': '1',
            'children': [{
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'this section [',
                }, {
                    'type': 'element',
                    'name': 'authorialNote',
                    'attribs': {
                        'placement': 'bottom',
                        'displaced': 'footnote',
                        'marker': '1',
                    },
                }, {
                    'type': 'text',
                    'value': '] uses a footnote.',
                }]
            }, {
                'type': 'element',
                'name': 'displaced',
                'attribs': {'marker': '1', 'name': 'footnote'},
                'children': [{
                    'type': 'content',
                    'name': 'p',
                    'children': [{
                        'type': 'text',
                        'value': "which isn't very interesting",
                    }]
                }]
            }, {
                'type': 'element',
                'name': 'displaced',
                'attribs': {'marker': '2', 'name': 'footnote'},
                'children': [{
                    'type': 'content',
                    'name': 'p',
                    'children': [{
                        'type': 'text',
                        'value': "which is not used",
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(self.generator.xml_from_tree(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_1">
  <num>1</num>
  <content>
    <p>this section [<authorialNote marker="1" placement="bottom" eId="part_1__authorialNote_1"><p>which isn't very interesting</p></authorialNote>] uses a footnote.</p>
  </content>
</part>
""", xml)

