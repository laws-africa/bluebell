from unittest import TestCase

from bluebell.akn import ParseError
from tests.support import ParserSupport


class SubflowsTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_quote(self):
        tree = self.parse("""
QUOTE

    some text
    
    BLOCKLIST
      ITEM (a)
        list item
    
    PART 1 - Heading
    
        part 1 text
""", 'block_quote')
        self.assertEqual({
            'type': 'element',
            'name': 'block',
            'attribs': {'name': 'quote'},
            'children': [{
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
                'type': 'element',
                'name': 'block',
                'attribs': {'name': 'quote'},
                'children': [{
                    'name': 'embeddedStructure',
                    'type': 'element',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'quoted',
                        }]
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
    BLOCKLIST
      ITEM (a)
        item
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
hello {{FOOTNOTE 9 9 }} there
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
hello {{FOOTNOTE }} there
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [
                {'type': 'text', 'value': 'hello '},
                {'type': 'text', 'value': '{'},
                {'type': 'text', 'value': '{'},
                {'type': 'text', 'value': 'FOOTNOTE }} there'},
            ],
        }, tree.to_dict())

        tree = self.parse("""
hello {{FOOTNOTE }} }} there
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [
                {'type': 'text', 'value': 'hello '},
                {'type': 'text', 'value': '{'},
                {'type': 'text', 'value': '{'},
                {'type': 'text', 'value': 'FOOTNOTE }} }} there'},
            ],
        }, tree.to_dict())

    def test_footnote_content_missing(self):
        tree = self.parse("""
hello {{FOOTNOTE 1}} there
""", 'line')

        xml = self.tostring(self.generator.to_xml(tree))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">hello <authorialNote eId="p_1__authorialNote_1" marker="1" placement="bottom"><p eId="p_1__authorialNote_1__p_1">(content missing)</p></authorialNote> there</p>
""", xml)

    def test_footnote_owner_missing(self):
        tree = self.parse("""
REMEDIES
some content

FOOTNOTE 99

  a footnote without a parent
""", 'remedies')

        xml = self.tostring(self.generator.to_xml(tree))

        self.assertEqual("""<remedies xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <p eId="remedies__p_1">some content</p>
  <p eId="remedies__p_2">FOOTNOTE 99</p>
  <p eId="remedies__p_3">a footnote without a parent</p>
</remedies>
""", xml)

    def test_footnote_xml(self):
        tree = self.parse("""
PART 1
  this section [{{FOOTNOTE 1}}] uses a footnote.
  
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

        xml = self.tostring(self.generator.to_xml(tree))

        self.assertEqual("""<part xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="part_1">
  <num>1</num>
  <content>
    <p eId="part_1__p_1">this section [<authorialNote eId="part_1__p_1__authorialNote_1" marker="1" placement="bottom"><p eId="part_1__p_1__authorialNote_1__p_1">which isn't very interesting</p></authorialNote>] uses a footnote.</p>
    <p eId="part_1__p_2">FOOTNOTE 2</p>
    <p eId="part_1__p_3">which is not used</p>
  </content>
</part>
""", xml)

    def test_duplicate_footnotes(self):
        tree = self.parse("""
PREAMBLE

First reference to the Sustainable Development Goals,{{^{{FOOTNOTE 1}}}}

FOOTNOTE 1

  General Assembly resolution 70/1, annex.

Second reference to the Sustainable Development Goals, with repeated reference and identical footnote text,{{^{{FOOTNOTE 1}}}}

FOOTNOTE 1

  General Assembly resolution 70/1, annex.

""", 'preamble')

        xml = self.tostring(self.generator.to_xml(tree))

        self.assertEqual("""<preamble xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <p eId="preamble__p_1">First reference to the Sustainable Development Goals,<sup><authorialNote eId="preamble__p_1__authorialNote_1" marker="1" placement="bottom"><p eId="preamble__p_1__authorialNote_1__p_1">General Assembly resolution 70/1, annex.</p></authorialNote></sup></p>
  <p eId="preamble__p_2">Second reference to the Sustainable Development Goals, with repeated reference and identical footnote text,<sup><authorialNote eId="preamble__p_2__authorialNote_1" marker="1" placement="bottom"><p eId="preamble__p_2__authorialNote_1__p_1">General Assembly resolution 70/1, annex.</p></authorialNote></sup></p>
</preamble>
""", xml)

        text = self.parser.unparse(xml)
        self.assertEqual("""PREAMBLE

  First reference to the Sustainable Development Goals,{{^{{FOOTNOTE 1}}}}

  FOOTNOTE 1
    General Assembly resolution 70/1, annex.

  Second reference to the Sustainable Development Goals, with repeated reference and identical footnote text,{{^{{FOOTNOTE 1}}}}

  FOOTNOTE 1
    General Assembly resolution 70/1, annex.

""", text)

    def test_nested_quotes(self):
        tree = self.parse("""
QUOTE

  line one
  
  QUOTE
  
    line two
""", 'block_quote')
        self.assertEqual({
            'type': 'element',
            'name': 'block',
            'attribs': {'name': 'quote'},
            'children': [{
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
                    'type': 'element',
                    'name': 'block',
                    'attribs': {'name': 'quote'},
                    'children': [{
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
                }]
            }]
        }, tree.to_dict())

    def test_quote_with_attrs(self):
        tree = self.parse("""
QUOTE{startQuote "}

  line one
""", 'block_quote')
        self.assertEqual({
            'type': 'element',
            'name': 'block',
            'attribs': {'name': 'quote'},
            'children': [{
                'name': 'embeddedStructure',
                'type': 'element',
                'attribs': {'startQuote': '"'},
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'line one',
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.generator.to_xml(tree))

        self.assertEqual("""<block xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="block_1" name="quote">
  <embeddedStructure eId="block_1__embeddedStructure_1" startQuote="&quot;">
    <p eId="block_1__embeddedStructure_1__p_1">line one</p>
  </embeddedStructure>
</block>
""", xml)

    def test_quote_curlies(self):
        # shouldn't be able to parse this double opening curlies, since
        # an attribute name can't start with {
        with self.assertRaises(ParseError):
            tree = self.parse("""
    QUOTE{{startQuote "}
        some text
    """, 'block_quote')

        # shouldn't be able to parse this double opening curlies, since
        # an attribute name can't start with }
        with self.assertRaises(ParseError):
            tree = self.parse("""
    QUOTE{}startQuote "}
        some text
    """, 'block_quote')

    def test_quote_unparsed(self):
        # quotes should be correctly indented when unparsed
        xml = '''<block xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="block_1" name="quote"><embeddedStructure eId="block_1__embeddedStructure_1" startQuote="&quot;"><p eId="block_1__embeddedStructure_1__p_1">line one</p></embeddedStructure></block>
'''
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''QUOTE{startQuote "}
  line one

''', unparsed)
