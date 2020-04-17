import re

from lxml.builder import E

from .akn import Parser, FAILURE, ParseError, format_error
import bluebell.types as types


INDENT = '\x0E'
DEDENT = '\x0F'


def pre_parse(lines, indent=INDENT, dedent=DEDENT):
    """ Pre-parse text, setting up indent and dedent markers.

    After calling this, the following are guaranteed:

    1. no whitespace at the start of a line
    2. no tab characters
    3. no trailing whitespace at the end of a line

    The indent and dedent parameters are the symbols the grammar
    uses to indicate indented and dedented blocks.
    """
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
                    if level >= stack[-1]:
                        break
                    stack.pop()

                return s + match.group(2)

    lines = line_re.sub(handle_indent, lines)

    if stack:
        lines += (dedent + "\n") * (len(stack) - 1)

    return lines


def parse_with_failure(lines, root):
    """ Helper function to do the actual parsing with an arbitrary root.
    """
    parser = Parser(lines, actions=None, types=types)
    tree = getattr(parser, f'_read_{root}')()
    if tree is not FAILURE and parser._offset == parser._input_size:
        return tree
    if not parser._expected:
        parser._failure = parser._offset
        parser._expected.append('<EOF>')
    raise ParseError(format_error(parser._input, parser._failure, parser._expected))

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

        if item['type'] == 'element':
            return E(item['name'], *kids_to_akn(item))

    items = []

    # TODO: handle different top-level elements
    if root == 'hierarchical_structure':
        if 'preface' in tree:
            items.append(to_akn(tree['preface']))
        items.append(to_akn(tree['body']))
        return E('act', *items)

    elif root == 'judgment':
        return to_akn(tree)
