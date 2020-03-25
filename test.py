#!/usr/bin/env python

import re
import json

from lxml.builder import E
from lxml import etree as ET

from hierarchicalStructure import parse, ParseError


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
                'name': self.hier_element_name.text,
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

    class Line:
        def to_dict(self):
            # TODO: document content and inline types
            return {
                'type': 'content',
                'name': 'p',
                'text': self.text,
            }


def pre_parse(lines):
    """ Pre-parse text, setting up indent and dedent markers.

    After calling this, the text is guaranteed not to have whitespace at the start
    of a line.
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
    def merge_blocks(item):
        """ blocks are just containers, merge adjacent ones together
        """
        prev = None
        kids = []
        for kid in item.get('children', []):
            merge_blocks(kid)

            if kid['type'] == 'block':
                if prev:
                    prev['children'].extend(kid['children'])
                else:
                    kids.append(kid)
                    prev = kid
            else:
                kids.append(kid)
                prev = None

        if 'children' in item:
            item['children'] = kids

    def to_akn(item):
        if item['type'] == 'hier':
            # if only hier elements, just add them
            if all(k['type'] == 'hier' for k in item['children']):
                kids = (to_akn(k) for k in item['children'])
                return E(item['name'].lower(), *(k for k in kids if k is not None))

            # if no hierarchy elements, use content and then just add them
            if all(k['type'] != 'hier' for k in item['children']):
                kids = (to_akn(k) for k in item['children'])
                return E(item['name'].lower(), E.content(*(k for k in kids if k is not None)))

            # if block/content at start and end, use intro and wrapup
            # TODO

            # otherwise, panic
            # TODO

        if item['type'] == 'block':
            kids = (to_akn(k) for k in item.get('children', []))
            return E(item['name'].lower(), *(k for k in kids if k is not None))

        if item['type'] == 'content':
            return E(item['name'].lower(), item['text'])

    merge_blocks(tree['body'])

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
    xml = make_akn(tree)

    print(json.dumps(tree))
    print(ET.tostring(xml, pretty_print=True, encoding='unicode'))
