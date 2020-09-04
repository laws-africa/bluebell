from unittest import TestCase

from lxml import etree
from .support import ParserSupport


class IdGeneratorTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_clean_num(self):
        self.assertEqual(
            "",
            self.generator.ids.clean_num(""),
        )

        self.assertEqual(
            "",
            self.generator.ids.clean_num(" "),
        )

        self.assertEqual(
            "",
            self.generator.ids.clean_num("( )"),
        )

        self.assertEqual(
            "6",
            self.generator.ids.clean_num("(6)"),
        )

        self.assertEqual(
            "16",
            self.generator.ids.clean_num("[16]"),
        )

        self.assertEqual(
            "123.4-5",
            self.generator.ids.clean_num("(123.4-5)"),
        )

        self.assertEqual(
            "12",
            self.generator.ids.clean_num("(12)"),
        )

        self.assertEqual(
            "312.32.7",
            self.generator.ids.clean_num("312.32.7"),
        )

        self.assertEqual(
            "312-32-7",
            self.generator.ids.clean_num("312-32-7"),
        )

        self.assertEqual(
            "312_32_7",
            self.generator.ids.clean_num("312_32_7"),
        )

    def test_hier_element_heading(self):
        tree = self.parse("""
PARA Any-1.ing)([but-a-s=ace - Now we're in the heading!
    Para text.
""", 'doc')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<doc xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <mainBody>
    <paragraph eId="para_Any-1.ingbut-a-s=ace">
      <num>Any-1.ing)([but-a-s=ace</num>
      <heading>Now we're in the heading!</heading>
      <content>
        <p eId="para_Any-1.ingbut-a-s=ace__p_1">Para text.</p>
      </content>
    </paragraph>
  </mainBody>
</doc>
""", xml)
