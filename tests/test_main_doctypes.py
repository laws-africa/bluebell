from unittest import TestCase

from lxml import etree

from bluebell.parser import AkomaNtosoParser
from cobalt import Judgment, Act, FrbrUri, Statement, DebateReport, Bill, Document, Debate
from cobalt.schemas import assert_validates

from tests.support import ParserSupport


class MainDoctypesTestCase(ParserSupport, TestCase):
    def validate_empty(self, root, doc_class):
        self.frbr_uri = FrbrUri.parse(f'/akn/za/{root}/2022/1')
        self.parser = AkomaNtosoParser(self.frbr_uri)
        self.generator = self.parser.generator

        xml = self.parser.parse_to_xml('', root)
        xml = etree.tostring(xml, encoding='unicode')
        assert_validates(doc_class(xml))

    def test_empty_judgment(self):
        self.validate_empty('judgment', Judgment)

    def test_empty_act(self):
        self.validate_empty('act', Act)

    def test_empty_bill(self):
        self.validate_empty('bill', Bill)

    def test_empty_statement(self):
        self.validate_empty('statement', Statement)

    def test_empty_doc(self):
        self.validate_empty('doc', Document)

    def test_empty_debateReport(self):
        self.validate_empty('debateReport', DebateReport)

    def test_empty_debate(self):
        self.validate_empty('debate', Debate)
