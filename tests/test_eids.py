from unittest import TestCase

from bluebell.xml import IdGenerator


class IdGeneratorTestCase(TestCase):
    generator = IdGenerator()

    def test_clean_num(self):
        self.assertEqual(
            "",
            self.generator.clean_num(""),
        )

        self.assertEqual(
            "",
            self.generator.clean_num(" "),
        )

        self.assertEqual(
            "",
            self.generator.clean_num("( )"),
        )

        self.assertEqual(
            "6",
            self.generator.clean_num("(6)"),
        )

        self.assertEqual(
            "16",
            self.generator.clean_num("[16]"),
        )

        self.assertEqual(
            "123.4-5",
            self.generator.clean_num("(123.4-5)"),
        )

        self.assertEqual(
            "12",
            self.generator.clean_num("(12)"),
        )

        self.assertEqual(
            "312.32.7",
            self.generator.clean_num("312.32.7"),
        )

        self.assertEqual(
            "312-32-7",
            self.generator.clean_num("312-32-7"),
        )

        self.assertEqual(
            "312_32_7",
            self.generator.clean_num("312_32_7"),
        )
