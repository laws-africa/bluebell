import os.path
from unittest import TestCase
import re
import datetime

from lxml import etree
from cobalt import StructuredDocument
from cobalt.schemas import assert_validates
from tests.support import print_with_lines, ParserSupport


class RoundTripTestCase(ParserSupport, TestCase):
    maxDiff = None

    def roundtrip(self, prefix, root):
        dir = os.path.join(os.path.dirname(__file__), 'roundtrip')

        fname = os.path.join(dir, f'{prefix}.txt')
        with open(fname, 'rt') as f:
            input = f.read()

        text = self.parser.pre_parse(input)
        try:
            xml = self.parser.parse_to_xml(text, root)
        except:
            print_with_lines(text)
            raise

        actual = self.parser.unparse(xml)

        self.assertMultiLineEqual(input, actual)

        # ensure it validates
        doc = StructuredDocument.for_document_type(root)(etree.tostring(xml, encoding='utf-8'))
        assert_validates(doc, strict=False)

    def roundtrip_xml(self, file_in, root='statement'):
        dir = os.path.join(os.path.dirname(__file__), 'roundtrip')
        fname = os.path.join(dir, f'{file_in}.xml')
        with open(fname, 'rt') as f:
            xml_in_pretty = f.read().replace('TODAY', str(datetime.date.today()))
        xml_in = re.sub(r'\n\s*', '', xml_in_pretty)

        # ensure xml_in validates
        doc = StructuredDocument.for_document_type(root)(xml_in)
        assert_validates(doc, strict=False)

        unparsed = self.parser.unparse(xml_in)
        text = self.parser.pre_parse(unparsed)
        xml_out = self.parser.parse_to_xml(text, root)
        xml_out_pretty = self.tostring(xml_out)

        # ensure xml_out validates
        doc = StructuredDocument.for_document_type(root)(xml_out_pretty)
        assert_validates(doc, strict=False)

        self.assertMultiLineEqual(xml_in_pretty, xml_out_pretty)

    def test_attribs(self):
        self.roundtrip_xml('attribs', root='act')

    def test_escapes(self):
        self.roundtrip_xml('escapes', root='act')

    def test_act(self):
        self.roundtrip('act', 'act')

    def test_judgment(self):
        self.roundtrip('judgment', 'judgment')

    def test_judgment_attachments(self):
        self.roundtrip('judgment-attachments', 'judgment')

    def test_act_footnotes(self):
        self.roundtrip('act-footnotes', 'act')

    def test_act_escapes(self):
        self.roundtrip('act-escapes', 'act')

    def test_eids(self):
        self.roundtrip('eids', 'statement')

    def test_nested_attachments(self):
        self.roundtrip('nested_attachments', 'statement')

    def test_debate_report(self):
        self.roundtrip('debate-report', 'debateReport')

    def test_hansard(self):
        self.roundtrip('hansard', 'debate')

    def test_empty_parts(self):
        self.roundtrip('act-empty', 'act')
