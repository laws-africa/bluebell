from unittest import TestCase

from .support import ParserSupport


class ContainerTestCase(TestCase, ParserSupport):
    maxDiff = None

    def test_preamble_simple(self):
        tree = self.parse("""
PREAMBLE

some preamble text
""", 'preamble')
        self.assertEqual({
            'name': 'preamble',
            'type': 'element',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some preamble text',
                }]
            }]
        }, tree.to_dict())

    def test_preamble_mixed_indent(self):
        tree = self.parse("""
PREAMBLE

not indented

    indented
""", 'preamble')
        self.assertEqual({
            'name': 'preamble',
            'type': 'element',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'not indented',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'indented',
                }]
            }]
        }, tree.to_dict())

    def test_preamble_mixed_indent_starts_indented(self):
        tree = self.parse("""
PREAMBLE

    not indented

indented
""", 'preamble')
        self.assertEqual({
            'name': 'preamble',
            'type': 'element',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'not indented',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'indented',
                }]
            }]
        }, tree.to_dict())

    def test_conclusions_hier_ignored(self):
        # conclusions can't contain hier elements
        tree = self.parse("""
CONCLUSIONS

    PART 1
    
    text
    
    (a) item a
""", 'conclusions')
        self.assertEqual({
            'name': 'conclusions',
            'type': 'element',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'PART 1',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'text',
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
                            'value': 'item a',
                        }]
                    }],
                }],
            }],
        }, tree.to_dict())
