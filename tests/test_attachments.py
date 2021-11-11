from datetime import date
from unittest import TestCase

from lxml import etree

from cobalt import datestring
from tests.support import ParserSupport


class AttachmentsTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_attachment(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text
""", 'attachment')
        self.assertEqual({
            'type': 'element',
            'name': 'attachment',
            'attribs': {'contains': 'originalVersion', 'name': 'annexure'},
            'heading': [{
                'type': 'text',
                'value': 'a heading',
            }],
            'subheading': [{
                'type': 'text',
                'value': 'subheading',
            }],
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some text',
                }]
            }]
        }, tree.to_dict())

    def test_attachment_no_indent(self):
        tree = self.parse("""
ANNEXURE a heading
SUBHEADING not matched as a subheading

  some text
""", 'attachment')
        self.assertEqual({
            'type': 'element',
            'name': 'attachment',
            'attribs': {'contains': 'originalVersion', 'name': 'annexure'},
            'heading': [{
                'type': 'text',
                'value': 'a heading',
            }],
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'SUBHEADING not matched as a subheading',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some text',
                }]
            }]
        }, tree.to_dict())

    def test_multiple_attachments(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text
  
SCHEDULE heading

  schedule text
""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [{
                'type': 'element',
                'name': 'attachment',
                'attribs': {
                    'name': 'annexure',
                    'contains': 'originalVersion',
                },
                'heading': [{
                    'type': 'text',
                    'value': 'a heading',
                }],
                'subheading': [{
                    'type': 'text',
                    'value': 'subheading',
                }],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'some text',
                    }]
                }]
            }, {
                'type': 'element',
                'name': 'attachment',
                'attribs': {'contains': 'originalVersion', 'name': 'schedule'},
                'heading': [{
                    'type': 'text',
                    'value': 'heading',
                }],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'schedule text',
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)
        today = datestring(date.today())

        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc contains="originalVersion" name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
      </mainBody>
    </doc>
  </attachment>
  <attachment eId="att_2">
    <heading>heading</heading>
    <doc contains="originalVersion" name="schedule">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_2__p_1">schedule text</p>
      </mainBody>
    </doc>
  </attachment>
</attachments>
""", xml)

    def test_multiple_attachments_no_indent(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

some text

SCHEDULE heading

schedule text
""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [{
                'type': 'element',
                'name': 'attachment',
                'attribs': {
                    'name': 'annexure',
                    'contains': 'originalVersion',
                },
                'heading': [{
                    'type': 'text',
                    'value': 'a heading',
                }],
                'subheading': [{
                    'type': 'text',
                    'value': 'subheading',
                }],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'some text',
                    }]
                }]
            }, {
                'type': 'element',
                'name': 'attachment',
                'attribs': {'contains': 'originalVersion', 'name': 'schedule'},
                'heading': [{
                    'type': 'text',
                    'value': 'heading',
                }],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'schedule text',
                    }]
                }]
            }]
        }, tree.to_dict())

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)
        today = datestring(date.today())

        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc contains="originalVersion" name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
      </mainBody>
    </doc>
  </attachment>
  <attachment eId="att_2">
    <heading>heading</heading>
    <doc contains="originalVersion" name="schedule">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_2__p_1">schedule text</p>
      </mainBody>
    </doc>
  </attachment>
</attachments>
""", xml)

    def test_nested_attachments_basic(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text

  SCHEDULE heading
    SUBHEADING a nother subheading

    schedule text
""", 'attachment')
        self.assertEqual({
            'type': 'element',
            'name': 'attachment',
            'attribs': {'contains': 'originalVersion', 'name': 'annexure'},
            'heading': [{'type': 'text', 'value': 'a heading'}],
            'subheading': [{'type': 'text', 'value': 'subheading'}],
            'children': [{
                'type': 'content',
                'name': 'p',
                'children': [{
                    'type': 'text',
                    'value': 'some text'}]
            }, {
                'type': 'element',
                'name': 'attachment',
                'attribs': {'contains': 'originalVersion', 'name': 'schedule'},
                'heading': [{'type': 'text', 'value': 'heading'}],
                'subheading': [{'type': 'text', 'value': 'a nother subheading'}],
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'schedule text',
                    }],
                }],
            }]
        }, tree.to_dict())
        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)
        today = datestring(date.today())
        self.assertEqual(f"""<attachment xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="att_1">
  <heading>a heading</heading>
  <subheading>subheading</subheading>
  <doc contains="originalVersion" name="annexure">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
          <FRBRuri value="/akn/za/act/2009/10"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRdate date="2009" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
          <FRBRnumber value="10"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
          <FRBRuri value="/akn/za/act/2009/10/eng"/>
          <FRBRdate date="{today}" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
          <FRBRuri value="/akn/za/act/2009/10/eng"/>
          <FRBRdate date="{today}" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <references source="#cobalt">
        <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
      </references>
    </meta>
    <mainBody>
      <p eId="att_1__p_1">some text</p>
    </mainBody>
    <attachments>
      <attachment eId="att_1__att_1">
        <heading>heading</heading>
        <subheading>a nother subheading</subheading>
        <doc contains="originalVersion" name="schedule">
          <meta>
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/akn/za/act/2009/10/!annexure_1__schedule_1"/>
                <FRBRuri value="/akn/za/act/2009/10"/>
                <FRBRalias value="Untitled" name="title"/>
                <FRBRdate date="2009" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="za"/>
                <FRBRnumber value="10"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1"/>
                <FRBRuri value="/akn/za/act/2009/10/eng"/>
                <FRBRdate date="{today}" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1"/>
                <FRBRuri value="/akn/za/act/2009/10/eng"/>
                <FRBRdate date="{today}" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
            <references source="#cobalt">
              <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
            </references>
          </meta>
          <mainBody>
            <p eId="att_1__att_1__p_1">schedule text</p>
          </mainBody>
        </doc>
      </attachment>
    </attachments>
  </doc>
</attachment>
""", xml)

    def test_nested_attachments_back_out(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text

  SCHEDULE heading
    SUBHEADING a nother subheading

    schedule text

ANNEXURE back out
  SUBHEADING subhead

  more content
""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [
                {
                    'type': 'element',
                    'name': 'attachment',
                    'attribs': {'contains': 'originalVersion', 'name': 'annexure'},
                    'children': [
                        {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'some text'}]
                        }, {
                            'type': 'element',
                            'name': 'attachment',
                            'attribs': {'contains': 'originalVersion', 'name': 'schedule'},
                            'children': [{
                                'type': 'content',
                                'name': 'p',
                                'children': [{
                                    'type': 'text',
                                    'value': 'schedule text'}]}],
                            'heading': [{'type': 'text', 'value': 'heading'}],
                            'subheading': [{'type': 'text', 'value': 'a nother subheading'}]}],
                    'heading': [{'type': 'text', 'value': 'a heading'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}]
                }, {
                    'type': 'element',
                    'name': 'attachment',
                    'attribs': {'contains': 'originalVersion', 'name': 'annexure'},
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'more content'}]}],
                    'heading': [{'type': 'text', 'value': 'back out'}],
                    'subheading': [{'type': 'text', 'value': 'subhead'}]}
            ]
        }, tree.to_dict())
        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc contains="originalVersion" name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>heading</heading>
          <subheading>a nother subheading</subheading>
          <doc contains="originalVersion" name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1__schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias value="Untitled" name="title"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
              <references source="#cobalt">
                <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
              </references>
            </meta>
            <mainBody>
              <p eId="att_1__att_1__p_1">schedule text</p>
            </mainBody>
          </doc>
        </attachment>
      </attachments>
    </doc>
  </attachment>
  <attachment eId="att_2">
    <heading>back out</heading>
    <subheading>subhead</subheading>
    <doc contains="originalVersion" name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_2__p_1">more content</p>
      </mainBody>
    </doc>
  </attachment>
</attachments>
""", xml)

    def test_nested_attachments_deep(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text

  SCHEDULE heading
    SUBHEADING a nother subheading

    SCHEDULE deeper heading

      SCHEDULE even deeper heading

        content in final nest

ANNEXURE back out
  SUBHEADING subhead

  more content
""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [
                {
                    'type': 'element',
                    'name': 'attachment',
                    'attribs': {'contains': 'originalVersion', 'name': 'annexure'},
                    'children': [
                        {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'some text'}]
                        }, {
                            'type': 'element',
                            'name': 'attachment',
                            'attribs': {'contains': 'originalVersion', 'name': 'schedule'},
                            'children': [{
                                'type': 'element',
                                'name': 'attachment',
                                'attribs': {'contains': 'originalVersion', 'name': 'schedule'},
                                'children': [{
                                    'type': 'element',
                                    'name': 'attachment',
                                    'attribs': {'contains': 'originalVersion', 'name': 'schedule'},
                                    'children': [{
                                        'type': 'content',
                                        'name': 'p',
                                        'children': [{
                                            'type': 'text',
                                            'value': 'content in final nest'}]}],
                                    'heading': [{'type': 'text', 'value': 'even deeper heading'}]}],
                                'heading': [{'type': 'text', 'value': 'deeper heading'}]}],
                            'heading': [{'type': 'text', 'value': 'heading'}],
                            'subheading': [{'type': 'text', 'value': 'a nother subheading'}]}],
                    'heading': [{'type': 'text', 'value': 'a heading'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}]
                }, {
                    'type': 'element',
                    'name': 'attachment',
                    'attribs': {'contains': 'originalVersion', 'name': 'annexure'},
                    'children': [{
                        'type': 'content',
                        'name': 'p',
                        'children': [{
                            'type': 'text',
                            'value': 'more content'}]}],
                    'heading': [{'type': 'text', 'value': 'back out'}],
                    'subheading': [{'type': 'text', 'value': 'subhead'}]}
            ]
        }, tree.to_dict())
        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc contains="originalVersion" name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>heading</heading>
          <subheading>a nother subheading</subheading>
          <doc contains="originalVersion" name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1__schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias value="Untitled" name="title"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
              <references source="#cobalt">
                <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
              </references>
            </meta>
            <mainBody/>
            <attachments>
              <attachment eId="att_1__att_1__att_1">
                <heading>deeper heading</heading>
                <doc contains="originalVersion" name="schedule">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1__schedule_1__schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias value="Untitled" name="title"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1__schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1__schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                    <references source="#cobalt">
                      <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
                    </references>
                  </meta>
                  <mainBody/>
                  <attachments>
                    <attachment eId="att_1__att_1__att_1__att_1">
                      <heading>even deeper heading</heading>
                      <doc contains="originalVersion" name="schedule">
                        <meta>
                          <identification source="#cobalt">
                            <FRBRWork>
                              <FRBRthis value="/akn/za/act/2009/10/!annexure_1__schedule_1__schedule_1__schedule_1"/>
                              <FRBRuri value="/akn/za/act/2009/10"/>
                              <FRBRalias value="Untitled" name="title"/>
                              <FRBRdate date="2009" name="Generation"/>
                              <FRBRauthor href=""/>
                              <FRBRcountry value="za"/>
                              <FRBRnumber value="10"/>
                            </FRBRWork>
                            <FRBRExpression>
                              <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1__schedule_1__schedule_1"/>
                              <FRBRuri value="/akn/za/act/2009/10/eng"/>
                              <FRBRdate date="{today}" name="Generation"/>
                              <FRBRauthor href=""/>
                              <FRBRlanguage language="eng"/>
                            </FRBRExpression>
                            <FRBRManifestation>
                              <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1__schedule_1__schedule_1__schedule_1"/>
                              <FRBRuri value="/akn/za/act/2009/10/eng"/>
                              <FRBRdate date="{today}" name="Generation"/>
                              <FRBRauthor href=""/>
                            </FRBRManifestation>
                          </identification>
                          <references source="#cobalt">
                            <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
                          </references>
                        </meta>
                        <mainBody>
                          <p eId="att_1__att_1__att_1__att_1__p_1">content in final nest</p>
                        </mainBody>
                      </doc>
                    </attachment>
                  </attachments>
                </doc>
              </attachment>
            </attachments>
          </doc>
        </attachment>
      </attachments>
    </doc>
  </attachment>
  <attachment eId="att_2">
    <heading>back out</heading>
    <subheading>subhead</subheading>
    <doc contains="originalVersion" name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias value="Untitled" name="title"/>
            <FRBRdate date="2009" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRcountry value="za"/>
            <FRBRnumber value="10"/>
          </FRBRWork>
          <FRBRExpression>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="{today}" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p eId="att_2__p_1">more content</p>
      </mainBody>
    </doc>
  </attachment>
</attachments>
""", xml)
