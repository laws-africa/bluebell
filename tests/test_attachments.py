from unittest import TestCase

from lxml import etree

from tests.support import ParserSupport


class ContainerTestCase(ParserSupport, TestCase):
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

        self.assertEqual("""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
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
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p>some text</p>
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
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p>schedule text</p>
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

        self.assertEqual("""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
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
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p>some text</p>
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
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
            <FRBRlanguage language="eng"/>
          </FRBRExpression>
          <FRBRManifestation>
            <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10/eng"/>
            <FRBRdate date="2020-07-22" name="Generation"/>
            <FRBRauthor href=""/>
          </FRBRManifestation>
        </identification>
        <references source="#cobalt">
          <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        </references>
      </meta>
      <mainBody>
        <p>schedule text</p>
      </mainBody>
    </doc>
  </attachment>
</attachments>
""", xml)
