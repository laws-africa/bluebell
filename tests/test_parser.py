import sys
import types
from unittest import TestCase
from unittest.mock import patch

from cobalt import FrbrUri
from lxml import etree

import bluebell.parser
from bluebell import parse_to_xml, parse_to_xml_bytes, parse_to_xml_str
from .support import ParserSupport


class ParserTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_top_level_parse_to_xml_function(self):
        xml = parse_to_xml("P hello", "statement", FrbrUri.parse("/akn/za/statement/2022/1"))

        ns = {'a': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}
        self.assertEqual('akomaNtoso', etree.QName(xml).localname)
        self.assertEqual(
            ['hello'],
            xml.xpath('/a:akomaNtoso/a:statement/a:mainBody/a:p/text()', namespaces=ns),
        )

    def test_top_level_parse_to_xml_str_function(self):
        xml = parse_to_xml_str("P hello", "statement", FrbrUri.parse("/akn/za/statement/2022/1"))

        self.assertIsInstance(xml, str)
        self.assertIn('<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">', xml)
        self.assertIn('>hello</p>', xml)

    def test_top_level_parse_to_xml_bytes_function(self):
        xml = parse_to_xml_bytes("P hello", "statement", FrbrUri.parse("/akn/za/statement/2022/1"))

        self.assertIsInstance(xml, bytes)
        self.assertIn(b'<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">', xml)
        self.assertIn(b'>hello</p>', xml)

    def test_top_level_parse_to_xml_uses_rust_extension_when_available(self):
        module = types.ModuleType("_bluebell_rs")
        module.parse_to_xml = lambda text, root, frbr_uri, eid_prefix='': (
            b'<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">'
            b'<statement name="statement"><mainBody><p eId="p_1">rust</p></mainBody></statement>'
            b'</akomaNtoso>'
        )

        with patch.dict(sys.modules, {"_bluebell_rs": module}):
            xml = bluebell.parser.parse_to_xml(
                "P ignored",
                "statement",
                FrbrUri.parse("/akn/za/statement/2022/1"),
            )

        self.assertEqual(["rust"], xml.xpath("//*[local-name()='p']/text()"))

    def test_top_level_parse_to_xml_str_decodes_rust_extension_bytes(self):
        module = types.ModuleType("_bluebell_rs")
        module.parse_to_xml = lambda text, root, frbr_uri, eid_prefix='': (
            b'<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">'
            b'<statement name="statement"><mainBody><p eId="p_1">rust</p></mainBody></statement>'
            b'</akomaNtoso>'
        )

        with patch.dict(sys.modules, {"_bluebell_rs": module}):
            xml = bluebell.parser.parse_to_xml_str(
                "P ignored",
                "statement",
                FrbrUri.parse("/akn/za/statement/2022/1"),
            )

        self.assertIsInstance(xml, str)
        self.assertIn(">rust</p>", xml)

    def test_top_level_parse_to_xml_bytes_uses_rust_extension_when_available(self):
        module = types.ModuleType("_bluebell_rs")
        module.parse_to_xml = lambda text, root, frbr_uri, eid_prefix='': (
            b'<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">'
            b'<statement name="statement"><mainBody><p eId="p_1">rust</p></mainBody></statement>'
            b'</akomaNtoso>'
        )

        with patch.dict(sys.modules, {"_bluebell_rs": module}):
            xml = bluebell.parser.parse_to_xml_bytes(
                "P ignored",
                "statement",
                FrbrUri.parse("/akn/za/statement/2022/1"),
            )

        self.assertIsInstance(xml, bytes)
        self.assertIn(b">rust</p>", xml)

    def test_top_level_parse_to_xml_passes_eid_prefix_to_rust_extension(self):
        module = types.ModuleType("_bluebell_rs")

        def parse_to_xml(text, root, frbr_uri, eid_prefix=''):
            self.assertEqual("pref", eid_prefix)
            return (
                b'<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">'
                b'<statement name="statement"><mainBody><p eId="pref__p_1">prefixed</p></mainBody></statement>'
                b'</akomaNtoso>'
            )

        module.parse_to_xml = parse_to_xml

        with patch.dict(sys.modules, {"_bluebell_rs": module}):
            xml = bluebell.parser.parse_to_xml(
                "P prefixed",
                "statement",
                FrbrUri.parse("/akn/za/statement/2022/1"),
                eid_prefix="pref",
            )

        self.assertEqual(["prefixed"], xml.xpath("//*[local-name()='p']/text()"))
        self.assertEqual(["pref__p_1"], xml.xpath("//*[local-name()='p']/@eId"))

    def test_top_level_functions_accept_string_frbr_uri_without_rust_extension(self):
        # a string frbr_uri must work in the pure-Python fallback path, not
        # just when the Rust extension is installed
        with patch.dict(sys.modules, {"_bluebell_rs": None}):
            xml = bluebell.parser.parse_to_xml_str(
                "P hello",
                "statement",
                "/akn/za/statement/2022/1",
            )

        self.assertIn('<FRBRuri value="/akn/za/statement/2022/1"/>', xml)
        self.assertIn('>hello</p>', xml)

    def test_pre_parse_empty(self):
        self.assertEqual(
            "",
            self.parser.pre_parse(""),
        )

        self.assertEqual(
            "",
            self.parser.pre_parse(" "),
        )

        self.assertEqual(
            "",
            self.parser.pre_parse("\n"),
        )

        self.assertEqual(
            "",
            self.parser.pre_parse("  \n  "),
        )

    def test_pre_parse_tabs(self):
        self.assertEqual(
            "a  b\n",
            self.parser.pre_parse("\ta\tb"),
        )

    def test_pre_parse_leading_whitespace(self):
        self.assertEqual(
            "b\nanother line\n",
            self.parser.pre_parse("  \n  \t\n  \n\t\n b\nanother line\n")
        )
        self.assertEqual(
            "a line\n",
            self.parser.pre_parse("\na line\n")
        )
        self.assertEqual(
            "a line\n",
            self.parser.pre_parse("\n\n\na line\n")
        )

    def test_pre_parse_simple(self):
        self.assertEqual(
            "hello\n",
            self.parser.pre_parse("hello"),
        )

    def test_pre_parse_no_leading_whitespace(self):
        self.parser.indent = '{'
        self.parser.dedent = '}'
        self.assertEqual(
            "hello\n",
            self.parser.pre_parse("  hello"),
        )

        self.assertEqual("""one
{
two
three
}
""",
            self.parser.pre_parse("""
one
  two
 three
  

"""))

    def test_pre_parse_inconsistent_nesting(self):
        self.parser.indent = '{'
        self.parser.dedent = '}'
        self.parser.indent_size = 4
        self.assertEqual("""one
{
two
three
{
four
}
}
five
""",
        self.parser.pre_parse("""
one
    two
  three
      four
 five
"""))

    def test_pre_parse_tables(self):
        self.parser.indent = '{'
        self.parser.dedent = '}'
        self.assertEqual("""SECTION 1.

{
SUBSECTION (a)

{
{|
|
}
bar
{
|}
}
}
""",
         self.parser.pre_parse("""
SECTION 1.

  SUBSECTION (a)
      
    {|
    |
  bar
    |}
"""))

    def test_pre_parse_crlf_line_endings(self):
        # \r is not a line separator and is preserved in the text
        self.assertEqual(
            "BODY\r\ntext\n",
            self.parser.pre_parse("BODY\r\ntext\r\n"),
        )
        self.assertEqual(
            "a\rb\n",
            self.parser.pre_parse("a\rb"),
        )
        # trailing spaces are only stripped before a newline, not before a \r
        self.assertEqual(
            "a \r\nb\n",
            self.parser.pre_parse("a \r\nb"),
        )

    def test_pre_parse_control_char_whitespace(self):
        # \x0b, \x0c and \x1c-\x1f count as whitespace at the document edges
        self.assertEqual("a\n", self.parser.pre_parse("\x1ca\x1f"))
        self.assertEqual("a\n", self.parser.pre_parse("\x0ba\x0c"))
        # but are preserved inside the document
        self.assertEqual("a\x1cb\n", self.parser.pre_parse("a\x1cb"))

    def test_pre_parse_unicode_whitespace(self):
        # unicode whitespace is stripped at the document edges
        self.assertEqual("a\n", self.parser.pre_parse("\xa0a\xa0"))
        self.assertEqual("a\n", self.parser.pre_parse("\x85a"))
        # but is not treated as indentation and is preserved in text
        self.assertEqual("a\n\xa0 b\n", self.parser.pre_parse("a\n\xa0 b"))
        self.assertEqual("a\n\u2003b\n", self.parser.pre_parse("a\n\u2003b"))

    def test_parse_crlf_line_endings(self):
        # \r is not a line separator: markers followed by \r are not recognised,
        # and the \r stays in the text
        xml = self.parser.parse_to_xml("BODY\r\nSEC 1. - Heading\r\n  Some text.\r\n", 'act')

        self.assertEqual("""<body xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <hcontainer eId="hcontainer_1" name="hcontainer">
    <content>
      <p eId="hcontainer_1__p_1">BODY&#13;</p>
    </content>
  </hcontainer>
  <section eId="sec_1">
    <num>1.</num>
    <heading>Heading&#13;</heading>
    <content>
      <p eId="sec_1__p_1">Some text.</p>
    </content>
  </section>
</body>
""", self.tostring(etree.tostring(xml.find('.//{*}body'), encoding='unicode')))

    def test_unparse_strip_newlines_and_whitespace(self):
        # strip newlines anywhere
        # strip whitespace at the start of P, listIntroduction and listWrapup
        xml = '''<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p>
        test <b>
 text
</b></p><crossHeading>
 crossheading
    </crossHeading><blockList><listIntroduction>  ITEMS escaped
</listIntroduction><item><p>
  item
</p></item><listWrapUp>
  some wrap
  up</listWrapUp></blockList><block name="quote"><embeddedStructure><p>   quoted text</p></embeddedStructure></block></content></section>
'''
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  test **  text **

  CROSSHEADING   crossheading     

  ITEMS
    \ITEMS escaped 

    ITEM
      item 

    some wrap   up

  QUOTE
    quoted text
'''.strip(), unparsed.strip())

    def test_unparse_images(self):
        # replace spaces in image names
        xml = '<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p><img src="media/foo bar.png" alt="alt text"/></p></content></section>'
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  {{IMG media/foo%20bar.png alt text}}
'''.strip(), unparsed.strip())

    def test_unparse_links(self):
        # replace spaces in hrefs
        xml = '<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p><ref href="foo bar">link text</ref></p></content></section>'
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  {{>foo%20bar link text}}
'''.strip(), unparsed.strip())

    def test_unparse_multiline_remarks_with_whitespace(self):
        xml = '<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p><remark status="editorial">remark<br/>  with white <b> space</b> and bold<br/>and other</remark></p></content></section>'
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  {{*remark
  with white ** space** and bold
  and other}}
'''.strip(), unparsed.strip())

    def test_unparse_inline_escapes(self):
        xml = '<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p><i>/italics/</i></p><p><b>*bold*</b></p><p><u>_underline_</u></p></content></section>'
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  //\/italics\///

  **\*bold\***

  __\_underline\___
'''.strip(), unparsed.strip())

    def test_unparse_inline_escapes_outside(self):
        xml = '<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p>/<i>italics</i>/</p><p>*<b>bold</b>*</p><p>_<u>underline</u>_</p></content></section>'
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  \///italics//\/

  \***bold**\*

  \___underline__\_
'''.strip(), unparsed.strip())

    def test_unparse_inline_escapes_double(self):
        xml = '<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p><i>//italics//</i></p><p><b>**bold**</b></p><p><u>__underline__</u></p></content></section>'
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  //\/\/italics\/\///

  **\*\*bold\*\***

  __\_\_underline\_\___
'''.strip(), unparsed.strip())
