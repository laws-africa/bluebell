from unittest import TestCase

from .support import ParserSupport


class ParserTestCase(ParserSupport, TestCase):
    maxDiff = None

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
