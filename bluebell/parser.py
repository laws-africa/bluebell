import re

from .akn import Parser, FAILURE, ParseError, format_error
import bluebell.types as types
import bluebell.xml as xml


INDENT = '\x0E'
DEDENT = '\x0F'


def pre_parse(text, indent=INDENT, dedent=DEDENT):
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
    text = text.replace('\t', '  ')
    # strip trailing whitespace
    text = trailing_ws_re.sub('', text)

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

    text = line_re.sub(handle_indent, text)

    if stack:
        text += (dedent + "\n") * (len(stack) - 1)

    return text


def parse_with_failure(text, root):
    """ Helper function to do the actual parsing with an arbitrary root.
    """
    parser = Parser(text, actions=None, types=types)
    tree = getattr(parser, f'_read_{root}')()
    if tree is not FAILURE and parser._offset == parser._input_size:
        return tree
    if not parser._expected:
        parser._failure = parser._offset
        parser._expected.append('<EOF>')
    raise ParseError(format_error(parser._input, parser._failure, parser._expected))


def parse_tree_to_xml(tree):
    # does the root of the tree declare an xml helper?
    root = getattr(tree, 'xml', None)
    if root:
        # load the helper class from the xml.py
        root = getattr(xml, root, None)

    tree = tree.to_dict()
    if root:
        # create and use the xml helper class
        return root().to_xml(tree)
    else:
        # default
        return xml.to_xml(tree)


def parse(text, root):
    text = pre_parse(text, indent='{', dedent='}')
    return parse_with_failure(text, root)
