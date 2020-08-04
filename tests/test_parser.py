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

    def test_pre_parse_simple(self):
        self.assertEqual(
            "hello\n",
            self.parser.pre_parse("hello"),
        )

    def test_pre_parse_no_leading_whitespace(self):
        self.assertEqual(
            "hello\n",
            self.parser.pre_parse("  hello"),
        )

        self.assertEqual("""
one
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
        self.parser.indent_size = 4
        self.assertEqual("""
one
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
        self.assertEqual("""
SECTION 1.

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

