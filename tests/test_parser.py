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

    def test_unparse_strip_newlines(self):
        # strip newlines when unparsing
        # whitespace is NOT stripped
        xml = '''<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"><content><p>test <b>
 text
</b></p><crossHeading>
 crossheading
    </crossHeading><block name="quote"><embeddedStructure><p>quoted text</p></embeddedStructure></block></content></section>
'''
        unparsed = self.parser.unparse(xml)
        self.assertEqual('''SEC

  test ** text**

  CROSSHEADING  crossheading    

  QUOTE
    quoted text
'''.strip(), unparsed.strip())
