import os
from unittest import TestCase

from lxml import etree

from tests.support import ParserSupport


class AttachmentWorkComponentsTestCase(ParserSupport, TestCase):
    maxDiff = None

    def rewrite_and_compare(self, xml_in, xml_out):
        dir = os.path.join(os.path.dirname(__file__), 'rewrite_work_components')
        with open(os.path.join(dir, f'{xml_in}.xml'), 'rt') as f:
            old_xml = f.read()
        with open(os.path.join(dir, f'{xml_out}.xml'), 'rt') as f:
            expected = f.read()

        xml = etree.fromstring(old_xml)
        self.generator.rewrite_all_attachment_work_components(xml)
        actual = self.tostring(xml)

        self.assertEqual(expected, actual)

    def test_fix_work_components_basic(self):
        self.rewrite_and_compare('basic_in', 'basic_out')
