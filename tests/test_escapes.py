from unittest import TestCase

from lxml import etree
from .support import ParserSupport


class EscapesTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_ignore_escaped_blocks(self):
        # Remember, in the strings below a double backslash is actually a
        # single backslash because python requires us to backslash a backslash
        tree = self.parse("""
PART
  \\LONGTITLE
  \\SUBHEADING aoeu
  foo \\bar
  foo \\**bar**
  \\CROSSHEADING foo
  \\TABLE
  \\
  \\\\
  \\SECTION 1
""", 'hier_element_block')

        self.assertEqual({
            'name': 'part',
            'type': 'hier',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'LONGTITLE',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'SUBHEADING aoeu',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo bar',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo *',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': 'bar',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': '*',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'CROSSHEADING foo',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'TABLE',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': '\\'
                }],
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': '\\'
                }],
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'SECTION 1'
                }],
            }]
        }, tree.to_dict())

    def test_ignore_escaped_at_top_level(self):
        tree = self.parse("""
\\h\\e\\l\\lo
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
                            'value': 'hello'
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

    def test_ignore_escaped_inlines(self):
        # Remember, in the strings below a double backslash is actually a
        # single backslash because python requires us to backslash a backslash
        tree = self.parse("""
PART
  foo \\**bar**
  foo **bar\\**
  some \\{{^non-sup}}
  some {{^sup\\}}}
  a \\[[remark]]
  a [[remark\\]]
""", 'hier_element_block')

        self.assertEqual({
            'name': 'part',
            'type': 'hier',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo *',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': 'bar',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': '*',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo ',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': 'bar*',
                }, {
                    'type': 'text',
                    'value': '*',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some {',
                }, {
                    'type': 'text',
                    'value': '{',
                }, {
                    'type': 'text',
                    'value': '^non-sup}}',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some '
                }, {
                    'type': 'inline',
                    'name': 'sup',
                    'children': [{
                        'type': 'text',
                        'value': 'sup}'
                    }]
                }],
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'a ['
                }, {
                    'type': 'text',
                    'value': '['
                }, {
                    'type': 'text',
                    'value': 'remark]]'
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'a '
                }, {
                    'type': 'text',
                    'value': '['
                }, {
                    'type': 'text',
                    'value': '['
                }, {
                    'type': 'text',
                    'value': 'remark]]'
                }]
            }]
        }, tree.to_dict())
