import sys

from cobalt import FrbrUri

from bluebell.parser import AkomaNtosoParser


def print_with_lines(text):
    for i, line in enumerate(text.split('\n')):
        i = i + 1
        print(f'{i:02}: {line}', file=sys.stderr)


class ParserSupport:
    def setUp(self):
        super().setUp()
        self.frbr_uri = self.make_frbr_uri()
        self.parser = AkomaNtosoParser(self.frbr_uri)
        self.generator = self.parser.generator

    def parse(self, text, root):
        text = self.parser.pre_parse(text.lstrip())

        try:
            return self.parser.parse_with_failure(text, root)
        except:
            print_with_lines(text)
            raise

    def to_xml(self, dict_tree):
        return self.generator.xml_from_tree(dict_tree)

    def make_frbr_uri(self):
        return FrbrUri.parse('/akn/za/act/2009/10')
