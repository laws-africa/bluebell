from unittest import TestCase

from .support import ParserSupport


class SubflowsTestCase(TestCase, ParserSupport):
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
some text

QUOTE

  quoted
    
something else
""", 'block', block=True)
        self.assertEqual({
            'name': 'block',
            'type': 'block',
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
