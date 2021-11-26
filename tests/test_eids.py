import datetime
import os
import re
from unittest import TestCase

from lxml import etree
from cobalt import StructuredDocument
from cobalt.schemas import assert_validates
from tests.support import ParserSupport


class IdGeneratorTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_clean_num(self):
        self.assertEqual("", self.generator.ids.clean_num(""))
        self.assertEqual("", self.generator.ids.clean_num(" "))
        self.assertEqual("", self.generator.ids.clean_num("( )"))
        self.assertEqual("123-4-5", self.generator.ids.clean_num("(123.4-5)"))
        self.assertEqual("312-32-7", self.generator.ids.clean_num("312.32.7"))
        self.assertEqual("312-32-7", self.generator.ids.clean_num("312-32-7"))
        self.assertEqual("312-32-7", self.generator.ids.clean_num("312_32_7"))
        self.assertEqual("6", self.generator.ids.clean_num("(6)"))
        self.assertEqual("16", self.generator.ids.clean_num("[16]"))
        self.assertEqual("i", self.generator.ids.clean_num("(i)"))
        self.assertEqual("i", self.generator.ids.clean_num("[i]"))
        self.assertEqual("2bis", self.generator.ids.clean_num("(2bis)"))
        self.assertEqual("1-2", self.generator.ids.clean_num('"1.2.'))
        self.assertEqual("1-2", self.generator.ids.clean_num("1.2."))
        self.assertEqual("2-3", self.generator.ids.clean_num("“2.3"))
        self.assertEqual("2-3", self.generator.ids.clean_num("2,3"))
        self.assertEqual("2-3-4", self.generator.ids.clean_num("2,3, 4,"))
        self.assertEqual("3abis", self.generator.ids.clean_num("3a bis"))
        self.assertEqual("3é", self.generator.ids.clean_num("3é"))
        self.assertEqual("3a-4-9", self.generator.ids.clean_num(" -3a--4,9"))

        # hebrew aleph
        self.assertEqual("א", self.generator.ids.clean_num("(א)"))
        # chinese 3
        self.assertEqual("三", self.generator.ids.clean_num("(三)"))

    def test_eids_no_num(self):
        tree = self.parse("""
PARA
    Intro

PARA 1.
    First para

PARA 1A.
    Added in later

PARA
    Unnumbered

PARA 2.
    Second (actually third/fourth/fifth, depending on who's counting) para.
""", 'doc')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<doc xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="doc">
  <mainBody>
    <paragraph eId="para_nn_1">
      <content>
        <p eId="para_nn_1__p_1">Intro</p>
      </content>
    </paragraph>
    <paragraph eId="para_1">
      <num>1.</num>
      <content>
        <p eId="para_1__p_1">First para</p>
      </content>
    </paragraph>
    <paragraph eId="para_1A">
      <num>1A.</num>
      <content>
        <p eId="para_1A__p_1">Added in later</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn_2">
      <content>
        <p eId="para_nn_2__p_1">Unnumbered</p>
      </content>
    </paragraph>
    <paragraph eId="para_2">
      <num>2.</num>
      <content>
        <p eId="para_2__p_1">Second (actually third/fourth/fifth, depending on who's counting) para.</p>
      </content>
    </paragraph>
  </mainBody>
</doc>
""", xml)

    def test_eids_duplicate_num(self):
        tree = self.parse("""
PARA 2.
    Second para.

PARA 2.
    Another para with the num 2.

PARA 2.3..74.5.
    Interesting number.

PARA 2.3..74.5.
    Duplicate interesting number.

PARA 2.3..74.5_2
    Highly unlikely duplicate of eId of previous.
""", 'doc')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<doc xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="doc">
  <mainBody>
    <paragraph eId="para_2">
      <num>2.</num>
      <content>
        <p eId="para_2__p_1">Second para.</p>
      </content>
    </paragraph>
    <paragraph eId="para_2_2">
      <num>2.</num>
      <content>
        <p eId="para_2_2__p_1">Another para with the num 2.</p>
      </content>
    </paragraph>
    <paragraph eId="para_2-3-74-5">
      <num>2.3..74.5.</num>
      <content>
        <p eId="para_2-3-74-5__p_1">Interesting number.</p>
      </content>
    </paragraph>
    <paragraph eId="para_2-3-74-5_2">
      <num>2.3..74.5.</num>
      <content>
        <p eId="para_2-3-74-5_2__p_1">Duplicate interesting number.</p>
      </content>
    </paragraph>
    <paragraph eId="para_2-3-74-5-2">
      <num>2.3..74.5_2</num>
      <content>
        <p eId="para_2-3-74-5-2__p_1">Highly unlikely duplicate of eId of previous.</p>
      </content>
    </paragraph>
  </mainBody>
</doc>
""", xml)

    def test_eids_duplicate_no_num(self):
        tree = self.parse("""
PARA
    Unnumbered para.

PARA
    Second unnumbered para.

PARA (nn)
    Perfectly possible paragraph numbering.

PARA nn_2
    Para nn_2, which is the second para's eId.

PARA nn_2
    Para nn_2, which is a dup of the second para's eId.

PARA nn-2
    Para nn-2, which we don't currently support because we don't like hyphens in numbers
""", 'doc')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<doc xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="doc">
  <mainBody>
    <paragraph eId="para_nn_1">
      <content>
        <p eId="para_nn_1__p_1">Unnumbered para.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn_2">
      <content>
        <p eId="para_nn_2__p_1">Second unnumbered para.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn_3">
      <num>(nn)</num>
      <content>
        <p eId="para_nn_3__p_1">Perfectly possible paragraph numbering.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn-2">
      <num>nn_2</num>
      <content>
        <p eId="para_nn-2__p_1">Para nn_2, which is the second para's eId.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn-2_2">
      <num>nn_2</num>
      <content>
        <p eId="para_nn-2_2__p_1">Para nn_2, which is a dup of the second para's eId.</p>
      </content>
    </paragraph>
    <p eId="p_1">PARA nn-2</p>
    <p eId="p_2">Para nn-2, which we don't currently support because we don't like hyphens in numbers</p>
  </mainBody>
</doc>
""", xml)

    def test_eids_nn(self):
        tree = self.parse("""
PARA (mm)
    Perfectly possible paragraph mm.

PARA (nn)
    Perfectly possible paragraph nn.

PARA (oo)
    Perfectly possible paragraph oo.

PARA
    Unnumbered para.
""", 'doc')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<doc xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="doc">
  <mainBody>
    <paragraph eId="para_mm">
      <num>(mm)</num>
      <content>
        <p eId="para_mm__p_1">Perfectly possible paragraph mm.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn">
      <num>(nn)</num>
      <content>
        <p eId="para_nn__p_1">Perfectly possible paragraph nn.</p>
      </content>
    </paragraph>
    <paragraph eId="para_oo">
      <num>(oo)</num>
      <content>
        <p eId="para_oo__p_1">Perfectly possible paragraph oo.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn_2">
      <content>
        <p eId="para_nn_2__p_1">Unnumbered para.</p>
      </content>
    </paragraph>
  </mainBody>
</doc>
""", xml)

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
        xml_out_pretty = etree.tostring(xml_out, encoding='unicode', pretty_print=True)

        # ensure xml_out validates
        doc = StructuredDocument.for_document_type(root)(xml_out_pretty)
        assert_validates(doc, strict=False)

        self.assertMultiLineEqual(xml_in_pretty, xml_out_pretty)

    def test_eids_against_js_basic(self):
        # should not change a document with correct eids (see bluebell-monaco/tests/eids.js)
        self.roundtrip_xml('eids_basic')

    def test_eids_against_js_edge(self):
        # should not change a document with correct eids (see bluebell-monaco/tests/eids.js)
        self.roundtrip_xml('eids_edge')

    def test_eids_nested_attachments(self):
        self.roundtrip_xml('nested_attachments')
