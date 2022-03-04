import datetime
import os
import re
from unittest import TestCase

from lxml import etree
from cobalt import StructuredDocument
from cobalt.schemas import assert_validates
from tests.support import ParserSupport
from bluebell.xml import IdGenerator


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

        xml = self.tostring(self.to_xml(tree.to_dict()))

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

        xml = self.tostring(self.to_xml(tree.to_dict()))

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
    Para nn-2, which we do support because we support hyphens in numbers
""", 'doc')

        xml = self.tostring(self.to_xml(tree.to_dict()))

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
    <paragraph eId="para_nn-2_3">
      <num>nn-2</num>
      <content>
        <p eId="para_nn-2_3__p_1">Para nn-2, which we do support because we support hyphens in numbers</p>
      </content>
    </paragraph>
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

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
        xml_out_pretty = self.tostring(xml_out)

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

    def test_eids_debatereport(self):
        self.roundtrip_xml('eids_debatereport', root='debateReport')

    def rewrite_compare_eids(self, text, root='doc'):
        """ Ensures eIds are rewritten exactly the same as they're written initially.
        """
        generator = IdGenerator()
        tree = self.parse(text, root)
        xml = self.to_xml(tree.to_dict())
        old_xml = self.tostring(xml)
        generator.rewrite_all_eids(xml)
        new_xml = self.tostring(xml)
        self.assertEqual(old_xml, new_xml)

    def test_rewrite_eids_no_num(self):
        self.rewrite_compare_eids("""
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
""")

    def test_rewrite_eids_duplicate_num(self):
        self.rewrite_compare_eids("""
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
""")

    def test_rewrite_eids_duplicate_no_num(self):
        self.rewrite_compare_eids("""
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
""")

    def test_rewrite_eids_duplicate_nn(self):
        self.rewrite_compare_eids("""
PARA (mm)
  Perfectly possible paragraph mm.

PARA (nn)
  Perfectly possible paragraph nn.

PARA (oo)
  Perfectly possible paragraph oo.

PARA
  Unnumbered para.
""")

    def rewrite_fix_eids(self, xml_in, xml_out):
        """ Ensures incorrect or older-style eIds are rewritten correctly.
        """
        dir = os.path.join(os.path.dirname(__file__), 'rewrite_eids')
        fname_in = os.path.join(dir, f'{xml_in}.xml')
        with open(fname_in, 'rt') as f:
            old_xml = f.read()
        fname_out = os.path.join(dir, f'{xml_out}.xml')
        with open(fname_out, 'rt') as f:
            expected = f.read()

        generator = IdGenerator()
        xml = etree.fromstring(old_xml)
        generator.rewrite_all_eids(xml)
        actual = self.tostring(xml)

        self.assertEqual(expected, actual)

    def test_rewrite_fix_eids_unchanged(self):
        """ Checks that rewrite_all_eids() doesn't change a document with correct eids"""
        self.rewrite_fix_eids('out', 'out')
        self.rewrite_fix_eids('unchanged_1', 'unchanged_1')
        self.rewrite_fix_eids('unchanged_2', 'unchanged_2')

    def test_rewrite_fix_eids_fixed(self):
        """ Checks that rewrite_all_eids() does fix a document with incorrect or missing eids"""
        self.rewrite_fix_eids('bad_eids', 'out')
        self.rewrite_fix_eids('missing_eids', 'out')
        self.rewrite_fix_eids('empty_doc_in', 'empty_doc_out')
