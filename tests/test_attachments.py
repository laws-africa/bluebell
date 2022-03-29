from datetime import date
from unittest import TestCase

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
            'attribs': {'name': 'annexure'},
            'heading': [{
                'type': 'text',
                'value': 'a heading',
            }],
            'subheading': [{
                'type': 'text',
                'value': 'subheading',
            }],
            'children': [{
                'type': 'element',
                'name': 'mainBody',
                'children': [{
                    'name': 'p',
                    'type': 'content',
                    'children': [{
                        'type': 'text',
                        'value': 'some text',
                    }]}],
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
            'attribs': {'name': 'annexure'},
            'heading': [{
                'type': 'text',
                'value': 'a heading',
            }],
            'children': [{
                'type': 'element',
                'name': 'mainBody',
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
                }],
            }]
        }, tree.to_dict())

    def test_multiple_attachments(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text
  
  CROSSHEADING crossheading
CROSSHEADING crossheading2

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
                    'type': 'element',
                    'name': 'mainBody',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'some text',
                        }]
                    }, {
                        'name': 'hcontainer',
                        'type': 'element',
                        'attribs': {'name': 'hcontainer'},
                         'children': [{
                             'name': 'crossHeading',
                             'type': 'element',
                             'children': [{
                                 'type': 'text',
                                 'value': 'crossheading'
                             }],
                         }, {
                             'name': 'crossHeading',
                             'type': 'element',
                             'children': [{
                                 'type': 'text',
                                 'value': 'crossheading2'
                             }]
                         }]
                    }]
                }]
            }, {
                'type': 'element',
                'name': 'attachment',
                'attribs': {'name': 'schedule'},
                'heading': [{
                    'type': 'text',
                    'value': 'heading',
                }],
                'children': [{
                    'type': 'element',
                    'name': 'mainBody',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'schedule text',
                        }]
                    }],
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())

        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="a heading"/>
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
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
        <hcontainer eId="att_1__hcontainer_1" name="hcontainer">
          <crossHeading eId="att_1__hcontainer_1__crossHeading_1">crossheading</crossHeading>
          <crossHeading eId="att_1__hcontainer_1__crossHeading_2">crossheading2</crossHeading>
        </hcontainer>
      </mainBody>
    </doc>
  </attachment>
  <attachment eId="att_2">
    <heading>heading</heading>
    <doc name="schedule">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="heading"/>
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
                    'type': 'element',
                    'name': 'mainBody',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'some text',
                        }]
                    }],
                }]
            }, {
                'type': 'element',
                'name': 'attachment',
                'attribs': {'name': 'schedule'},
                'heading': [{
                    'type': 'text',
                    'value': 'heading',
                }],
                'children': [{
                    'type': 'element',
                    'name': 'mainBody',
                    'children': [{
                        'name': 'p',
                        'type': 'content',
                        'children': [{
                            'type': 'text',
                            'value': 'schedule text',
                        }]
                    }],
                }]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())

        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="a heading"/>
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
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
      </mainBody>
    </doc>
  </attachment>
  <attachment eId="att_2">
    <heading>heading</heading>
    <doc name="schedule">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="heading"/>
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
            'attribs': {'name': 'annexure'},
            'heading': [{'type': 'text', 'value': 'a heading'}],
            'subheading': [{'type': 'text', 'value': 'subheading'}],
            'children': [
                {
                    'type': 'element',
                    'name': 'mainBody',
                    'children': [
                        {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'some text'}]
                        },
                    ],
                },
                {
                    'type': 'element',
                    'name': 'attachments',
                    'children': [{
                        'type': 'element',
                        'name': 'attachment',
                        'attribs': {'name': 'schedule'},
                        'heading': [{'type': 'text', 'value': 'heading'}],
                        'subheading': [{'type': 'text', 'value': 'a nother subheading'}],
                        'children': [{
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [{
                                'name': 'p',
                                'type': 'content',
                                'children': [{'type': 'text', 'value': 'schedule text'}]}],
                        }],
                    }]
                },

            ]
        }, tree.to_dict())
        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())
        self.assertEqual(f"""<attachment xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="att_1">
  <heading>a heading</heading>
  <subheading>subheading</subheading>
  <doc name="annexure">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
          <FRBRuri value="/akn/za/act/2009/10"/>
          <FRBRalias name="title" value="a heading"/>
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
    </meta>
    <mainBody>
      <p eId="att_1__p_1">some text</p>
    </mainBody>
    <attachments>
      <attachment eId="att_1__att_1">
        <heading>heading</heading>
        <subheading>a nother subheading</subheading>
        <doc name="schedule">
          <meta>
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1"/>
                <FRBRuri value="/akn/za/act/2009/10"/>
                <FRBRalias name="title" value="heading"/>
                <FRBRdate date="2009" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="za"/>
                <FRBRnumber value="10"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                <FRBRuri value="/akn/za/act/2009/10/eng"/>
                <FRBRdate date="{today}" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                <FRBRuri value="/akn/za/act/2009/10/eng"/>
                <FRBRdate date="{today}" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
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

    def test_nested_attachments_multiple(self):
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
                    'attribs': {'name': 'annexure'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [
                                {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'some text'}]
                                },
                            ],
                        },
                        {
                            'type': 'element',
                            'name': 'attachments',
                            'children': [
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'attribs': {'name': 'schedule'},
                                    'children': [{
                                        'type': 'element',
                                        'name': 'mainBody',
                                        'children': [{
                                            'type': 'content',
                                            'name': 'p',
                                            'children': [{
                                                'type': 'text',
                                                'value': 'schedule text'}]}],
                                    }],
                                    'heading': [{'type': 'text', 'value': 'heading'}],
                                    'subheading': [{'type': 'text', 'value': 'a nother subheading'}]}
                            ]
                        }
                    ],
                    'heading': [{'type': 'text', 'value': 'a heading'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}]
                },
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'back out'}],
                    'subheading': [{'type': 'text', 'value': 'subhead'}],
                    'attribs': {'name': 'annexure'},
                    'children': [{
                        'type': 'element',
                        'name': 'mainBody',
                        'children': [{
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'more content'}]}],
                    }],
                }
            ]
        }, tree.to_dict())
        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="a heading"/>
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
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>heading</heading>
          <subheading>a nother subheading</subheading>
          <doc name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="heading"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
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
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="back out"/>
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

  some more text

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
                    'heading': [{'type': 'text', 'value': 'a heading'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}],
                    'attribs': {'name': 'annexure'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [{
                                'type': 'content',
                                'name': 'p',
                                'children': [{'type': 'text', 'value': 'some text'}]
                            }, {
                                'type': 'content',
                                'name': 'p',
                                'children': [{'type': 'text', 'value': 'some more text'}]
                            }],
                        },
                        {
                            'type': 'element',
                            'name': 'attachments',
                            'children': [
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'heading'}],
                                    'subheading': [{'type': 'text', 'value': 'a nother subheading'}],
                                    'attribs': {'name': 'schedule'},
                                    'children': [
                                        {
                                            'type': 'element',
                                            'name': 'mainBody',
                                            'children': [{
                                                'type': 'content',
                                                'name': 'p',
                                                'children': [],
                                            }],
                                        },
                                        {
                                            'type': 'element',
                                            'name': 'attachments',
                                            'children': [
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [{'type': 'text', 'value': 'deeper heading'}],
                                                    'attribs': {'name': 'schedule'},
                                                    'children': [
                                                        {
                                                            'type': 'element',
                                                            'name': 'mainBody',
                                                            'children': [{
                                                                'type': 'content',
                                                                'name': 'p',
                                                                'children': [],
                                                            }],
                                                        },
                                                        {
                                                            'type': 'element',
                                                            'name': 'attachments',
                                                            'children': [
                                                                {
                                                                    'type': 'element',
                                                                    'name': 'attachment',
                                                                    'heading': [{'type': 'text', 'value': 'even deeper heading'}],
                                                                    'attribs': {'name': 'schedule'},
                                                                    'children': [{
                                                                        'type': 'element',
                                                                        'name': 'mainBody',
                                                                        'children': [{
                                                                            'type': 'content',
                                                                            'name': 'p',
                                                                            'children': [{'type': 'text', 'value': 'content in final nest'}]}],
                                                                    }],
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                },
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'back out'}],
                    'subheading': [{'type': 'text', 'value': 'subhead'}],
                    'attribs': {'name': 'annexure'},
                    'children': [{
                        'type': 'element',
                        'name': 'mainBody',
                        'children': [{
                            'type': 'content',
                            'name': 'p',
                            'children': [{'type': 'text', 'value': 'more content'}]
                        }],
                    }],
                }
            ]
        }, tree.to_dict())
        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="a heading"/>
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
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
        <p eId="att_1__p_2">some more text</p>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>heading</heading>
          <subheading>a nother subheading</subheading>
          <doc name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="heading"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_1__att_1__p_1"/>
            </mainBody>
            <attachments>
              <attachment eId="att_1__att_1__att_1">
                <heading>deeper heading</heading>
                <doc name="schedule">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="deeper heading"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_1__att_1__p_1"/>
                  </mainBody>
                  <attachments>
                    <attachment eId="att_1__att_1__att_1__att_1">
                      <heading>even deeper heading</heading>
                      <doc name="schedule">
                        <meta>
                          <identification source="#cobalt">
                            <FRBRWork>
                              <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1/schedule_1/schedule_1"/>
                              <FRBRuri value="/akn/za/act/2009/10"/>
                              <FRBRalias name="title" value="even deeper heading"/>
                              <FRBRdate date="2009" name="Generation"/>
                              <FRBRauthor href=""/>
                              <FRBRcountry value="za"/>
                              <FRBRnumber value="10"/>
                            </FRBRWork>
                            <FRBRExpression>
                              <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/schedule_1/schedule_1"/>
                              <FRBRuri value="/akn/za/act/2009/10/eng"/>
                              <FRBRdate date="{today}" name="Generation"/>
                              <FRBRauthor href=""/>
                              <FRBRlanguage language="eng"/>
                            </FRBRExpression>
                            <FRBRManifestation>
                              <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/schedule_1/schedule_1"/>
                              <FRBRuri value="/akn/za/act/2009/10/eng"/>
                              <FRBRdate date="{today}" name="Generation"/>
                              <FRBRauthor href=""/>
                            </FRBRManifestation>
                          </identification>
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
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="back out"/>
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
      </meta>
      <mainBody>
        <p eId="att_2__p_1">more content</p>
      </mainBody>
    </doc>
  </attachment>
</attachments>
""", xml)

    def test_nested_attachments_component_names(self):
        tree = self.parse("""
ANNEXURE first

  ANNEXURE first, first

    ANNEXURE first, first, first

      content

    ANNEXURE first, first, second

      content

    SCHEDULE first, first, first schedule

      content

  ANNEXURE first, second

    SCHEDULE first, second, first schedule

      content

    ANNEXURE first, second, first

      content

ANNEXURE second

  ANNEXURE second, first

    content

  ANNEXURE second, second

    content

SCHEDULE first schedule

  SCHEDULE first, first

    content

  ANNEXURE first, first annex

    content

""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'first'}],
                    'attribs': {'name': 'annexure'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [{
                                'type': 'content',
                                'name': 'p',
                                'children': [],
                            }],
                        },
                        {
                            'type': 'element',
                            'name': 'attachments',
                            'children': [
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'first, first'}],
                                    'attribs': {'name': 'annexure'},
                                    'children': [
                                        {
                                            'type': 'element',
                                            'name': 'mainBody',
                                            'children': [{
                                                'type': 'content',
                                                'name': 'p',
                                                'children': [],
                                            }],
                                        },
                                        {
                                            'type': 'element',
                                            'name': 'attachments',
                                            'children': [
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [{'type': 'text', 'value': 'first, first, first'}],
                                                    'attribs': {'name': 'annexure'},
                                                    'children': [{
                                                        'type': 'element',
                                                        'name': 'mainBody',
                                                        'children': [{
                                                            'type': 'content',
                                                            'name': 'p',
                                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                                    }],
                                                },
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [{'type': 'text', 'value': 'first, first, second'}],
                                                    'attribs': {'name': 'annexure'},
                                                    'children': [{
                                                        'type': 'element',
                                                        'name': 'mainBody',
                                                        'children': [{
                                                            'type': 'content',
                                                            'name': 'p',
                                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                                    }],
                                                },
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [
                                                        {'type': 'text', 'value': 'first, first, first schedule'}],
                                                    'attribs': {'name': 'schedule'},
                                                    'children': [{
                                                        'type': 'element',
                                                        'name': 'mainBody',
                                                        'children': [{
                                                            'type': 'content',
                                                            'name': 'p',
                                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                                    }],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'first, second'}],
                                    'attribs': {'name': 'annexure'},
                                    'children': [
                                        {
                                            'type': 'element',
                                            'name': 'mainBody',
                                            'children': [{
                                                'type': 'content',
                                                'name': 'p',
                                                'children': [],
                                            }],
                                        },
                                        {
                                            'type': 'element',
                                            'name': 'attachments',
                                            'children': [
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [
                                                        {'type': 'text', 'value': 'first, second, first schedule'}],
                                                    'attribs': {'name': 'schedule'},
                                                    'children': [{
                                                        'type': 'element',
                                                        'name': 'mainBody',
                                                        'children': [{
                                                            'type': 'content',
                                                            'name': 'p',
                                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                                    }],
                                                },
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [{'type': 'text', 'value': 'first, second, first'}],
                                                    'attribs': {'name': 'annexure'},
                                                    'children': [{
                                                        'type': 'element',
                                                        'name': 'mainBody',
                                                        'children': [{
                                                            'type': 'content',
                                                            'name': 'p',
                                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                                    }],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'second'}],
                    'attribs': {'name': 'annexure'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [{
                                'type': 'content',
                                'name': 'p',
                                'children': [],
                            }],
                        },
                        {
                            'type': 'element',
                            'name': 'attachments',
                            'children': [
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'second, first'}],
                                    'attribs': {'name': 'annexure'},
                                    'children': [{
                                        'type': 'element',
                                        'name': 'mainBody',
                                        'children': [{
                                            'type': 'content',
                                            'name': 'p',
                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                    }],
                                },
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'second, second'}],
                                    'attribs': {'name': 'annexure'},
                                    'children': [{
                                        'type': 'element',
                                        'name': 'mainBody',
                                        'children': [{
                                            'type': 'content',
                                            'name': 'p',
                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                    }],
                                },
                            ],
                        },
                    ],
                },
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'first schedule'}],
                    'attribs': {'name': 'schedule'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [{
                                'type': 'content',
                                'name': 'p',
                                'children': [],
                            }],
                        },
                        {
                            'type': 'element',
                            'name': 'attachments',
                            'children': [
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'first, first'}],
                                    'attribs': {'name': 'schedule'},
                                    'children': [{
                                        'type': 'element',
                                        'name': 'mainBody',
                                        'children': [{
                                            'type': 'content',
                                            'name': 'p',
                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                    }],
                                },
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'first, first annex'}],
                                    'attribs': {'name': 'annexure'},
                                    'children': [{
                                        'type': 'element',
                                        'name': 'mainBody',
                                        'children': [{
                                            'type': 'content',
                                            'name': 'p',
                                            'children': [{'type': 'text', 'value': 'content'}]}],
                                    }],
                                },
                            ],
                        },
                    ],
                },
            ]
        }, tree.to_dict())
        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>first</heading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="first"/>
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
      </meta>
      <mainBody>
        <p eId="att_1__p_1"/>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>first, first</heading>
          <doc name="annexure">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="first, first"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_1__att_1__p_1"/>
            </mainBody>
            <attachments>
              <attachment eId="att_1__att_1__att_1">
                <heading>first, first, first</heading>
                <doc name="annexure">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/annexure_1/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="first, first, first"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_1__att_1__p_1">content</p>
                  </mainBody>
                </doc>
              </attachment>
              <attachment eId="att_1__att_1__att_2">
                <heading>first, first, second</heading>
                <doc name="annexure">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/annexure_1/annexure_2"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="first, first, second"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1/annexure_2"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1/annexure_2"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_1__att_2__p_1">content</p>
                  </mainBody>
                </doc>
              </attachment>
              <attachment eId="att_1__att_1__att_3">
                <heading>first, first, first schedule</heading>
                <doc name="schedule">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/annexure_1/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="first, first, first schedule"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_1/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_1__att_3__p_1">content</p>
                  </mainBody>
                </doc>
              </attachment>
            </attachments>
          </doc>
        </attachment>
        <attachment eId="att_1__att_2">
          <heading>first, second</heading>
          <doc name="annexure">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1/annexure_2"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="first, second"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_2"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_2"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_1__att_2__p_1"/>
            </mainBody>
            <attachments>
              <attachment eId="att_1__att_2__att_1">
                <heading>first, second, first schedule</heading>
                <doc name="schedule">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/annexure_2/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="first, second, first schedule"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_2/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_2/schedule_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_2__att_1__p_1">content</p>
                  </mainBody>
                </doc>
              </attachment>
              <attachment eId="att_1__att_2__att_2">
                <heading>first, second, first</heading>
                <doc name="annexure">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/annexure_2/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="first, second, first"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_2/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/annexure_2/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_2__att_2__p_1">content</p>
                  </mainBody>
                </doc>
              </attachment>
            </attachments>
          </doc>
        </attachment>
      </attachments>
    </doc>
  </attachment>
  <attachment eId="att_2">
    <heading>second</heading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="second"/>
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
      </meta>
      <mainBody>
        <p eId="att_2__p_1"/>
      </mainBody>
      <attachments>
        <attachment eId="att_2__att_1">
          <heading>second, first</heading>
          <doc name="annexure">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_2/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="second, first"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_2__att_1__p_1">content</p>
            </mainBody>
          </doc>
        </attachment>
        <attachment eId="att_2__att_2">
          <heading>second, second</heading>
          <doc name="annexure">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_2/annexure_2"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="second, second"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2/annexure_2"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_2/annexure_2"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_2__att_2__p_1">content</p>
            </mainBody>
          </doc>
        </attachment>
      </attachments>
    </doc>
  </attachment>
  <attachment eId="att_3">
    <heading>first schedule</heading>
    <doc name="schedule">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!schedule_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="first schedule"/>
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
      </meta>
      <mainBody>
        <p eId="att_3__p_1"/>
      </mainBody>
      <attachments>
        <attachment eId="att_3__att_1">
          <heading>first, first</heading>
          <doc name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!schedule_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="first, first"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_3__att_1__p_1">content</p>
            </mainBody>
          </doc>
        </attachment>
        <attachment eId="att_3__att_2">
          <heading>first, first annex</heading>
          <doc name="annexure">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!schedule_1/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="first, first annex"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!schedule_1/annexure_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_3__att_2__p_1">content</p>
            </mainBody>
          </doc>
        </attachment>
      </attachments>
    </doc>
  </attachment>
</attachments>
""", xml)

    def test_nested_attachments_with_hier(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text

  some more text

  SCHEDULE is a heading
    SUBHEADING is a subheading

    PARA 1. - is a paragraph

      para 1 content

    ANNEXURE is an Annex

      content of Annex to Schedule to first Annex

    ANNEXURE para

      content of second Annex to Schedule to first Annex

ANNEXURE back out
  SUBHEADING subheading

  text :)

""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'a heading'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}],
                    'attribs': {'name': 'annexure'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [
                                {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'some text'}]
                                },
                                {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'some more text'}]
                                },
                            ],
                        },
                        {
                            'type': 'element',
                            'name': 'attachments',
                            'children': [
                                {
                                    'type': 'element',
                                    'name': 'attachment',
                                    'heading': [{'type': 'text', 'value': 'is a heading'}],
                                    'subheading': [{'type': 'text', 'value': 'is a subheading'}],
                                    'attribs': {'name': 'schedule'},
                                    'children': [
                                        {
                                            'type': 'element',
                                            'name': 'mainBody',
                                            'children': [
                                                {
                                                    'type': 'hier',
                                                    'name': 'paragraph',
                                                    'children': [
                                                        {
                                                            'type': 'content',
                                                            'name': 'p',
                                                            'children': [
                                                                {'type': 'text', 'value': 'para 1 content'}]
                                                        },
                                                    ],
                                                    'num': '1.',
                                                    'heading': [{'type': 'text', 'value': 'is a paragraph'}]
                                                },
                                            ],
                                        },
                                        {
                                            'type': 'element',
                                            'name': 'attachments',
                                            'children': [
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [
                                                        {'type': 'text', 'value': 'is an Annex'}],
                                                    'attribs': {'name': 'annexure'},
                                                    'children': [
                                                        {
                                                            'type': 'element',
                                                            'name': 'mainBody',
                                                            'children': [
                                                                {
                                                                    'type': 'content',
                                                                    'name': 'p',
                                                                    'children': [{
                                                                        'type': 'text',
                                                                        'value': 'content of Annex to Schedule to first Annex'}]
                                                                }
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    'type': 'element',
                                                    'name': 'attachment',
                                                    'heading': [{'type': 'text', 'value': 'para'}],
                                                    'attribs': {'name': 'annexure'},
                                                    'children': [
                                                        {
                                                            'type': 'element',
                                                            'name': 'mainBody',
                                                            'children': [
                                                                {
                                                                    'type': 'content',
                                                                    'name': 'p',
                                                                    'children': [{
                                                                        'type': 'text',
                                                                        'value': 'content of second Annex to Schedule to first Annex'}]
                                                                }
                                                            ],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'back out'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}],
                    'attribs': {'name': 'annexure'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [
                                {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{'type': 'text', 'value': 'text :)'}],
                                },
                            ],
                        },
                    ],
                },
            ]}, tree.to_dict())
        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="a heading"/>
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
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
        <p eId="att_1__p_2">some more text</p>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>is a heading</heading>
          <subheading>is a subheading</subheading>
          <doc name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="is a heading"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <paragraph eId="att_1__att_1__para_1">
                <num>1.</num>
                <heading>is a paragraph</heading>
                <content>
                  <p eId="att_1__att_1__para_1__p_1">para 1 content</p>
                </content>
              </paragraph>
            </mainBody>
            <attachments>
              <attachment eId="att_1__att_1__att_1">
                <heading>is an Annex</heading>
                <doc name="annexure">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="is an Annex"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/annexure_1"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_1__att_1__p_1">content of Annex to Schedule to first Annex</p>
                  </mainBody>
                </doc>
              </attachment>
              <attachment eId="att_1__att_1__att_2">
                <heading>para</heading>
                <doc name="annexure">
                  <meta>
                    <identification source="#cobalt">
                      <FRBRWork>
                        <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1/annexure_2"/>
                        <FRBRuri value="/akn/za/act/2009/10"/>
                        <FRBRalias name="title" value="para"/>
                        <FRBRdate date="2009" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRcountry value="za"/>
                        <FRBRnumber value="10"/>
                      </FRBRWork>
                      <FRBRExpression>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/annexure_2"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                        <FRBRlanguage language="eng"/>
                      </FRBRExpression>
                      <FRBRManifestation>
                        <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1/annexure_2"/>
                        <FRBRuri value="/akn/za/act/2009/10/eng"/>
                        <FRBRdate date="{today}" name="Generation"/>
                        <FRBRauthor href=""/>
                      </FRBRManifestation>
                    </identification>
                  </meta>
                  <mainBody>
                    <p eId="att_1__att_1__att_2__p_1">content of second Annex to Schedule to first Annex</p>
                  </mainBody>
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
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_2"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="back out"/>
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
      </meta>
      <mainBody>
        <p eId="att_2__p_1">text :)</p>
      </mainBody>
    </doc>
  </attachment>
</attachments>
""", xml)

    def test_push_nested_attachment_to_end(self):
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  some text

  SCHEDULE actually a schedule
    SUBHEADING actually a subheading

    Schedule (to Annexure) content

  some more text, pushed into Schedule to Annexure

even more text, pushed into Annex (will move up)

  SCHEDULE not a heading
    SUBHEADING just text

    PARA 1. - just text

      more just text

    ANNEXURE not an Annex

      even more just text

""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'a heading'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}],
                    'attribs': {'name': 'annexure'},
                    'children': [{
                        'type': 'element',
                        'name': 'mainBody',
                        'children': [{
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'some text'}]
                        }, {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'even more text, pushed into Annex (will move up)'}]
                        }, {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'SCHEDULE not a heading'}]
                        }, {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'SUBHEADING just text'}]
                        }, {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'PARA 1. - just text'}]
                        }, {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'more just text'}]
                        }, {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'ANNEXURE not an Annex'}]
                        }, {
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'even more just text'}]
                        }],
                    }, {
                        'type': 'element',
                        'name': 'attachments',
                        'children': [{
                            'type': 'element',
                            'name': 'attachment',
                            'heading': [{'type': 'text', 'value': 'actually a schedule'}],
                            'subheading': [{'type': 'text', 'value': 'actually a subheading'}],
                            'attribs': {'name': 'schedule'},
                            'children': [{
                                'type': 'element',
                                'name': 'mainBody',
                                'children': [{
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'Schedule (to Annexure) content'}]
                                }, {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'some more text, pushed into Schedule to Annexure'}]}],
                            }],
                        }],
                    }],
                }]}, tree.to_dict())
        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="a heading"/>
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
      </meta>
      <mainBody>
        <p eId="att_1__p_1">some text</p>
        <p eId="att_1__p_2">even more text, pushed into Annex (will move up)</p>
        <p eId="att_1__p_3">SCHEDULE not a heading</p>
        <p eId="att_1__p_4">SUBHEADING just text</p>
        <p eId="att_1__p_5">PARA 1. - just text</p>
        <p eId="att_1__p_6">more just text</p>
        <p eId="att_1__p_7">ANNEXURE not an Annex</p>
        <p eId="att_1__p_8">even more just text</p>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>actually a schedule</heading>
          <subheading>actually a subheading</subheading>
          <doc name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="actually a schedule"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_1__att_1__p_1">Schedule (to Annexure) content</p>
              <p eId="att_1__att_1__p_2">some more text, pushed into Schedule to Annexure</p>
            </mainBody>
          </doc>
        </attachment>
      </attachments>
    </doc>
  </attachment>
</attachments>
""", xml)

    def test_nested_attachments_overindented(self):
        """ A correctly marked-up Schedule inside a Division in an attachment will be parsed as text,
            but once it's unindented it'll be recognised as a Schedule again.
        """
        tree = self.parse("""
ANNEXURE a heading
  SUBHEADING subheading

  DIVISION A. - The First Division

    contento

    SCHEDULE not a heading
      SUBHEADING not a subheading

      not Schedule content

  SCHEDULE a heading again
    SUBHEADING a subheading again

    Schedule content again

""", 'attachments')
        self.assertEqual({
            'type': 'element',
            'name': 'attachments',
            'children': [
                {
                    'type': 'element',
                    'name': 'attachment',
                    'heading': [{'type': 'text', 'value': 'a heading'}],
                    'subheading': [{'type': 'text', 'value': 'subheading'}],
                    'attribs': {'name': 'annexure'},
                    'children': [
                        {
                            'type': 'element',
                            'name': 'mainBody',
                            'children': [{
                                'type': 'hier',
                                'name': 'division',
                                'children': [{
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'contento'}]
                                }, {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'SCHEDULE not a heading'}]
                                }, {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'SUBHEADING not a subheading'}]
                                }, {
                                    'type': 'content',
                                    'name': 'p',
                                    'children': [{
                                        'type': 'text',
                                        'value': 'not Schedule content'}]}],
                                'num': 'A.',
                                'heading': [{
                                    'type': 'text',
                                    'value': 'The First Division'}]
                            }],
                        },
                        {
                            'type': 'element',
                            'name': 'attachments',
                            'children': [{
                                'type': 'element',
                                'name': 'attachment',
                                'heading': [{'type': 'text', 'value': 'a heading again'}],
                                'subheading': [{'type': 'text', 'value': 'a subheading again'}],
                                'attribs': {'name': 'schedule'},
                                'children': [{
                                    'type': 'element',
                                    'name': 'mainBody',
                                    'children': [{
                                        'type': 'content',
                                        'name': 'p',
                                        'children': [{
                                            'type': 'text',
                                            'value': 'Schedule content again'}]
                                    }],
                                }],
                            }],
                        },
                    ],
                }
            ]}, tree.to_dict())
        xml = self.tostring(self.to_xml(tree.to_dict()))
        today = datestring(date.today())
        self.assertEqual(f"""<attachments xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <attachment eId="att_1">
    <heading>a heading</heading>
    <subheading>subheading</subheading>
    <doc name="annexure">
      <meta>
        <identification source="#cobalt">
          <FRBRWork>
            <FRBRthis value="/akn/za/act/2009/10/!annexure_1"/>
            <FRBRuri value="/akn/za/act/2009/10"/>
            <FRBRalias name="title" value="a heading"/>
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
      </meta>
      <mainBody>
        <division eId="att_1__dvs_A">
          <num>A.</num>
          <heading>The First Division</heading>
          <content>
            <p eId="att_1__dvs_A__p_1">contento</p>
            <p eId="att_1__dvs_A__p_2">SCHEDULE not a heading</p>
            <p eId="att_1__dvs_A__p_3">SUBHEADING not a subheading</p>
            <p eId="att_1__dvs_A__p_4">not Schedule content</p>
          </content>
        </division>
      </mainBody>
      <attachments>
        <attachment eId="att_1__att_1">
          <heading>a heading again</heading>
          <subheading>a subheading again</subheading>
          <doc name="schedule">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/akn/za/act/2009/10/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10"/>
                  <FRBRalias name="title" value="a heading again"/>
                  <FRBRdate date="2009" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="za"/>
                  <FRBRnumber value="10"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/akn/za/act/2009/10/eng/!annexure_1/schedule_1"/>
                  <FRBRuri value="/akn/za/act/2009/10/eng"/>
                  <FRBRdate date="{today}" name="Generation"/>
                  <FRBRauthor href=""/>
                </FRBRManifestation>
              </identification>
            </meta>
            <mainBody>
              <p eId="att_1__att_1__p_1">Schedule content again</p>
            </mainBody>
          </doc>
        </attachment>
      </attachments>
    </doc>
  </attachment>
</attachments>
""", xml)
