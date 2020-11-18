import datetime
from unittest import TestCase

from lxml import etree
from cobalt import StructuredDocument
from cobalt.schemas import assert_validates
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
    <paragraph eId="para_2.3..74.5">
      <num>2.3..74.5.</num>
      <content>
        <p eId="para_2.3..74.5__p_1">Interesting number.</p>
      </content>
    </paragraph>
    <paragraph eId="para_2.3..74.5_2">
      <num>2.3..74.5.</num>
      <content>
        <p eId="para_2.3..74.5_2__p_1">Duplicate interesting number.</p>
      </content>
    </paragraph>
    <paragraph eId="para_2.3..74.5_2_2">
      <num>2.3..74.5_2</num>
      <content>
        <p eId="para_2.3..74.5_2_2__p_1">Highly unlikely duplicate of eId of previous.</p>
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
    Para nn_2, which is the previous para's eId.

PARA nn_2_2
    Para nn_2_2, which is the previous para's eId.

PARA nn_2_2
    Another para nn_2_2.
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
    <paragraph eId="para_nn_2_2">
      <num>nn_2</num>
      <content>
        <p eId="para_nn_2_2__p_1">Para nn_2, which is the previous para's eId.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn_2_2_2">
      <num>nn_2_2</num>
      <content>
        <p eId="para_nn_2_2_2__p_1">Para nn_2_2, which is the previous para's eId.</p>
      </content>
    </paragraph>
    <paragraph eId="para_nn_2_2_3">
      <num>nn_2_2</num>
      <content>
        <p eId="para_nn_2_2_3__p_1">Another para nn_2_2.</p>
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

    def test_eids_against_js(self):
        # should not change a document with correct eids (see bluebell-monaco/tests/eids.js)
        xml_in = f'''<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <statement name="statement">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/akn/za/act/2009/10"/>
          <FRBRuri value="/akn/za/act/2009/10"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRdate date="2009" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
          <FRBRnumber value="10"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/akn/za/act/2009/10/eng"/>
          <FRBRuri value="/akn/za/act/2009/10/eng"/>
          <FRBRdate date="{datetime.date.today()}" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/akn/za/act/2009/10/eng"/>
          <FRBRuri value="/akn/za/act/2009/10/eng"/>
          <FRBRdate date="{datetime.date.today()}" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <references source="#cobalt">
        <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
      </references>
    </meta>
    <mainBody>
      <p eId="p_1">
        <i>The Conference of Parties,</i>
      </p>
      <division eId="dvs_A">
        <num>A.</num>
        <heading>Cooperation with other conventions</heading>
        <intro>
          <p eId="dvs_A__intro__p_1"><i>Noting</i> the report of the Executive Secretary on progress,<sup><authorialNote marker="1" placement="bottom" eId="dvs_A__intro__p_1__authorialNote_1"><p eId="dvs_A__intro__p_1__authorialNote_1__p_1">UNEP/CBD/COP/12/24.</p></authorialNote></sup></p>
          <p eId="dvs_A__intro__p_2"><i>Recalling</i> decision XI/6, including paragraph 3, in which it urged Parties to pursue efforts to enhance synergies among the biodiversity-related conventions to promote policy coherence, improve efficiency and enhance coordination and cooperation at all levels, and with a view to strengthening Parties’ ownership of the process,</p>
        </intro>
        <paragraph eId="dvs_A__para_1">
          <num>1.</num>
          <content>
            <p eId="dvs_A__para_1__p_1"><i>Welcomes</i> the International Plant Protection Convention as a member of the Liaison Group of the Biodiversity-related Conventions and <i>notes</i> with appreciation the role of the International Plant Protection Convention in helping to achieve Aichi Biodiversity Target 9;</p>
          </content>
        </paragraph>
        <paragraph eId="dvs_A__para_4">
          <num>4.</num>
          <content>
            <p eId="dvs_A__para_4__p_1"><i>Reaffirming</i> <ref href="/akn/un/statement/decision/unep-cbd-cop/2010-10-18/10-20">decision X/20</ref>, <i>invites</i> the members of the Liaison Group of the Biodiversity-related Conventions:</p>
            <blockList eId="dvs_A__para_4__list_1">
              <item eId="dvs_A__para_4__list_1__item_a">
                <num>(a)</num>
                <p eId="dvs_A__para_4__list_1__item_a__p_1">To increase their cooperation, coordination and attention to synergies in the development of their respective reporting systems, including future online reporting systems, as a means to increase synergies in national reporting under the biodiversity-related conventions;</p>
              </item>
              <item eId="dvs_A__para_4__list_1__item_b">
                <num>(b)</num>
                <p eId="dvs_A__para_4__list_1__item_b__p_1">To consider ways and means to increase cooperation on outreach and communication strategies;</p>
              </item>
            </blockList>
          </content>
        </paragraph>
      </division>
      <division eId="dvs_B">
        <num>B.</num>
        <heading>Cooperation with international organizations and initiatives</heading>
        <intro>
          <p eId="dvs_B__intro__p_1"><i>Recognizing</i> the need for an all-encompassing effort by all relevant processes to achieve the Aichi Biodiversity Targets, taking into account different views and approaches to achieve the conservation and sustainable use of biodiversity and sustainable development,</p>
        </intro>
        <paragraph eId="dvs_B__para_13">
          <num>13.</num>
          <content>
            <p eId="dvs_B__para_13__p_1"><i>Reiterates</i> the importance of a United Nations system‑wide approach to the implementation of the Strategic Plan for Biodiversity 2011-2020 and the achievement of the Aichi Biodiversity Targets in the framework of the United Nations Decade for Biodiversity,<sup><authorialNote marker="3" placement="bottom" eId="dvs_B__para_13__p_1__authorialNote_1"><p eId="dvs_B__para_13__p_1__authorialNote_1__p_1">See General Assembly resolution 65/161.</p></authorialNote></sup> and <i>welcomes</i> the report of the Environment Management Group on relevant activities of the Issue Management Group on Biodiversity;<sup><authorialNote marker="4" placement="bottom" eId="dvs_B__para_13__p_1__authorialNote_2"><p eId="dvs_B__para_13__p_1__authorialNote_2__p_1">UNEP/CBD/COP/12/INF/48. See also: United Nations Environment Programme, Advancing the Biodiversity Agenda: A UN System-wide Contribution. A report by the Environment Management Group (EMG/1320/GEN) (UNEP, 2010). Available from <ref href="http://unemg.org">http://unemg.org</ref>;</p></authorialNote></sup></p>
          </content>
        </paragraph>
        <paragraph eId="dvs_B__para_14">
          <num>14.</num>
          <content>
            <p eId="dvs_B__para_14__p_1"><i>Invites</i> the United Nations and other organizations to continue their efforts in furthering the integration of the Aichi Biodiversity Targets throughout the United Nations system, in particular through the Environment Management Group and other relevant initiatives;</p>
          </content>
        </paragraph>
      </division>
    </mainBody>
  </statement>
</akomaNtoso>
'''
        unparsed = self.parser.unparse(xml_in)
        text = self.parser.pre_parse(unparsed)
        xml = self.parser.parse_to_xml(text, 'statement')
        xml_out = etree.tostring(xml, encoding='unicode', pretty_print=True)

        self.assertMultiLineEqual(xml_in, xml_out)

        # ensure it validates
        doc = StructuredDocument.for_document_type('statement')(xml_out)
        assert_validates(doc, strict=False)
