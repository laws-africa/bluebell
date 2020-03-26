#!/usr/bin/env python

import re
import json

from lxml.builder import E
from lxml import etree as ET

from hierarchicalStructure import parse, ParseError

# TODO: heading
# TODO: num
# TODO: block lists
# TODO: nested block lists
# TODO: arbitrary indents
# TODO: schedules
# TODO: tables
# TODO: inlines (b, i, etc.)
# TODO: markers (img, eol)


class Types:
    class Root:
        def to_dict(self):
            return {
                'type': 'hierarchicalStructure',
                'body': self.body.to_dict(),
            }

    class Body:
        def to_dict(self):
            return {
                'type': 'hier',
                'name': 'body',
                'children': [c.to_dict() for c in self]
            }

    class HierElement:
        def to_dict(self):
            if hasattr(self.hier_element_num, 'num'):
                num = self.hier_element_num.num.text
            else:
                num = None

            return {
                'type': 'hier',
                'name': self.hier_element_name.text.lower(),
                'num': num,
                'children': [c.to_dict() for c in self.children]
            }

    class Block:
        def to_dict(self):
            return self.content.to_dict()

    class Table:
        def to_dict(self):
            return {
                'type': 'block',
                'name': 'table',
            }

    # TODO: document content and inline types
    class Line:
        def to_dict(self):
            return {
                'type': 'content',
                'name': 'p',
                'children': Types.Inline.many_to_dict(self.elements),
            }

    class Ref:
        def to_dict(self):
            return {
                'type': 'inline',
                'name': 'ref',
                'attribs': {
                    'href': self.href.text,
                },
                'children': [{
                    'type': 'text',
                    'value': self.content.text,
                }],
            }

    class Remark:
        def to_dict(self):
            return {
                'type': 'inline',
                'name': 'remark',
                'attribs': {'status': 'editorial'},
                'children': Types.Inline.many_to_dict(x.inline for x in self.content.elements),
            }

    class Image:
        def to_dict(self):
            attribs = {'src': self.href.text}
            if self.content.text:
                attribs['alt'] = self.content.text

            return {
                'type': 'marker',
                'name': 'img',
                'attribs': attribs,
            }

    class Bold:
        def to_dict(self):
            return {
                'type': 'inline',
                'name': 'b',
                'children': Types.Inline.many_to_dict(x.inline for x in self.content.elements),
            }

    class Italics:
        def to_dict(self):
            return {
                'type': 'inline',
                'name': 'i',
                'children': Types.Inline.many_to_dict(x.inline for x in self.content.elements),
            }

    class Inline:
        @classmethod
        def many_to_dict(cls, items):
            """ Convert adjacent inline items, merging consecutive single characters.
            """
            merged = []
            text = []

            for item in items:
                if not hasattr(item, 'to_dict'):
                    text.append(item.text)

                else:
                    if text:
                        merged.append({
                            'type': 'text',
                            'value': ''.join(text),
                        })
                        text = []
                    merged.append(item.to_dict())

            if text:
                merged.append({
                    'type': 'text',
                    'value': ''.join(text),
                })

            return merged


def pre_parse(lines):
    """ Pre-parse text, setting up indent and dedent markers.

    After calling this, the following are guaranteed:

    1. no whitespace at the start of a line
    2. no tab characters
    """
    indent = '\x0E'
    dedent = '\x0F'
    indent = '{'
    dedent = '}'

    line_re = re.compile(r'^([ ]*)([^ \n])', re.M)

    # tabs are two spaces
    lines = lines.replace('\t', '  ')
    stack = [-1]

    def handle_indent(match):
        level = len(match.group(1)) / 2

        if level == stack[-1]:
            # same level, no change
            return match.group(2)

        elif level > stack[-1]:
            # indent
            stack.append(level)
            return indent + "\n" + match.group(2)

        else:
            # dedent
            stack.pop()

            if level > stack[-1]:
                # we were over-indented previously
                stack.append(level)
                return match.group(2)

            else:
                # dedent until we're back to the previous level
                s = ""
                while True:
                    s += dedent + "\n"
                    if level <= stack[-1]:
                        break
                    stack.pop()

                return s + match.group(2)

    lines = line_re.sub(handle_indent, lines)

    if stack:
        lines += (dedent + "\n") * (len(stack) - 1)

    return lines


def make_akn(tree):
    def to_akn(item):
        kids = (to_akn(k) for k in item.get('children', []))

        if item['type'] == 'hier':
            # by default, if all children are hier elements, we add them as-is

            # if no hierarchy children (ie. all block/content), wrap children in <content>
            if all(k['type'] != 'hier' for k in item['children']):
                kids = [E.content(*kids)]

            return E(item['name'], E.content(*kids), **item.get('attribs', {}))

            # if block/content at start and end, use intro and wrapup
            # TODO

            # otherwise, panic
            # TODO

        if item['type'] == 'block':
            return E(item['name'], *kids)

        if item['type'] == 'content':
            return E(item['name'], *kids)

        if item['type'] == 'inline':
            return E(item['name'], *kids, **item.get('attribs', {}))

        if item['type'] == 'marker':
            return E(item['name'], **item.get('attribs', {}))

        if item['type'] == 'text':
            return item['value']

    return to_akn(tree['body'])


def print_with_lines(lines):
    for i, line in enumerate(lines.split('\n')):
        i = i + 1
        print(f'{i:02}: {line}')


if __name__ == '__main__':
    lines = open("test.txt", "r").read()

    lines = pre_parse(lines)
    try:
        tree = parse(lines, types=Types)
    except ParseError as e:
        print_with_lines(lines)
        raise

    tree = tree.to_dict()
    print(json.dumps(tree))

    xml = make_akn(tree)
    print(ET.tostring(xml, pretty_print=True, encoding='unicode'))
