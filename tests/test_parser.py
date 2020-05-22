from unittest import TestCase

from bluebell.parser import pre_parse
from .support import ParserSupport


class ParserTestCase(TestCase, ParserSupport):
    maxDiff = None

    def test_pre_parse_empty(self):
        self.assertEqual(
            "",
            pre_parse("", indent='{', dedent='}'),
        )

        self.assertEqual(
            "",
            pre_parse(" ", indent='{', dedent='}'),
        )

        self.assertEqual(
            "",
            pre_parse("\n", indent='{', dedent='}'),
        )

        self.assertEqual(
            "",
            pre_parse("  \n  ", indent='{', dedent='}'),
        )

    def test_pre_parse_tabs(self):
        self.assertEqual(
            "a  b\n",
            pre_parse("\ta\tb", indent='{', dedent='}'),
        )

    def test_pre_parse_simple(self):
        self.assertEqual(
            "hello\n",
            pre_parse("hello", indent='{', dedent='}'),
        )

    def test_pre_parse_no_leading_whitespace(self):
        self.assertEqual(
            "hello\n",
            pre_parse("  hello", indent='{', dedent='}'),
        )

        self.assertEqual("""
one
{
two
three


}
""",
            pre_parse("""
one
  two
 three
  

""", indent='{', dedent='}'),
        )

    def test_pre_parse_inconsistent_nesting(self):
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
""", pre_parse("""
one
    two
  three
      four
 five
""", indent_size=4, indent='{', dedent='}'),
                         )

