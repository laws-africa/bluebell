#!/usr/bin/env python

import re
import json
import sys

from lxml.builder import E
from lxml import etree as ET

from hierarchicalStructure import parse, ParseError

# TODO: block lists
# TODO: nested block lists
# TODO: arbitrary indents
# TODO: schedules and annexures - how to "push" to end?
# TODO: tables


def hoist_blocks(children):
    """ Block elements can use this to pull grandchildren of anonymous block
        elements into their child list.

        So this:
            block -> block -> block
        becomes:
            block -> block
    """
    kids = []

    for kid in children:
        if kid['type'] == 'block' and kid['name'] == 'block':
            kids.extend(c for c in kid.get('children', []))
        else:
            kids.append(kid)

    return kids


class Types:
    # ------------------------------------------------------------------------------
    # Judgement
    # ------------------------------------------------------------------------------

    class Judgement:
        def to_dict(self):
            return {
                'type': 'wrapper',
                'name': 'judgmentBody',
                'children': [c.to_dict() for c in self.judgment_body if c.text],
            }

    class Introduction:
        def to_dict(self):
            return {
                'type': 'wrapper',
                'name': 'introduction',
                'children': [c.block_element.to_dict() for c in self.content],
            }

    class Background:
        def to_dict(self):
            return {
                'type': 'wrapper',
                'name': 'background',
                'children': [c.block_element.to_dict() for c in self.content],
            }

    class Arguments:
        def to_dict(self):
            return {
                'type': 'wrapper',
                'name': 'arguments',
                'children': [c.block_element.to_dict() for c in self.content],
            }

    class Remedies:
        def to_dict(self):
            return {
                'type': 'wrapper',
                'name': 'remedies',
                'children': [c.block_element.to_dict() for c in self.content],
            }

    class Motivation:
        def to_dict(self):
            return {
                'type': 'wrapper',
                'name': 'motivation',
                'children': [c.block_element.to_dict() for c in self.content],
            }

    class Decision:
        def to_dict(self):
            return {
                'type': 'wrapper',
                'name': 'decision',
                'children': [c.to_dict() for c in self.content],
            }

    # ------------------------------------------------------------------------------
    # Hierarchical structures (act, bill)
    # ------------------------------------------------------------------------------

    class HierarchicalStructure:
        def to_dict(self):
            info = {
                'type': 'hierarchicalStructure',
                'body': self.body.to_dict(),
            }
            if self.preface.text:
                info['preface'] = self.preface.to_dict()

            return info

    class Preface:
        def to_dict(self):
            return {
                'type': 'preface',
                'children': [c.preface_block_element.to_dict() for c in self.content]
            }

    class Longtitle:
        def to_dict(self):
            return {
                'type': 'content',
                'name': 'longtitle',
                'children': Types.Inline.many_to_dict(k for k in self.content)
            }

    class Body:
        def to_dict(self):
            return {
                'type': 'hier',
                'name': 'body',
                'children': [c.to_dict() for c in self.content]
            }

    class HierElement:
        def to_dict(self):
            info = {
                'type': 'hier',
                'name': self.hier_element_name.text.lower(),
                'children': [c.elements[1].to_dict() for c in self.content]
            }

            if self.heading.text:
                num = self.heading.num.text.strip()
                if num:
                    info['num'] = num

                heading = self.heading.heading_to_dict()
                if heading:
                    info['heading'] = heading

            if self.subheading.text:
                info['subheading'] = self.subheading.to_dict()

            return info

    class HierElementHeading:
        def heading_to_dict(self):
            if hasattr(self.heading, 'content') and self.heading.content.text.strip():
                return Types.Inline.many_to_dict(x for x in self.heading.content)

    class Heading:
        def to_dict(self):
            return Types.Inline.many_to_dict(k for k in self.content)

    class Block:
        def to_dict(self):
            # if we have one child, it's a block element and we're only a wrapper,
            # return it directly
            if len(self.content.elements) == 1:
                return self.content.elements[0].to_dict()

            # TODO: name and attribs for arbitrary indented block
            return {
                'type': 'block',
                # TODO: name? the block is essentially anonymous?
                # what about arbitrary indented text?
                'name': 'block',
                'children': [c.to_dict() for c in self.content]
            }

    class BlockList:
        def to_dict(self):
            return {
                'type': 'block',
                'name': 'blockList',
                'children': [c.to_dict() for c in self],
            }

    class BlockItem:
        def to_dict(self):
            kids = []

            # preamble content on the same line as the number
            if self.preamble.text and hasattr(self.preamble, 'block_element'):
                kids.append(self.preamble.block_element)

            # nested blocks
            if self.content.text:
                kids.extend(self.content.content)

            return {
                'type': 'block',
                'name': 'item',
                'num': self.num.text,
                'children': [c.to_dict() for c in kids],
            }

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
                'children': Types.Inline.many_to_dict(self.content.elements),
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
    3. no trailing whitespace at the end of a line
    """
    indent = '\x0E'
    dedent = '\x0F'
    indent = '{'
    dedent = '}'

    line_re = re.compile(r'^([ ]*)([^ \n])', re.M)
    trailing_ws_re = re.compile(r' +$', re.M)

    # tabs are two spaces
    lines = lines.replace('\t', '  ')
    # strip trailing whitespace
    lines = trailing_ws_re.sub('', lines)

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


def make_akn(tree, root):
    def kids_to_akn(parent=None, kids=None):
        if kids is None:
            kids = parent.get('children', [])
        return [to_akn(k) for k in kids]

    def to_akn(item):
        if item['type'] == 'preface':
            # preface is already a block, so hoist in any block children
            kids = hoist_blocks(item.get('children', []))
            return E('preface', *kids_to_akn(kids=kids))

        if item['type'] == 'hier':
            pre = []
            kids = kids_to_akn(item)

            # by default, if all children are hier elements, we add them as-is
            # if no hierarchy children (ie. all block/content), wrap children in <content>
            if all(k['type'] != 'hier' for k in item['children']):
                kids = [E.content(*kids)]

            if item.get('num'):
                pre.append(E.num(item['num']))

            if item.get('heading'):
                pre.append(E.heading(*(to_akn(k) for k in item['heading'])))

            if item.get('subheading'):
                pre.append(E.subheading(*(to_akn(k) for k in item['subheading'])))

            kids = pre + kids

            return E(item['name'], *kids, **item.get('attribs', {}))

            # if block/content at start and end, use intro and wrapup
            # TODO

            # otherwise, panic
            # TODO

        if item['type'] == 'block':
            # TODO: can have num, heading, subheading
            # TODO: make this generic? what else can have num?
            kids = kids_to_akn(item)
            if 'num' in item:
                kids.insert(0, E('num', item['num']))
            return E(item['name'], *kids)

        if item['type'] == 'content':
            return E(item['name'], *kids_to_akn(item))

        if item['type'] == 'inline':
            return E(item['name'], *kids_to_akn(item), **item.get('attribs', {}))

        if item['type'] == 'marker':
            return E(item['name'], **item.get('attribs', {}))

        if item['type'] == 'text':
            return item['value']

        if item['type'] == 'wrapper':
            return E(item['name'], *kids_to_akn(item))

        # TODO: host blocks for background, introduction, etc.

    items = []

    # TODO: handle different top-level elements
    if root == 'hierarchical_structure':
        if 'preface' in tree:
            items.append(to_akn(tree['preface']))
        items.append(to_akn(tree['body']))
        return E('act', *items)

    elif root == 'judgment':
        return to_akn(tree)


def print_with_lines(lines):
    for i, line in enumerate(lines.split('\n')):
        i = i + 1
        print(f'{i:02}: {line}', file=sys.stderr)


def parse_with_failure(lines, root):
    """ Helper function to do the actual parsing with an arbitrary root.
    """
    from hierarchicalStructure import Parser, FAILURE, ParseError, format_error

    parser = Parser(lines, actions=None, types=Types)
    tree = getattr(parser, f'_read_{root}')()
    if tree is not FAILURE and parser._offset == parser._input_size:
        return tree
    if not parser._expected:
        parser._failure = parser._offset
        parser._expected.append('<EOF>')
    raise ParseError(format_error(parser._input, parser._failure, parser._expected))

if __name__ == '__main__':
    root = sys.argv[1]
    lines = open(sys.argv[2], "r").read()

    lines = pre_parse(lines)
    try:
        tree = parse_with_failure(lines, root)
    except ParseError as e:
        print_with_lines(lines)
        raise

    tree = tree.to_dict()
    print(json.dumps(tree))

    xml = make_akn(tree, root)
    print(ET.tostring(xml, pretty_print=True, encoding='unicode'))
