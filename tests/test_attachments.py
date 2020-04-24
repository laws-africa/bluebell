from unittest import TestCase

from .support import ParserSupport


class ContainerTestCase(TestCase, ParserSupport):
    maxDiff = None

    def test_attachment(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text
""", 'attachment')
        self.assertEqual({
            'type': 'attachment',
            'name': 'annexure',
            'attribs': {'contains': 'originalVersion'},
            'heading': [{
                'type': 'text',
                'value': 'a heading',
            }],
            'subheading': [{
                'type': 'text',
                'value': 'subheading',
            }],
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some text',
                }]
            }]
        }, tree.to_dict())

    def test_multiple_attachments(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text
  
SCHEDULE heading

  schedule text
""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [{
                'type': 'attachment',
                'name': 'annexure',
                'attribs': {'contains': 'originalVersion'},
                'heading': [{
                    'type': 'text',
                    'value': 'a heading',
                }],
                'subheading': [{
                    'type': 'text',
                    'value': 'subheading',
                }],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'some text',
                    }]
                }]
            }, {
                'type': 'attachment',
                'name': 'schedule',
                'attribs': {'contains': 'originalVersion'},
                'heading': [{
                    'type': 'text',
                    'value': 'heading',
                }],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'schedule text',
                    }]
                }]
            }]
        }, tree.to_dict())
