import re
import os.path

from .akn import Parser as BaseParser, FAILURE, ParseError, format_error, TreeNode
import bluebell.types as types
from bluebell.xml import XmlGenerator
from lxml import etree


INDENT = '\x0E'  # ascii SHIFT-IN character
DEDENT = '\x0F'  # ascii SHIFT_OUT character
ROOT_ALIASES = {
    'debatereport': 'debateReport'
}


class Parser(BaseParser):
    # Note: we remove the '^' anchor and use re.match rather than re.search to match against it
    NON_INLINE_START_RE = re.compile(r'[^*/_{\n\\]+')

    def _read_non_inline_start(self):
        """ This is a customised version of _read_non_inline_start that is optimised to let the regular expression
        match multiple times, rather than manually looping over it. This provides a huge speed improvement.
        """
        address0, index0 = FAILURE, self._offset
        cached = self._cache['non_inline_start'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            # ** CUSTOM START
            chunk0 = self._input[self._offset:]
            decr = 1
            m = self.NON_INLINE_START_RE.match(chunk0)
            if m:
                address1 = TreeNode(self._input[self._offset + m.start():self._offset + m.end()], self._offset, [])
                self._offset = self._offset + m.end()
                decr = m.end()
                # ** CUSTOM END
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[^*/_{[\\n]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= decr
                # ** CUSTOM START
                # we matched and cannot match again, stop looping
                break
                # ** CUSTOM END
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['non_inline_start'][index0] = (address0, self._offset)
        return address0


class AkomaNtosoParser:
    """ Parses plain text into well-formed Akoma Ntoso XML.
    """
    indent = INDENT
    dedent = DEDENT
    indent_size = 2

    line_re = re.compile(r'^([ ]*)([^ \n])', re.M)
    trailing_ws_re = re.compile(r' +$', re.M)

    def __init__(self, frbr_uri, eid_prefix=''):
        self.eid_prefix = eid_prefix
        self.generator = XmlGenerator(frbr_uri, self.eid_prefix)

    def parse_to_xml(self, text, root):
        """ Parse text for a particular root rule into XML.
        """
        return self.tree_to_xml(self.parse(text, root))

    def parse(self, text, root):
        """ Parse text for a particular root rule into a parse tree.
        """
        return self.parse_with_failure(self.pre_parse(text), root)

    def tree_to_xml(self, tree):
        """ Transform a parse tree into XML.
        """
        return self.generator.to_xml(tree)

    def pre_parse(self, text):
        """ Pre-parse text, setting up indent and dedent markers.

        After calling this, the following are guaranteed:

        1. no empty lines at the start
        2. no whitespace at the start of a line
        3. no tab characters
        4. no trailing whitespace at the end of a line
        5. a newline at the end of the string

        The indent and dedent parameters are the symbols the grammar
        uses to indicate indented and dedented blocks.
        """
        # tabs to spaces
        text = text.replace('\t', ' ' * self.indent_size)

        # strip leading and trailing whitespace
        # any initial indent is effectively ignored
        text = text.strip()

        # strip trailing whitespace on lines
        text = self.trailing_ws_re.sub('', text)
        if not text.endswith('\n'):
            text = text + '\n'

        stack = [-1]

        def handle_indent(match):
            level = len(match.group(1)) / self.indent_size

            if level == stack[-1]:
                # same level, no change
                return match.group(2)

            elif level > stack[-1]:
                # indent
                stack.append(level)
                return self.indent + "\n" + match.group(2)

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
                        s += self.dedent + "\n"
                        if level >= stack[-1]:
                            break
                        stack.pop()

                    return s + match.group(2)

        text = self.line_re.sub(handle_indent, text)

        text += (self.dedent + "\n") * (len(stack) - 1)

        # exclude initial indent+newline and final dedent+newline
        skip = len(self.indent) + 1
        return text[skip:-skip]

    def parse_with_failure(self, text, root):
        """ Helper function to do the actual parsing with an arbitrary root. Raises ParseError if parsing fails.
        """
        root = ROOT_ALIASES.get(root, root)
        parser = Parser(text, actions=None, types=types)
        tree = getattr(parser, f'_read_{root}')()
        if tree is not FAILURE and parser._offset == parser._input_size:
            return tree
        if not parser._expected:
            parser._failure = parser._offset
            parser._expected.append('<EOF>')
        raise ParseError(format_error(parser._input, parser._failure, parser._expected))

    def unparse(self, xml):
        """ Transform an XML document or fragment into parseable plain text.
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        # load xslt
        fname = os.path.join(os.path.dirname(__file__), 'akn_text.xsl')
        xslt = etree.XSLT(etree.parse(fname))

        return str(xslt(xml))
