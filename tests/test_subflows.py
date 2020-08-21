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

    def test_footnote_content_missing(self):
        tree = self.parse("""
hello ++FOOTNOTE 1++ there
""", 'line')

        xml = etree.tostring(self.generator.to_xml(tree), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">hello <authorialNote marker="1" placement="bottom" eId="authorialNote_1"><p>(content missing)</p></authorialNote> there</p>
""", xml)

    def test_footnote_owner_missing(self):
        tree = self.parse("""
REMEDIES
some content

FOOTNOTE 99

  a footnote without a parent
""", 'remedies')

        xml = etree.tostring(self.generator.to_xml(tree), encoding='unicode', pretty_print=True)

        self.assertEqual("""<remedies xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <p>some content</p>
  <p>FOOTNOTE 99</p>
  <p>a footnote without a parent</p>
</remedies>
""", xml)

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

        xml = etree.tostring(self.generator.to_xml(tree), encoding='unicode', pretty_print=True)

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_1">
  <num>1</num>
  <content>
    <p>this section [<authorialNote marker="1" placement="bottom" eId="part_1__authorialNote_1"><p>which isn't very interesting</p></authorialNote>] uses a footnote.</p>
    <p>FOOTNOTE 2</p>
    <p>which is not used</p>
  </content>
</part>
""", xml)

    def test_duplicate_footnotes(self):
        tree = self.parse("""
PREAMBLE

First reference to the Sustainable Development Goals,^^++FOOTNOTE 1++^^

FOOTNOTE 1

  General Assembly resolution 70/1, annex.

Second reference to the Sustainable Development Goals, with repeated reference and identical footnote text,^^++FOOTNOTE 1++^^

FOOTNOTE 1

  General Assembly resolution 70/1, annex.

""", 'preamble')

        xml = etree.tostring(self.generator.to_xml(tree), encoding='unicode', pretty_print=True)

        self.assertEqual("""<preamble xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <p>First reference to the Sustainable Development Goals,<sup><authorialNote marker="1" placement="bottom" eId="preamble__authorialNote_1"><p>General Assembly resolution 70/1, annex.</p></authorialNote></sup></p>
  <p>Second reference to the Sustainable Development Goals, with repeated reference and identical footnote text,<sup><authorialNote marker="1" placement="bottom" eId="preamble__authorialNote_2"><p>General Assembly resolution 70/1, annex.</p></authorialNote></sup></p>
</preamble>
""", xml)

        text = self.parser.unparse(xml)
        self.assertEqual("""PREAMBLE

  First reference to the Sustainable Development Goals,^^++FOOTNOTE 1++^^

  FOOTNOTE 1

    General Assembly resolution 70/1, annex.

  Second reference to the Sustainable Development Goals, with repeated reference and identical footnote text,^^++FOOTNOTE 1++^^

  FOOTNOTE 1

    General Assembly resolution 70/1, annex.

""", text)

    def test_nested_quotes(self):
        tree = self.parse("""
QUOTE

  line one
  
  QUOTE
  
    line two
""", 'embedded_structure')
        self.assertEqual({
            'name': 'embeddedStructure',
            'type': 'element',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'line one',
                }]
            }, {
                'name': 'embeddedStructure',
                'type': 'element',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'line two',
                    }]
                }]
            }]
        }, tree.to_dict())
