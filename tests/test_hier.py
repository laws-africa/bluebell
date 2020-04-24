from unittest import TestCase

from .support import ParserSupport


class HierTestCase(TestCase, ParserSupport):
    maxDiff = None

    def test_hier_with_block_lists(self):
        tree = self.parse("""
PART

  (a) item a

    indent

      indent
""", 'hier_element_block')
        self.assertEqual({
            'name': 'part',
            'type': 'hier',
            'children': [{
                'type': 'block',
                'name': 'blockList',
                'children': [{
                    'type': 'block',
                    'name': 'item',
                    'num': '(a)',
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'item a',
                        }],
                    }, {
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'indent',
                        }],
                    }, {
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'indent',
                        }],
                    }]
                }]
            }]
        }, tree.to_dict())

    def test_hier_nested_indents(self):
        tree = self.parse("""
PART

  indent
  
    indent
      
      indent
""", 'hier_element_block')
        self.assertEqual({
            'name': 'part',
            'type': 'hier',
            'children': [{
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'indent',
                }],
            }, {
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'indent',
                }],
            }, {
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'indent',
                }],
            }]
        }, tree.to_dict())
